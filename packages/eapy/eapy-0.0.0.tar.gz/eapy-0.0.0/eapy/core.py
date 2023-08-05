import os
import sys
import time
import shutil
import random
import asyncio
import logging
import pprint
from typing import Union
from pathlib import Path
from collections import deque
import ray
import numpy as np
import matplotlib.pyplot as plt

from . import baseclasses as bc


def setup_logger(log_path: Path = None):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s: %(message)s", datefmt="%H:%M:%S"
    )

    terminal_handler = logging.StreamHandler(sys.stdout)
    terminal_handler.setFormatter(log_fmt)
    terminal_handler.setLevel(logging.DEBUG)
    logger.addHandler(terminal_handler)

    if log_path is not None:
        log_path = Path(log_path)
        file_handler = logging.FileHandler(log_path / f"{logger.name}.log", mode="w")
        file_handler.setFormatter(log_fmt)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger


def log_config(kwargs: dict, log_path: Path = None):
    class repr_wrapper:
        def __init__(self, cls) -> None:
            self._cls = cls

        def __repr__(self) -> str:
            return f"{self._cls.__module__}.{self._cls.__name__}"

    if log_path is not None:
        kwargs["log_path"] = str(kwargs["log_path"])

        with open(log_path / "config.py", "w") as fp:
            fp.write(f"import sys\n")

            path_set = set()
            for component in "population", "selection", "operator", "problem":
                cls = kwargs[component]["type"]
                fp.write(f"import {cls.__module__}\n")
                cls_path = os.path.abspath(sys.modules[cls.__module__].__file__)
                path_set.add(Path(cls_path).parent)
                kwargs[component] = {
                    "type": repr_wrapper(cls),
                    "args": kwargs[component]["args"],
                }

            for path in path_set:
                fp.write(f"\nsys.path.append('{path}')\n")
            fp.write(f"\nCONFIG =")
            pprint.pprint(kwargs, stream=fp)


_PROCESS_RNG: np.random.Generator


def _setup_rng(seed: int) -> None:
    global _PROCESS_RNG
    _PROCESS_RNG = np.random.default_rng(seed)
    random.seed(int.from_bytes(_PROCESS_RNG.bytes(4), "big"))


def get_rng() -> np.random.Generator:
    global _PROCESS_RNG
    return _PROCESS_RNG


class Progress:
    def update(self, progress: float) -> None:
        percent_str = f" {progress*100:5.1f}%"

        if progress == 0:
            eta_str = " eta: --:--:--"
        else:
            eta = (time.perf_counter() - self._start_time) * (1 - progress) / progress
            if eta < 24 * 60 * 60:
                eta_str = time.strftime(" eta: %H:%M:%S", time.gmtime(eta))
            else:
                eta_str = " eta:>24:00:00"

        bar_width = self._terminal_width - len(percent_str) - len(eta_str)
        whole_width = int(progress * (bar_width - 2))
        part_idx = int((progress * (bar_width - 2) - whole_width) * 8)
        part_str = ["", "▏", "▎", "▍", "▌", "▋", "▊", "▉"][part_idx]
        empty_width = bar_width - whole_width - len(part_str) - 2
        bar_str = "▕" + "█" * whole_width + part_str + " " * empty_width + "▏"

        sys.stdout.write(bar_str + percent_str + eta_str + "\r")
        sys.stdout.flush()

    def __enter__(self) -> "Progress":
        self._terminal_width = shutil.get_terminal_size((80, 24)).columns
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, *exc_args) -> None:
        self.update(1)
        sys.stdout.write("\n")
        sys.stdout.flush()


@ray.remote
class RayDeme:
    def initialise(
        self,
        seed: int,
        population_size: int,
        population: dict,
        selection: dict,
        problem: dict,
        operator: dict,
    ) -> None:
        _setup_rng(seed)

        self._population: bc.Population = population["type"](**population["args"])
        self._selection: bc.Selection = selection["type"](**selection["args"])
        self._problem: bc.Problem = problem["type"](**problem["args"])
        self._operator: bc.Problem = operator["type"](**operator["args"])

        self._population.populate(population_size, self._operator, self._problem)

    def process(
        self,
        variations_to_complete: int,
        immigrants: list[bc.Model],
        emigrants_requested: int,
    ) -> tuple[int, list[bc.Model], list[float]]:
        self._population.insert_migrants(immigrants)

        variations_completed = 0
        while variations_completed < variations_to_complete:
            variations_completed += self._population.advance(
                self._selection, self._operator, self._problem
            )

        emigrants = self._population.get_migrants(emigrants_requested)
        fitness_list = [model.fitness for model in self._population.populace]
        return (variations_completed, emigrants, fitness_list)

    def get_populace(self) -> list[bc.Model]:
        return self._population.populace


class RayManager:
    def __init__(self, variations: int, variations_per_migration: int) -> None:
        self._variations_remaining = variations
        self._variations_completed = 0
        self._variations_per_migration = variations_per_migration

    async def run(
        self,
        raydemes: list[RayDeme],
        migrant_buffers: list[deque[bc.Model]],
        sync: bool = False,
    ) -> None:
        progress_task = asyncio.create_task(self._report_progress())

        make_task = lambda i: asyncio.create_task(
            self.manage(raydemes[i], migrant_buffers[i - 1], migrant_buffers[i]),
            name=str(i),
        )

        return_when = asyncio.ALL_COMPLETED if sync else asyncio.FIRST_COMPLETED

        self._fitness_logs = {raydeme: {} for raydeme in raydemes}

        done, pending = {}, {make_task(i) for i in range(len(raydemes))}
        while self._variations_remaining > 0:
            pending |= {make_task(int(task.get_name())) for task in done}
            done, pending = await asyncio.wait(pending, return_when=return_when)
        if pending:
            await asyncio.wait(pending, return_when=asyncio.ALL_COMPLETED)

        progress_task.cancel()

    async def manage(
        self,
        raydeme: RayDeme,
        immigrant_buffer: deque[bc.Model],
        emigrant_buffer: deque[bc.Model],
    ) -> None:
        variations_to_complete = min(
            self._variations_remaining, self._variations_per_migration
        )
        self._variations_remaining -= variations_to_complete

        immigrants = list(immigrant_buffer)
        immigrant_buffer.clear()
        variations_completed, emigrants, fitness_list = await raydeme.process.remote(
            variations_to_complete, immigrants, emigrant_buffer.maxlen
        )
        emigrant_buffer.extend(emigrants)

        self._variations_remaining += variations_to_complete - variations_completed
        self._variations_completed += variations_completed

        self._fitness_logs[raydeme][self._variations_remaining] = fitness_list

    async def _report_progress(self) -> None:
        total_variations = self._variations_remaining

        with Progress() as progress:
            while True:
                progress.update(self._variations_completed / total_variations)
                await asyncio.sleep(1)

    def log_fitness(self, log_path: Path = None) -> None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))

        for fitness_log in self._fitness_logs.values():
            x = self._variations_completed - np.array(list(fitness_log.keys()))

            fitness_array = np.array(list(fitness_log.values()))
            fitness_array.sort(axis=1)
            y = fitness_array[:, 0]
            ax.plot(x, y)

        ax.set_yscale("log")
        ax.set_ylabel("Fitness")
        ax.set_xlabel("Variations")
        ax.set_title("Fitness vs Variations")

        fig.savefig(log_path / "fitness.png")


def genetic_algorithm(
    generations: int,
    population_size: int,
    population: dict,
    selection: dict,
    problem: dict,
    operator: dict,
    deme_count: int = None,
    migration_size: int = None,
    migration_period: int = None,
    sync: bool = False,
    seed: int = None,
    log_path: Union[str, Path] = None,
) -> None:
    ### Input Validation ###
    if log_path is not None and type(log_path) not in (str, Path):
        raise TypeError("log_path must be of type str or Path")
    elif log_path is not None and not os.path.exists(log_path):
        raise FileNotFoundError(f"No such file or directory: '{log_path}'")
    elif type(log_path) is str:
        log_path: Path = Path(log_path)
    logger = setup_logger(log_path)

    if type(generations) is not int:
        raise TypeError("generations must be of type int")
    elif generations < 1:
        raise ValueError("generations must be >= 1")

    cpu_count = os.cpu_count()
    if deme_count is None:
        deme_count = cpu_count
    elif type(deme_count) is not int:
        raise TypeError("deme_count must be of type int")
    elif deme_count < 1:
        raise ValueError("deme_count must be >= 1")
    elif deme_count > cpu_count:
        logger.warning(f"deme_count ({deme_count}) exceeds CPU count ({cpu_count})")

    if type(population_size) is not int:
        raise TypeError("population_size must be of type int")
    elif population_size < deme_count:
        raise ValueError("population_size must be >= deme_count")
    elif population_size % deme_count != 0:
        raise ValueError("population_size must be divisible by deme_count")

    components = {
        "population": population,
        "selection": selection,
        "problem": problem,
        "operator": operator,
    }
    for name, component in components.items():
        if not ("type" in component and "args" in component):
            raise ValueError(
                f"{name} must be a dict in the form: {{'type': <Class>, 'args': <kwargs>}}"
            )
        elif not isinstance(component["type"], type):
            raise TypeError(f"{name}['type'] must be a Class")
        elif type(component["args"]) is not dict:
            raise TypeError(f"{name}['args'] must be a dict")

    if migration_size is None:
        migration_size = int(population_size / deme_count * 0.1)
    elif type(migration_size) is not int:
        raise TypeError("migration_size must be of type int")
    elif migration_size < 0 or migration_size > population_size // deme_count:
        raise ValueError(
            "migration_size must be within [0, population_size/deme_count]"
        )

    if migration_period is None:
        migration_period = generations // deme_count // 10
    elif type(migration_period) is not int:
        raise TypeError("migration_period must be of type int")
    elif migration_period < 1 or migration_period > generations:
        raise ValueError("migration_period must be in the range [1, generations]")

    if type(sync) is not bool:
        raise TypeError("sync must be True or False")
    elif not sync and seed is not None:
        logger.warning(f"Seed is set but sync is disabled")

    if seed is None:
        seed = int.from_bytes(os.urandom(4), "big")
    elif type(seed) is not int:
        raise TypeError("seed must be of type int")

    ### Initialisation ###
    logger.info("Initialising.")
    start = time.perf_counter()

    kwargs = {
        "generations": generations,
        "population_size": population_size,
        "deme_count": deme_count,
        "migration_size": migration_size,
        "migration_period": migration_period,
        "log_path": log_path,
        "seed": seed,
        "sync": sync,
        **components,
    }
    log_config(kwargs, log_path)

    rng = np.random.default_rng(seed)
    deme_seeds = [int.from_bytes(rng.bytes(4), "big") for _ in range(deme_count)]

    quotient, remainder = divmod(population_size, deme_count)
    deme_sizes = [quotient] * deme_count
    deme_sizes[:remainder] = [q + 1 for q in deme_sizes[:remainder]]

    ray.init()
    raydemes = [RayDeme.remote() for _ in range(deme_count)]
    init_objectrefs = [
        raydeme.initialise.remote(
            seed=seed,
            population_size=deme_size,
            **components,
        )
        for raydeme, deme_size, seed in zip(raydemes, deme_sizes, deme_seeds)
    ]
    ray.wait(init_objectrefs, num_returns=deme_count)

    variations = generations * population_size
    variations_per_migration = migration_period * population_size // deme_count
    manager = RayManager(variations, variations_per_migration)

    migrant_buffers = [deque(maxlen=migration_size) for _ in range(len(raydemes))]

    ### Processing ###
    logger.info("Processing.")
    asyncio.run(manager.run(raydemes, migrant_buffers, sync=sync))
    logger.info(f"Done. Duration= {time.perf_counter() - start:.3f}s.")

    ### Results ###
    manager.log_fitness(log_path)

    deme_populaces = ray.get([raydeme.get_populace.remote() for raydeme in raydemes])
    best_model = min([min(populace) for populace in deme_populaces])
    logger.info(f"Best fitness: {best_model.fitness}")
    return best_model

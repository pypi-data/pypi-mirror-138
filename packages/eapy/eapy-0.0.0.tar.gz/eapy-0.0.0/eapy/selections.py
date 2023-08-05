import random
from . import baseclasses as bc


class TournamentSelection(bc.Selection):
    def __init__(self, n: int = 1, k: int = 2) -> None:
        self._n = n  # exchange_size
        self._k = k  # tournament size

    def select(self, models: list[bc.Model]) -> tuple[list[bc.Model], list[bc.Model]]:
        models_to_reproduce = []
        models_to_delete = []
        for _ in range(self._n):
            competitors = random.sample(models, k=self._k)
            competitors.sort()
            models_to_reproduce.append(competitors[0])
            models_to_delete.append(competitors[-1])

        return models_to_reproduce, models_to_delete

import abc
import numpy as np


class Model(abc.ABC):
    fitness: float

    @abc.abstractmethod
    def process(self, inputs: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def __lt__(self, other: "Model") -> bool:
        return self.fitness < other.fitness


class Problem(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, model: Model) -> float:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def Ni(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def No(self) -> int:
        raise NotImplementedError


class Operator(abc.ABC):
    @abc.abstractmethod
    def new_model(self, problem: Problem) -> Model:
        raise NotImplementedError

    @abc.abstractmethod
    def reproduce(self, model: Model) -> Model:
        raise NotImplementedError


class Selection(abc.ABC):
    @abc.abstractmethod
    def select(self, models: list[Model]) -> tuple[list[Model], list[Model]]:
        raise NotImplementedError


class Population(abc.ABC):
    @abc.abstractmethod
    def populate(
        self, population_size: int, operator: Operator, problem: Problem
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def advance(
        self, selection: Selection, operator: Operator, problem: Problem
    ) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def insert_migrants(self, models: list[Model]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_migrants(self, emigrants_requested: int) -> list[Model]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def populace(self) -> list[Model]:
        raise NotImplementedError

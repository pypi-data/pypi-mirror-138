from . import baseclasses as bc


class FlatPopulation(bc.Population):
    def populate(
        self, population_size: int, operator: bc.Operator, problem: bc.Problem
    ) -> None:
        self._populace = []
        for _ in range(population_size):
            new_model = operator.new_model(problem)
            new_model.fitness = problem.evaluate(new_model)
            self._populace.append(new_model)

    def advance(
        self, selection: bc.Selection, operator: bc.Operator, problem: bc.Problem
    ) -> int:
        models_to_reproduce, models_to_delete = selection.select(self._populace)

        for model in models_to_delete:
            self._populace.remove(model)

        for model in models_to_reproduce:
            new_model = operator.reproduce(model)
            new_model.fitness = problem.evaluate(new_model)
            self._populace.append(new_model)

        return len(models_to_reproduce)

    def insert_migrants(self, models: list[bc.Model]) -> None:
        insert_index = len(self._populace) - len(models)
        self._populace[insert_index:] = models[:]

    def get_migrants(self, emigrants_requested: int) -> list[bc.Model]:
        self._populace.sort()
        return self._populace[:emigrants_requested]

    @property
    def populace(self) -> list[bc.Model]:
        return self._populace

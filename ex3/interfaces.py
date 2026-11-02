from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, entity_type: str) -> None:
        self.name: str = name
        self.entity_type: str = entity_type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a {self.entity_type} type Creature"


class TransformCapability(ABC):
    def __init__(self) -> None:
        self._is_transformed: bool = False

    @abstractmethod
    def transform(self) -> None:
        pass

    @abstractmethod
    def revert(self) -> None:
        pass


class CreatureFactory(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_base() -> Creature:
        pass

    @abstractmethod
    def create_evolved() -> Creature:
        pass

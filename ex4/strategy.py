from abc import ABC, abstractmethod
from typing import Any


class BattleStrategy(ABC):
    @abstractmethod
    def act(self, entity: Any) -> str:
        pass

    @abstractmethod
    def is_valid(self, entity: Any) -> bool:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: Any) -> bool:
        return hasattr(entity, "attack")

    def act(self, entity: Any) -> None:
        if not self.is_valid(entity):
            raise ValueError(
                f"Invalid Creature '{entity.__class__.__name__}' for normal strategy"
            )
        print(entity.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: Any) -> bool:
        from ex3.interfaces import TransformCapability
        return isinstance(entity, TransformCapability)

    def act(self, entity: Any) -> None:
        if not self.is_valid(entity):
            raise ValueError(
                f"Invalid Creature '{entity.__class__.__name__}' "
                "for this aggressive strategy"
            )
        entity.transform()
        print(entity.attack())
        entity.revert()
        


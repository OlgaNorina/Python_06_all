from .interfaces import Creature, TransformCapability


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__(name = "Flameling", entity_type = "Fire")
    
    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__(name = "Pyrodon", entity_type = "Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, name = "Shiftling", entity_type = "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self._is_transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def revert(self) -> None:
        self._is_transformed = False
        print(f"{self.name} returns to normal.")

    def transform(self) -> None:
        self._is_transformed = True
        print(f"{self.name} shifts into a sharper form!")


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, name = "Morphagon", entity_type = "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self._is_transformed:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."

    def revert(self) -> None:
        self._is_transformed = False
        print(f"{self.name} stabilizes its form.")

    def transform(self) -> None:
        self._is_transformed = True
        print(f"{self.name} morphs into a dragonic battle form!")

from ex4.strategy import NormalStrategy, AggressiveStrategy
from ex3.factories import FlameFactory, TransformCreatureFactory

def single_battle(opponents: list) -> None:
    print(f"{len(opponents)} opponents involved")

    entities: tuple = []
    for factory, stratege in opponents:
        entity: str = factory.create_base()
        entities.append((entity, stratege))

    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            entity_1, strategy_1 = entities[i]
            entity_2, stratege_2 = entities[j]

            print("\n* Battle *")
            print(entity_1.describe())
            print(" vs.")
            print(entity_2.describe())
            print(" now fight!")

            try:
                strategy_1.act(entity_1)
                stratege_2.act(entity_2)
            except ValueError as err:
                print(f"Battle error, aborting tournament: {err}")
                return


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    print("Tournament 0 (basic)")
    opponents_0: list = [
        (flame_factory, normal),
        (transform_factory, aggressive)
    ]

    items_0 = [f"({factory.create_base().name}+"
        f"{strategy.__class__.__name__.replace('Strategy', '')})"
        for factory, strategy in opponents_0
    ]

    print("["+", ".join(items_0) + "]")

    single_battle(opponents_0)

    print("\nTournament 1 (error)")
    
    opponents_1: list = [
        (transform_factory, aggressive),
        (flame_factory, aggressive)
    ]

    items_1 = [f"({factory.create_base().name}+"
        f"{strategy.__class__.__name__.replace('Strategy', '')})"
        for factory, strategy in opponents_1
    ]
    
    print("["+", ".join(items_1) + "]")

    single_battle(opponents_1)


if __name__ == "__main__":
    main() 

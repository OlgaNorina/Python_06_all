from ex3.factories import FlameFactory, TransformCreatureFactory


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    print("Testing factory")
    flameling = flame_factory.create_base()
    print(flameling.describe())
    print(flameling.attack())

    pyrodon = flame_factory.create_evolved()
    print(pyrodon.describe())
    print(pyrodon.attack())

    print("\nTesting factory")
    shiftling = transform_factory.create_base()
    print(shiftling.describe())
    print(shiftling.attack())

    morphagon = transform_factory.create_evolved()
    print(morphagon.describe())
    print(morphagon.attack())

    print("\nTesting battle")
    print(flameling.describe())
    print(" vs.")
    print(shiftling.describe())
    print("fight!")
    print(flameling.attack())
    print(shiftling.attack())


if __name__ == "__main__":
    main()

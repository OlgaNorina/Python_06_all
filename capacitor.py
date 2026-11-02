from ex3.factories import TransformCreatureFactory

def main() -> None:
    print("Testing Creature with transform capability\n base:")
    transform_factory = TransformCreatureFactory()
    
    shiftling = transform_factory.create_base()
    morphagon = transform_factory.create_evolved()

    print(shiftling.describe())
    print(shiftling.attack())
    shiftling.transform()
    print(shiftling.attack())
    shiftling.revert()

    print("  evolved:")
    print(morphagon.describe())
    print(morphagon.attack())
    morphagon.transform()
    print(morphagon.attack())
    morphagon.revert()


if __name__ == "__main__":
    main()
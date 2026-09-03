from src.rules.evaluator import RuleEvaluator


def main():
    evaluator = RuleEvaluator()

    conditions = evaluator.evaluate(
        soil_moisture=30,
        temperature=30,
        uv=5,
    )

    print("Aktive Umweltbedingungen:")
    print(conditions)


if __name__ == "__main__":
    main()

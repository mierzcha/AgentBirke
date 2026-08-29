from src.llm.client import OllamaClient


def main():
    client = OllamaClient()

    prompt = "Sag kurz Hallo. Du bist Agent Birke."

    answer = client.generate(prompt)

    print("Antwort:")
    print(answer)


if __name__ == "__main__":
    main()

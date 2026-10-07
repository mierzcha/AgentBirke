from src.llm.open_webui_client import OpenWebUIClient

def main():
    client = OpenWebUIClient()
    answer = client.generate("Welche Maßnahmen wurden nach 1990 zur Verbesserung der Wasserqualität der Elbe eingeleitet?")
    print("Antwort:")
    print(answer)

if __name__ == "__main__":
    main()
from clonellm import CloneLLM, LiteLLMEmbeddings
from examples.const import EXIT_COMMANDS


def main() -> None:
    documents = [open("about_me.txt").read()]
    embedding = LiteLLMEmbeddings(model="text-embedding-3-small")
    clone = CloneLLM(model="gpt-4o-mini", documents=documents, embedding=embedding)
    clone.fit()

    while True:
        prompt = input("Question: ")
        if prompt.strip().lower() in EXIT_COMMANDS:
            break
        response = clone.invoke(prompt)
        print("Response:", response, end="\n\n")


if __name__ == "__main__":
    main()

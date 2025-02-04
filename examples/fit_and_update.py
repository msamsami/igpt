from langchain_community.document_loaders import (
    DirectoryLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
)
from langchain_core.documents import Document

from clonellm import CloneLLM, LiteLLMEmbeddings, RagVectorStore

# !pip install clonellm[faiss]
# !pip install jq
# !pip install pypdf
# !pip install unstructured


def main() -> None:
    documents: list[Document | str] = [
        Document(page_content=open("about_me.txt", "r").read()),
        open("bio.txt", "r").read(),
    ]
    documents += TextLoader("history.txt").load()
    documents += UnstructuredHTMLLoader("linkedin.html", strategy="fast").load()
    documents += UnstructuredMarkdownLoader("README.md").load()
    documents += PyPDFLoader("my_cv.pdf").load()

    embedding = LiteLLMEmbeddings(model="text-embedding-3-small")
    clone = CloneLLM(model="gpt-4o-mini", documents=documents, embedding=embedding, vector_store=RagVectorStore.FAISS)
    clone.fit()

    new_documents = JSONLoader(file_path="chat.json", jq_schema=".messages[].content", text_content=False).load()
    new_documents += DirectoryLoader("docs/", glob="**/*.md").load()
    clone.update(new_documents)

    # Handle conversation
    ...


if __name__ == "__main__":
    main()

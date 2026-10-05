import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from process_document import process_document

from pathlib import Path

load_dotenv()

api_key = os.getenv("My_API_Key")
embedding_model = os.getenv("My_Embedding_Model")

if not api_key:
    raise ValueError("My_API_Key was not found")

if not embedding_model:
    raise ValueError("My_Embedding_Model was not found")


client = OpenAI(
    api_key=api_key,
    base_url="https://integrate.api.nvidia.com/v1"
)


Current_Dir = Path(__file__).resolve().parent.parent
PDF_PATH = Current_Dir / 'Knowledge_base' / 'test.pdf'
OUTPUT_PATH = Current_Dir / "vector_store/chunks.json"


def create_embedding(text):

    response = client.embeddings.create(
        model=embedding_model,
        input=text
    )

    return response.data[0].embedding


def main():

    print("Processing document...")

    chunks = process_document(PDF_PATH)

    print("Total chunks:", len(chunks))

    embedded_chunks = []

    for index, chunk in enumerate(chunks):

        print(
            f"Embedding chunk {index + 1}/{len(chunks)}..."
        )

        embedding = create_embedding(chunk["text"])

        embedded_chunks.append(
            {
                "id": index,
                "text": chunk["text"],
                "embedding": embedding,
                "metadata": chunk["metadata"]
            }
        )

    os.makedirs("../vector_store", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8")as file:

        json.dump(embedded_chunks, file, ensure_ascii=False)

    print("\nEmbedding pipeline completed!")
    print("Saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
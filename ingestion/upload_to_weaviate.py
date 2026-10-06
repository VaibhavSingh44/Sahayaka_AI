import json
import os

import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth
from pathlib import Path

load_dotenv()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

COLLECTION_NAME = "SahayakaChunks"
Current_Dir = Path(__file__).resolve().parent.parent
CHUNKS_PATH = Current_Dir / "vector_store/chunks.json"

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)

try: 

    with open(CHUNKS_PATH, "r", encoding="utf-8")as file:

        chunks = json.load(file)

    collection = client.collections.get(COLLECTION_NAME)    

    print("Total chunks:", len(chunks))
    print("Starting upload...\n")

    for index, chunk in enumerate(chunks):

        collection.data.insert(
            properties={
                "text": chunk["text"],

                "source": chunk["metadata"]["source"],

                "page": chunk["metadata"]["page"],

                "chunk": chunk["metadata"]["chunk"],
            },

            vector=chunk["embedding"],
        )

        print(
            f"Uploaded {index + 1}/{len(chunks)}"
        )


    print("\nUpload completed successfully.")


finally:

    client.close()

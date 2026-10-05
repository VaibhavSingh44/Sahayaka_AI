import os

import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType


load_dotenv()


WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")


client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
)


COLLECTION_NAME = "SahayakaChunk"


try:

    if client.collections.exists(COLLECTION_NAME):

        print(
            f"Collection '{COLLECTION_NAME}' already exists."
        )

    else:

        client.collections.create(
            name=COLLECTION_NAME,

            vector_config=Configure.Vectors.self_provided(),

            properties=[
                Property(
                    name="text",
                    data_type=DataType.TEXT,
                ),

                Property(
                    name="source",
                    data_type=DataType.TEXT,
                ),

                Property(
                    name="page",
                    data_type=DataType.INT,
                ),

                Property(
                    name="chunk",
                    data_type=DataType.INT,
                ),
            ],
        )

        print(
            f"Collection '{COLLECTION_NAME}' created."
        )

finally:

    client.close()
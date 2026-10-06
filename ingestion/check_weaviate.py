import os

import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth


load_dotenv()


client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
)


try:

    collection = client.collections.get(
        "SahayakaChunk"
    )

    response = collection.aggregate.over_all(
        total_count=True
    )

    print(
        "Objects in SahayakaChunk:",
        response.total_count
    )

finally:

    client.close()
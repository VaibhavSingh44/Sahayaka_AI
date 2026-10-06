import os

import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth


load_dotenv()


client = weaviate.connect_to_weaviate_cloud(
    cluster_url=os.getenv("WEAVIATE_URL"),
    auth_credentials=Auth.api_key(
        os.getenv("WEAVIATE_API_KEY")
    ),
)


try:
    collections = client.collections.list_all()

    print("Collections in Weaviate:")

    for collection in collections:
        print("-", collection)

finally:
    client.close()
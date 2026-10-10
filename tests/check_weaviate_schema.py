import os
import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth,AdditionalConfig,Timeout
from pathlib import Path

curr_lib = Path(__file__).resolve().parent.parent
envpath = curr_lib / ".env"
load_dotenv(dotenv_path=envpath)

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = None

try:
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=Auth.api_key(
            os.getenv("WEAVIATE_API_KEY")
        ),
    )

    collection = client.collections.get("SahayakaChunk")
    config = collection.config.get()

    print("Collection name:", config.name)
    print("Vectorizer:", config.vectorizer_config)
    print("Properties:")

    for prop in config.properties:
        print("-", prop.name, "|", prop.data_type)

except Exception as exc:
    print("Error:", type(exc).__name__, str(exc))

finally:
    if client is not None:
        client.close()
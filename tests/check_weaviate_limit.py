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

    print("Connected:", client.is_connected())

    collections = client.collections.list_all()
    print("Collections:", list(collections.keys()))

    collection = client.collections.get("SahayakaChunk")
    print("Collection ready:", collection is not None)

    try:
        result = collection.aggregate.over_all(total_count=True)
        print("Object count:", result.total_count)
    except Exception as exc:
        print("Count check failed:", type(exc).__name__, str(exc))

except Exception as exc:
    print("Diagnostic error:", type(exc).__name__, str(exc))

finally:
    if client is not None:
        client.close()
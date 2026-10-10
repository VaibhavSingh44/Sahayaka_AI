import os

import weaviate
from dotenv import load_dotenv
from weaviate.classes.init import Auth, AdditionalConfig, Timeout
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
env_path = base_dir / '.env'


load_dotenv(dotenv_path=env_path)


weaviate_url = os.getenv("WEAVIATE_URL")
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

if not weaviate_url or not weaviate_api_key:
    raise ValueError(
        "WEAVIATE_URL or WEAVIATE_API_KEY is missing from .env"
    )

client = None


if not weaviate_url:
    raise ValueError("WEAVIATE_URL was not found")

if not weaviate_api_key:
    raise ValueError("WEAVIATE_API_KEY was not found")


try:
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )

    print("Connected:", client.is_connected())
    print("Ready:", client.is_ready())
    print("Collections:", list(client.collections.list_all().keys()))

except Exception as exc:
    print("Connection test failed:", type(exc).__name__)
    print(str(exc))

finally:
    if client is not None:
        client.close()

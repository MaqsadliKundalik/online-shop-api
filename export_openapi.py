import json
from fastapi.openapi.utils import get_openapi
from app.main import app
import os

def export_openapi():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    )
    with open("api_docs.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    print("OpenAPI schema exported to api_docs.json")

if __name__ == "__main__":
    export_openapi()


import sys
import os
import json

sys.path.append(os.getcwd())

try:
    from app.main import app
    print("Exporting OpenAPI JSON...")
    openapi_data = app.openapi()
    
    output_file = "openapi.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, indent=2)
    
    print(f"Successfully exported OpenAPI JSON to {output_file}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

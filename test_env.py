# test_env.py
import requests
import os
from dotenv import load_dotenv

# Load the clinical environment variables
load_dotenv('.env.clinical')
fhir_url = os.getenv("FHIR_SERVER")
response = requests.get(f"{fhir_url}/Patient?_count=1")
# Print them to verify
print("DB:", os.getenv("DB_URL"))
print("FDA:", os.getenv("OPENFDA_API_KEY"))

print("FHIR Status:", response.status_code)
print("Sample Response:", response.json())
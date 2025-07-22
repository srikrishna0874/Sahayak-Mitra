from google import genai
from google.genai import types
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "sahayak-mitra-798f79e7e5f9.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"])


client = genai.Client(
vertexai=True, project="sahayak-mitra", location="global",credentials=credentials
)

model = "gemini-2.5-flash-lite"

def generate_response(prompt):
    response = client.models.generate_content(
        model=model,
        contents=[
            prompt
        ],
    )
    return response.text

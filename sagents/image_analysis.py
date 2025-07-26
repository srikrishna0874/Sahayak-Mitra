# from sagents.temp import client
# from google.genai import types
# import temp
# dotenv.load_dotenv()
# project_id = os.getenv("PROJECT_ID")
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sahayak-mitra-89f74b79e0e1.json'



# authenticate()
# vertexai.init(project="sahayak-mitra", location="us-central1")

# input_file = "https://storage.googleapis.com/sahayak-mitra/Chat_files/bot/+919883219829/20250726165345.png"

# local_image_path = "temp_image.jpg"

# response = requests.get(input_file)
# with open(local_image_path, "wb") as f:
#     f.write(response.content)

# # Now load from the local file
# source_img = Image.load_from_file(location=local_image_path)
# model = ImageTextModel.from_pretrained("imagetext@001")
# question = "Give me a summary of this image in 3 sentences."

from google import genai
from google.genai import types
from google.oauth2 import service_account
from google.genai.types import GenerateContentConfig, HttpOptions

credentials = service_account.Credentials.from_service_account_file(
    "sahayak-mitra-89f74b79e0e1.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"])


client = genai.Client(
vertexai=True, project="sahayak-mitra", location="global",credentials=credentials
)

model = "gemini-2.5-flash-lite"

IMAGE_URI = "https://storage.googleapis.com/sahayak-mitra/Chat_files/bot/+919883219829/20250726165345.png"
model = "gemini-2.5-flash-lite"

# response = temp.client.models.generate_content(
#   model=model,
#   contents=[
#     "What is shown in this image?",
#     types.Part.from_uri(
#       file_uri=IMAGE_URI,
#       mime_type="image/png",
#     ),
#   ],
# )
# print(response.text, end="")

def generate_image_analysis(image_uri,prompt="What is shown in this image?"):
    response = client.models.generate_content(
    model=model,
    contents=[
            prompt,
            types.Part.from_uri(
                file_uri=image_uri,
                mime_type="image/png",
            ),
        ],
    )
    return response.text



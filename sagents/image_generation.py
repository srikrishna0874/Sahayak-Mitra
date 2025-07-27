# from google.colab import auth
import google.auth
import typing
import vertexai
from vertexai.vision_models import ImageGenerationModel
from google.genai.types import GenerateContentConfig, HttpOptions
from google import genai
from google.genai import types
from google.oauth2 import service_account

from Firebase.firebase_setup import upload_file_to_firebase


def authenticate():
    """Authenticate the user locally."""
    import os
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    
    
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'sahayak-mitra-89f74b79e0e1.json'
    
    
    credentials, project = google.auth.default()
    print(f"Authenticated to project: {project}")

def save_image(image, filename: str = "generated_image.png"):
    """Save the generated image to disk."""
    pil_image = image._pil_image
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")
    pil_image.save(filename)
    print(f"Image saved as: {filename}")

# def display_image(image, max_width: int = 600, max_height: int = 350) -> None:
#     """Display an image with a max size limitation."""
#     pil_image = image._pil_image  # Access PIL Image object
#     if pil_image.mode != "RGB":
#         pil_image = pil_image.convert("RGB")
#     image_width, image_height = pil_image.size
#     if max_width < image_width or max_height < image_height:
#         pil_image = PIL_ImageOps.contain(pil_image, (max_width, max_height))
#     IPython.display.display(pil_image)

def refactorPrompt(prompt: str):

    credentials = service_account.Credentials.from_service_account_file(
    "sahayak-mitra-89f74b79e0e1.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"])


    client = genai.Client(
    vertexai=True, project="sahayak-mitra", location="global",credentials=credentials
    )

    model = "gemini-2.5-flash-lite"

    systemInstructions = """You are a prompt enhancer, you will be given a simple prompt for image genration by a teacher.
    Your task is to give an enhanced prompt for the given prompt. The prompt given by you will be given to "imagen-3.0-generate-002" model to generate image.
    Reply only with the enhanced prompt
    """
    response = client.models.generate_content(
        model=model,
        contents=[
            prompt
        ],
        config=GenerateContentConfig(
        system_instruction= systemInstructions
        ),
    )
    return response.text

    #return updatedPrompt
    
    
def generate_image(prompt: str, number_of_images: int = 1, aspect_ratio: str = "1:1", add_watermark: bool = True,userWaId=None) -> typing.List[str]:
    authenticate()
    print("User prompt: ", prompt)
    prompt = refactorPrompt(prompt)
    print("Enhanced prompt: ", prompt)
    """Generate images using Vertex AI's Image Generation Model."""
    vertexai.init(project="sahayak-mitra", location="us-central1")
    generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    images = generation_model.generate_images(
        prompt=prompt,
        number_of_images=number_of_images,  
        aspect_ratio=aspect_ratio,
        add_watermark=add_watermark,
    )
    # Suppose 'img' is a PIL Image object
    #for ind,image in enumerate(images):
        # print(f"Generated image {ind+1}:")
        # if isinstance(image, PIL_Image.Image):
        #     img_bytes = io.BytesIO()
        #     image.save(img_bytes, format='PNG')
        #     img_bytes.seek(0)
        # else:
        #     # Assume image is already bytes
        #     img_bytes = io.BytesIO(image._image_bytes)
    
    ai_generated_image_link = upload_file_to_firebase("bot", "image/png", images[0]._image_bytes, "png",userWaId=userWaId)
    print("Image uploaded to Firebase Storage:", ai_generated_image_link)
    # save_image(images[0], "generated.png")
    return ai_generated_image_link

# if __name__ == "__main__":
#     authenticate()
#     prompt = "Create a very simple, colorful illustration with large shapes and animals to teach the concept of 'big and small'. Show elephants and mice, trees and flowers, with clear size differences."
#     images = generate_image(prompt)
#     print("Generated image link:", images)
#     # display_image(images[0])
#     #save_image(images[0], "generated.png")



    

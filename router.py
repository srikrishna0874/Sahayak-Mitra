from sagents.temp import generate_response, client, model, systemInstructions
from sagents.image_generation import generate_image
from google.genai.types import GenerateContentConfig

def classify_query(userQuery):
    """
    Uses the Gemini model to decide if the userQuery is requesting image generation or text.
    Returns either 'image' or 'text'.
    """
    classification_prompt = f"""
You are a query classifier for an AI assistant. A user sends the following message:

"{userQuery}"

Decide whether this is a request for:
1. "image" — if the user is asking for any kind of visual, drawing, illustration, or picture.
2. "text" — if the user wants an explanation, story, lesson plan, answer, or any language/text-based response.

Only reply with a single word: "image" or "text".
"""

    response = client.models.generate_content(
        model=model,
        contents=[classification_prompt],
        config=GenerateContentConfig(system_instruction="Classify the query accurately as 'image' or 'text'. Only reply with that one word."),
    )

    classification = response.text.strip().lower()
    return classification


def getResult(userQuery):
    print("Received query:", userQuery)

    classification = classify_query(userQuery)
    print("LLM classified query as:", classification)

    if classification == "image":
        print("Calling image generation agent...")
        images = generate_image(prompt=userQuery)
        return "Image generated successfully and saved as 'generated.png'."
    elif classification == "text":
        print("Calling text generation agent...")
        response = generate_response(userQuery)
        return response
    else:
        print("Unclear classification. Defaulting to text response.")
        return generate_response(userQuery)


# userQuery = "Give me an image to explain the water cycle concept to 5th grade students."
# responseString=getResult(userQuery)
# print(responseString)















# from temp import generate_response


# def getResult(userQuery):
#     # Placeholder for the actual response logic
#     # This function should return a string based on userResponse
#     print("Generating response for:", userQuery)
#     responseString=generate_response(userQuery)
#     print("Generated response:", responseString)
#     return responseString

from sagents.temp import generate_response, client, model, systemInstructions
from sagents.image_generation import generate_image
from google.genai import types
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


def getResult(userQuery,history=None):
    print("Received query:", userQuery)

    classification = classify_query(userQuery)
    print("LLM classified query as:", classification)

    if classification == "image":
        print("Calling image generation agent...")
        images = generate_image(prompt=userQuery)
        return "Image generated successfully and saved as 'generated.png'."
    elif classification == "text":
        print("Calling text generation agent...")
        response = generate_response(userQuery,history)
        return response
    else:
        print("Unclear classification. Defaulting to text response.")
        return generate_response(userQuery,history)
    
    
    
def generate_image_analysis(image_uri,content_type,prompt="What is shown in this image?"):
    
    response = client.models.generate_content(
    model=model,
    contents=[
            prompt,
            types.Part.from_uri(
                file_uri=image_uri,
                mime_type=content_type,
            ),
        ],
    )
    return response.text

# generate_image_analysis("https://storage.googleapis.com/sahayak-mitra/Chat_files/bot/+919883219829/20250726165345.png")
# userQuery = "Convert this story into English"
# history = {
#     "message1": {
#         "message": "Hi, I am kamal",
#         "sender": "Namaste Kamal ji! I am Sahayak. How can I help you today with your teaching in your multi-grade classroom?",
#         "messageType": "text"
#     }
# }

# his = [{'messageType': 'text', 'messageBody': 'Hi, I am kamal', 'sender': 'user'}, 
# {'messageType': 'text', 'messageBody': 'Namaste Kamal ji! I am Sahayak. How can I help you today with your teaching in your multi-grade classroom?', 'sender': 'bot'}, 
# {'messageType': 'text', 'messageBody': 'Give me a story on lion in telugu', 'sender': 'user'},
# {'messageType': 'text', 'messageBody': """Here a simple story about a lion in Telugu for your students:

# ఒక అడవిలో ఒక పెద్ద సింహం ఉండేది. దాని పేరు రాజా. రాజా చాలా బలమైనది మరియు అడవికి రాజు.

# ఒకరోజు, రాజా నీళ్లు తాగడానికి నది దగ్గరకు వెళ్లింది. అక్కడ ఒక చిన్న జింకపిల్ల నీళ్లు తాగుతోంది.

# జింకపిల్ల రాజాను చూసి భయపడింది. కానీ రాజా దానిని చూసి గర్జించలేదు.

# "భయపడకు, చిన్నదానా. నేను నిన్ను ఏమీ చేయను," అని రాజా అంది.

# జింకపిల్ల ఆశ్చర్యపోయింది. సింహం తనతో స్నేహంగా మాట్లాడటం దానికి కొత్త.

# "మీరు ఎందుకు నన్ను తినడం లేదు?" అని జింకపిల్ల అడిగింది.

# "నేను ఎప్పుడూ బలహీనులను బాధించను. అందరం కలిసి ఉంటేనే అడవి బాగుంటుంది," అని రాజా చెప్పింది.

# అప్పటి నుండి, రాజా మరియు జింకపిల్ల మంచి స్నేహితులయ్యారు. అందరూ రాజాను మెచ్చుకున్నారు""", 'sender': 'bot'},
# ]
# # userQuery = "Give me an image to explain the water cycle concept to 5th grade students."
# responseString=getResult(userQuery,his)
# print(responseString)












# from temp import generate_response


# def getResult(userQuery):
#     # Placeholder for the actual response logic
#     # This function should return a string based on userResponse
#     print("Generating response for:", userQuery)
#     responseString=generate_response(userQuery)
#     print("Generated response:", responseString)
#     return responseString
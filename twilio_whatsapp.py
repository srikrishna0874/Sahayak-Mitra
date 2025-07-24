from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse 
from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
from Firebase.firebase_setup import upload_file_to_firebase

import router

load_dotenv()


# todo: Use python-dotenv to load environment variables
# Ensure you have a .env file with the following variables: 
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
client = Client(account_sid, auth_token)

def send_whatsapp_message(to,body):
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        body=body,
        to=f'whatsapp:{to}'
    )
    return message



# send_media_message('+917569105854', ['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80')]
def send_media_message(to, media_url):
    print("Sending media message to:", to)
    print("Media URL:", media_url)
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        media_url=media_url,
        to=f'whatsapp:{to}'
    )
    return message



app=Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the WhatsApp Bot!"

@app.route('/webhook',methods=['POST','GET'])
def reply():
    print("Received a message")
    userResponse=request.values.get('Body') 
    print("User response:", userResponse)
    print("Num media:- ", request.values.get('NumMedia'))
    classification = router.classify_query(userResponse)
    userNumber=request.values.get('From')
    if request.values.get('NumMedia') and int(request.values.get('NumMedia')) > 0:
        print("Received media message")
        media_urls = [request.values.get(f'MediaUrl{i}') for i in range(int(request.values.get('NumMedia')))]
        for i in range(int(request.values.get('NumMedia'))):
            print("Media URL:", request.values.get('MediaUrl'+str(i)))
            content_type= request.values.get('MediaContentType'+str(i), '')
            file_extension = content_type.split('/')[-1]
            media_url = request.values.get('MediaUrl'+str(i))
            response = requests.get(media_url, auth=HTTPBasicAuth(account_sid, auth_token))
            print("content_type:", content_type)
            print("file_extension:", file_extension)
            print("Media URL:", media_url)
            
            if response.status_code == 200:
                firebase_file_link=upload_file_to_firebase("user",content_type, response.content, file_extension, userWaId=request.values.get('From').split(':')[1],userWaId=userNumber)
                
                print("File uploaded successfully")
                send_media_message(userNumber.split(':')[1], [firebase_file_link])
                print("message sent successfully")
                return Response(status=200)
                
            else:
                    
                print("Response failed. Status code:", response.status_code)
            
            
            
        print("Media URLs:", media_urls)
        responseString = "Received media: " + ", ".join(media_urls)
        
    else:
        if classification == "image":
            print("Calling image generation agent...")
            responseString = router.generate_image(prompt=userResponse)
            send_media_message(request.values.get('From').split(':')[1], [responseString])
            responseString = "Image generated successfully and sent to you."
        else:
            responseString=router.getResult(userResponse)
    
    print(request.values)
    
    print(userResponse)
    print(userNumber)    
    response= MessagingResponse()
    print("Response string:", responseString)
    response.message(responseString)
    response.message("This is a test message from Sahayak Mitra.")
    return str(response)


    
    
if __name__ == '__main__':
    # send_whatsapp_message('+917569105854', "Hello! This is a test message from Sahayak Mitra.")
    # port = int(os.environ.get("PORT", 8080))  # Cloud Run uses PORT env variable
    # app.run(host="0.0.0.0", port=port)
    
    
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Run locally on port 5000 for testing
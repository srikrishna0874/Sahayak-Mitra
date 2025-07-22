from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse 
from dotenv import load_dotenv
import os

from router import getResponse

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



app=Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the WhatsApp Bot!"

@app.route('/webhook',methods=['POST','GET'])
def reply():
    print("Received a message")
    userResponse=request.values.get('Body') 
    print("User response:", userResponse)
    responseString=getResponse(userResponse)
    
    print(request.values)
    userNumber=request.values.get('From')
    print(userResponse)
    print(userNumber)    
    response= MessagingResponse()
    response.message(responseString)
    return str(response)
    
    
if __name__ == '__main__':
    # send_whatsapp_message('+917569105854', "Hello! This is a test message from Sahayak Mitra.")
    # port = int(os.environ.get("PORT", 8080))  # Cloud Run uses PORT env variable
    # app.run(host="0.0.0.0", port=port)
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Run locally on port 5000 for testing
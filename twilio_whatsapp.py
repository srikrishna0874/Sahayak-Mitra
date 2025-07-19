from twilio.rest import Client
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse 
from dotenv import load_dotenv
import os

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

@app.route('/webhook',methods=['POST','GET'])
def reply():
    print("Received a message")
    userResponse=request.values.get('Body')
    userNumber=request.values.get('From')
    print(userResponse)
    print(userNumber)
    response= MessagingResponse()
    response.message(f"Hello! You said: {userResponse}")
    return str(response)
    
    
if __name__ == '__main__':
    # send_whatsapp_message('+917569105854', "Hello! This is a test message from Sahayak Mitra.")
    app.run(debug=True,port=5000)

from twilio.rest import Client
from flask import Flask, request

account_sid = 'AC3a58d503e76de9ee36a49fb7c9ba5b0c'
auth_token = '7cdbd52c2ae03e0d3dfce73459762277'
client = Client(account_sid, auth_token)

def send_whatsapp_message(to,body):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to=f'whatsapp:{to}'
    )
    return message



app=Flask(__name__)

@app.route('/sms',methods=['POST','GET'])
def reply():
    print("Received a message")
    userResponse=request.values.get('Body')
    userNumber=request.values.get('From')
    print(userResponse)
    print(userNumber)
    
if __name__ == '__main__':
    app.run()

print(send_whatsapp_message('+917569105854', 'Is it working fine?'))
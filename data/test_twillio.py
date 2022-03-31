# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC69e15f5c9f9516922b62deda108a0716'
auth_token = '8d88652b0ebb6fc423f75d2dd42330bc'
client = Client(account_sid, auth_token)

message = client.messages.create(
                     body="This is Matt saying thanks for being in this group with me",
                     from_='+19562908799',
                     to='+16503828800'
                 )
print(message.sid)

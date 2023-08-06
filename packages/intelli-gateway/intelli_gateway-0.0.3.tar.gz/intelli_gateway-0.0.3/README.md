# Simple Stuff

### Usage
- import library
- create library instance using your email and password
- authenticate client
- make requests

> Unauthenticated requests will fail. Authenticate does not need to be done everytime
> when one wants to make a request, it can be done once and works across all requests.

### Sample Code
```python
from intelli_gateway.gateway_client import GatewayClient

client = GatewayClient("snlv@people.com", "snlv")

# Authenticate Client
client.authenticate()

# Get Account Information
client.account_information()

# Send single sms
client.send_sms(message="Hello Wangu", receiver="263777213388", sender_id="IAS")

# Send bulk sms
client.send_bulk_sms(message="Hello Vakuru", receivers=["263777213388", "263775810157"], sender_id="Tumai")

# Send Email
client.send_email(body="Hi hallo", setting_id="2819bdaa-6035-4e45-9d93-ce5d3724ec52", receiver_email="ngoni.mangudya@intelliafrica.solutions", subject="Testing")




```
import requests
import json
from datetime import datetime


class GatewayClient:
    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password
        self.__host = "http://147.182.201.104:32500/api/v1"
        self.__authenticated = False
        self.axios = requests.Session()
        self.axios.headers.update({"Content-Type": "application/json"})

    def authenticate(self):
        url = f"{self.__host}/users/authenticate/"
        payload = {
            "email": self.__email,
            "password": self.__password,
        }

        try:
            response = self.axios.post(url=url, data=json.dumps(payload))

            if response.status_code == 200:
                print("Authenticated successfully")
                self.__authenticated = True
                data = json.loads(response.text).get('data')
                self.axios.headers.update({
                    "Access-ID": data.get('access_id'),
                    "Access-Key": data.get('access_key')
                })
            else:
                print("Failed to authenticate")
                print("Status Code: ", response.status_code)
                print("Response: ", response.text)
        except Exception as e:
            print("Failed to process request")
            print("Exception: ", e)

    def account_information(self):
        if self.__authenticated:
            try:
                url = f"{self.__host}/users/info/"
                response = self.axios.get(url)

                if response.status_code == 200:
                    print("Response: ", response.text)
                    return response.json()
                else:
                    print("Failed to process request")
                    print("Response: ", response.text)
                    return response.json()
            except Exception as e:
                print("Failed to process request")
                print("Exception: ", e)
        else:
            raise Exception("Client not authenticated")

    def send_sms(self, message: str, receiver: str, sender_id: str = None, scheduled: bool = False,
                 process_at: datetime = None):
        if self.__authenticated:
            try:
                url = f"{self.__host}/messaging/send/"
                payload = {
                    "message": message,
                    "receiver": receiver
                }

                if sender_id is not None:
                    payload["sender_id"] = sender_id

                if scheduled:
                    assert process_at is not None
                    payload["scheduled"] = scheduled
                    payload["process_at"] = process_at

                print("Final Payload: ", payload)

                response = self.axios.post(url, data=json.dumps(payload))

                if response.status_code == 200:
                    print("Message send")
                    return response.json()
                else:
                    print("Failed to process request")
                    print("Response: ", response.text)
                    return response.json()
            except Exception as e:
                print("Failed to process request")
                print("Exception: ", e)
        else:
            raise Exception("Client not authenticated")

    def send_bulk_sms(self, message: str, receivers: list, sender_id: str = None, scheduled: bool = False,
                      process_at: datetime = None):
        if self.__authenticated:

            assert type(receivers) is list
            assert len(receivers) > 0

            try:
                url = f"{self.__host}/messaging/send/bulk/"
                payload = {
                    "message": message,
                    "receivers": list(set(receivers))
                }

                if sender_id is not None:
                    payload["sender_id"] = sender_id

                if scheduled:
                    assert process_at is not None
                    payload["scheduled"] = scheduled
                    payload["process_at"] = process_at

                print("Final Payload: ", payload)

                response = self.axios.post(url, data=json.dumps(payload))

                if response.status_code == 200:
                    print("Message send")
                    return response.json()
                else:
                    print("Failed to process request")
                    print("Response: ", response.text)
                    return response.json()
            except Exception as e:
                print("Failed to process request")
                print("Exception: ", e)
        else:
            raise Exception("Client not authenticated")

    def send_email(self, body: str, setting_id: str, receiver_email: str, subject: str, scheduled: bool = False, process_at: datetime = None):
        if self.__authenticated:
            try:
                url = f"{self.__host}/mailing/email/plain/"

                payload = {
                    "body": body,
                    "setting": setting_id,
                    "receiver": receiver_email,
                    "subject": subject
                }

                if scheduled:
                    assert process_at is not None
                    payload["scheduled"] = scheduled
                    payload["process_at"] = process_at

                response = self.axios.post(url, data=json.dumps(payload))

                if response.status_code == 200:
                    print("Email sent!")
                    return response.json()
                else:
                    print("Failed to process request")
                    print("Response: ", response.text)
                    return response.json()
            except Exception as e:
                print("Failed to process request")
                print("Exception: ", e)
        else:
            raise Exception("Client not authenticated")

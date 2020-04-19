import requests
import json
# from getpass import getpass
import base64
from datetime import datetime
from urllib3 import disable_warnings
from config import myasa
# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
disable_warnings()


class ASA:
    def __init__(self, host, authorization):
        self.host = host
        self.baseauth = f"basic {authorization}"
        self.token = ""
        self.__generate_token()
        self.headers = {'X-Auth-Token': self.token, 'Content-Type': 'application/json'}

    def __generate_token(self):
        url = f"https://{self.host}/api/tokenservices"
        payload = {}
        headers = {'Authorization': self.baseauth}
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        self.token = response.headers['X-Auth-Token']

    def __get_method(self, url):
        url = url
        response = requests.request("GET", url, headers=self.headers, verify=False)
        if 400 <= response.status_code <= 499:
            return f"Failed {json.dumps(response.json())}"
        if 200 <= response.status_code <= 299:
            for item in response.json()["items"]:
                print(item["name"])

    def __post_method(self, url, payload):
        url = url
        payload = payload
        if payload != {}:
            response = requests.request("POST", url, headers=self.headers, data=json.dumps(payload), verify=False)
        else:
            response = requests.request("POST", url, headers=self.headers, data=payload, verify=False)
        if 400 <= response.status_code <= 499:
            return f"Failed {json.dumps(response.json())}"
        if 200 <= response.status_code <= 299:
            return "Success"

    def get_time_range_objects(self):
        print("Getting the Time-Range Objects:")
        url = f"https://{self.host}/api/objects/timeranges"
        print(self.__get_method(url))

    def post_time_range_object(self, time_range_name, start_time, end_time):
        print("Posting new object:", time_range_name)
        url = f"https://{self.host}/api/objects/timeranges"
        payload = {
            "kind": "object#TimeRange",
            "name": time_range_name,
            "value": {
                "start": str(start_time),
                "end": str(end_time),
                "periodic": []
                }
            }
        print(self.__post_method(url, payload))

    def save_config(self):
        print("saving the config")
        url = f"https://{self.host}/api/commands/writemem"
        payload = {}
        print(self.__post_method(url, payload))


def encode_username_password(username, password):
    auth_string = f"{username}:{password}"
    message_bytes = auth_string.encode()
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode()
    return base64_message


def main(*args, **kwargs):
    authorization = encode_username_password(args[0]['username'], args[0]['password'])
    asa5506 = ASA(args[0]['host'], authorization)
    print("Token:", asa5506.token)
    asa5506.get_time_range_objects()
    asa5506.post_time_range_object("teszt4", kwargs['start'], kwargs['end'])
    asa5506.save_config()


if __name__ == '__main__':
    # username = input("Enter your username: ")
    # password = getpass("Enter your password: ")
    start = datetime.now()
    end = datetime(2020, 4, 25, 11, 22)
    start = f"{start.hour}:{start.minute} {start.strftime('%B')} {start.day} {start.year}"
    end = f"{end.hour}:{end.minute} {end.strftime('%B')} {end.day} {end.year}"
    main(myasa, start=start, end=end)

import os
import requests

from json import JSONDecodeError

from firebase_admin import credentials

from google.cloud.firestore_v1 import DocumentReference
from account.account_generator import Account
from bots.notify_bot import send_message_attempts
from serializers import ConstraintsSerializer

CURRENT_FILE_LOCATION = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(os.path.join(CURRENT_FILE_LOCATION, "antycode-3f8e262dd0a7.json"))


def create_account(
        serialized_data,
        sms_api_code,
) -> Account:
    account = Account(
        gender=serialized_data.get("gender"),
        locale=serialized_data.get("locale"),
        years=serialized_data.get("years"),
        proxy_type=serialized_data.get("proxy_type"),
        proxy_host=serialized_data.get("proxy_host"),
        proxy_port=serialized_data.get("proxy_port"),
        proxy_user=serialized_data.get("proxy_user"),
        proxy_pass=serialized_data.get("proxy_pass"),
        proxy_refresh=serialized_data.get("proxy_refresh"),
        sms_api_code=sms_api_code,
    )

    return account


def push_account_data_to_api(account_data):
    try:
        response = requests.post("http://127.0.0.1:8000/store_json/", json=account_data)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to push account data to API. Error: {e}")


def create_json(doc_ref: DocumentReference, constraints: dict, current_worker_id: int) -> None:
    serializer = ConstraintsSerializer()
    serialized_data = serializer.serialize(constraints)
    current_worker_id = current_worker_id
    sms_api_code = serialized_data.get("sms_api_code")

    account = None

    account_creation_error = None
    tries = 5

    while not account and tries > 0:
        try:
            account = create_account(
                serialized_data=serialized_data,
                sms_api_code=sms_api_code,
            )
        except JSONDecodeError as e:
            print("JSON error, probably wrong data in certain field", e)

        tries -= 1
        if tries == 0:
            account_creation_error = "error"
            send_message_attempts(msg="Account creation error")

    new_doc_data = None
    try:
        new_doc_data = {
            "id": doc_ref.id,
            "gender": account.gender,
            "first_name": account.first_name,
            "last_name": account.last_name,
            "login": account.login,
            "password": account.password,
            "status": "",
            "proxy_type": account.proxy_type,
            "proxy_host": account.proxy_host,
            "proxy_user": account.proxy_user,
            "proxy_port": account.proxy_port,
            "proxy_pass": account.proxy_pass,
            "proxy_refresh": account.proxy_refresh,
            "phone": "",
            "cookies": account.cookies,
            "sms_api_code": account.sms_api_code,
            "worker_id": f"{current_worker_id}"
        }
    except Exception as e:
        send_message_attempts(msg=e)

    if new_doc_data:
        print("result:", new_doc_data)
        push_account_data_to_api(new_doc_data)

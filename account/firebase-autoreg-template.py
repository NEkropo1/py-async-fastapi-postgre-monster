from typing import Tuple

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def start_app() -> Tuple[firestore.client, dict]:
    cred = credentials.Certificate("creds.json")
    firebase_admin.initialize_app(cred)

    # Get a reference to the Firestore database
    db = firestore.client()

    new_doc_ref_1 = db.collection("accounts").add({})
    new_doc_ref_1_id = new_doc_ref_1[1]
    new_doc_ref_2 = db.collection("accounts").add({})
    new_doc_ref_2_id = new_doc_ref_2[1]

    # Define the document data
    data = {
        "constraints": {
            "gender": "female",  # "male", "female
            "years": [1995, 2003],  # years constraints, minimum_date - maximum_date
            "handle_captcha_key": "9f0dfe8b5869f40a0fc854494db8d203",  # captcha token for handling captcha (won't be in future)
            "locale": "ru_RU",  # "en_US", "ru_RU" - chose language for account credentials
            "sms_api_code": "88cf33cA49847b1fc7b6fd2e451be316",
            "proxy_host": "connect-ua.z-proxy.com",
            "proxy_port": "7957",
            "proxy_type": "http",
            "proxy_user": "z_e2ku1gfh",
            "proxy_pass": "rds69vj0r7",
            "proxy_refresh": "https://z-proxy.com/r/?h=5m1kqo",
        },
        "count": 2,  # how many accounts should be registered, used for result, where we will iterate on some certain id
        "status": "not_done",  # "not_done" , "in_work", "done" - for understanding if worker should work on task
        "type": "register",  # currently only "register" - flag for autoreg

        "result": [
            new_doc_ref_1_id,
            new_doc_ref_2_id,
        ],
    }
    return db, data


data_2 = {
    "constraints": {
        "years": [1990, 2001],  # years constraints, minimum_data - maximum_date
        "locale": "en_US",  # "en_US", "ru_RU" - chose language for account credentials
        "sms_api_code": "88cf33cA49847b1fc7b6fd2e451be316",
        "proxy_host": "connect-ua.z-proxy.com",
        "proxy_port": "7666",
        "proxy_type": "http",
        "proxy_user": "z_91s_3tuy",
        "proxy_pass": "mszd7yv1dt",
        "proxy_refresh": "https://z-proxy.com/r/?hash=br7o99",
    },
    "count": 1,  # how many accounts should be registered, used for result, where we will iterate on some certain id
}

data_3 = {
    "constraints": {
        "locale": "en_US",  # "en_US", "ru_RU" - chose language for account credentials
        "proxy_host": "connect-ua.z-proxy.com",
        "proxy_port": "7496",
        "proxy_type": "http",
        "proxy_user": "z_cva8_xr7",
        "proxy_pass": "z66lfba8o5",
        "proxy_refresh": "https://z-proxy.com/r/?hash=qi8pyi",
    },
    "count": 1,  # how many accounts should be registered
}

data_4 = {
    "constraints": {
        "image": "gs://fb-autoreg-test-002.appspot.com/photo_2023-05-18_23-00-49.jpg",
        "locale": "en_US",  # "en_US", "ru_RU" - chose language for account credentials
        "proxy_host": "connect-ua.z-proxy.com",
        "proxy_port": "7590",
        "proxy_type": "http",
        "proxy_user": "z_8gvwsezz",
        "proxy_pass": "rc36v69iuo",
        "proxy_refresh": "https://z-proxy.com/r/?hash=5v1wh3",
    },
    "count": 2,  # how many accounts should be registered
}


def send_facebook_profile(db, profile_name: str = None, data: dict = None, data_2: dict = None) -> None:
    if data_2:
        data.update(data_2)
    doc_ref = db.collection("tasks").document(profile_name)
    doc_ref.set(data, merge=True)
    print(f"Document created with ID: {doc_ref.id}")


if __name__ == "__main__":
    # All you need is change needed data in templates to work with
    db, data = start_app()
    send_facebook_profile(db, "Json for Facebook create test 1", data)
    send_facebook_profile(db, "Json for Facebook create test 2", data, data_2)
    send_facebook_profile(db, "Json for Facebook create test 3", data, data_3)
    send_facebook_profile(db, "Json for Facebook create test 4", data, data_4)
    send_facebook_profile(db, "Json for Facebook create test 5", data, data_4)
    send_facebook_profile(db, "Json for Facebook create test 6", data, data_3)
    send_facebook_profile(db, "Json for Facebook create test 7", data, data_2)

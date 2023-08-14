from abc import ABC, abstractmethod


class Serializer(ABC):
    @abstractmethod
    def serialize(*args, **kwargs):
        ...


class ConstraintsSerializer:
    @staticmethod
    def serialize(constraints: dict) -> dict:
        result = {}
        keys = [
            "gender", "locale", "years", "proxy_host",
            "proxy_refresh", "proxy_pass", "proxy_port",
            "proxy_user", "proxy_type",
            "sms_api_code", "proxies"
        ]

        for key in keys:
            result[key] = constraints.get(key)

        print("Constratints serializer debug result: ", result)  # DEBUG
        return result

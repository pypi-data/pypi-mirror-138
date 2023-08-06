import json
import random
import string

from .util import c, s, uu

uid = None
sid = None
deviceId = None
lang = None
new = False


class Headers:
    def __init__(self, data=None):
        if deviceId: self.deviceId = deviceId
        else: self.deviceId = c()

        self.headers = {
            "NDCDEVICEID": self.deviceId,
            "AUID": uu(),
            "SMDEVICEID": uu(),
            "Content-Type": "application/json; charset=utf-8",
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Upgrade"
        }
        self.web_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ar,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            "x-requested-with": "xmlhttprequest"
        }

        if sid:
            self.headers["NDCAUTH"] = sid
            self.web_headers["cookie"] = sid

        if uid:
            self.uid = uid

        if data:
            self.headers["Content-Length"] = str(len(data))
            if type(data) is not str: data = json.dumps(data)
            self.headers["NDC-MSG-SIG"] = s(data)

        if lang:
            self.headers.update({"NDCLANG": lang[:lang.index("-")], "Accept-Language": lang})

        if new:
            self.headers["NDCDEVICEID"] = c("".join(random.choices(string.ascii_lowercase, k=12)).encode())
            del self.headers["SMDEVICEID"]
            del self.headers["AUID"]


class AdHeaders:
    def __init__(self, userId: str = None):
        self.data = {
            "reward": {
                "ad_unit_id": "t00_tapjoy_android_master_checkinwallet_rewardedvideo_322",
                "credentials_type": "publisher",
                "custom_json": {
                    "hashed_user_id": userId
                },
                "demand_type": "sdk_bidding",
                "event_id": uu(),
                "network": "tapjoy",
                "placement_tag": "default",
                "reward_name": "Amino Coin",
                "reward_valid": True,
                "reward_value": 2,
                "shared_id": "4d7cc3d9-8c8a-4036-965c-60c091e90e7b",
                "version_id": "1569147951493",
                "waterfall_id": "4d7cc3d9-8c8a-4036-965c-60c091e90e7b"
            },
            "app": {
                "bundle_id": "com.narvii.amino.master",
                "current_orientation": "portrait",
                "release_version": "3.4.33585",
                "user_agent": "Dalvik\/2.1.0 (Linux; U; Android 10; G8231 Build\/41.2.A.0.219; com.narvii.amino.master\/3.4.33567)"
            },
            "device_user": {
                "country": "US",
                "device": {
                    "architecture": "aarch64",
                    "carrier": {
                        "country_code": 255,
                        "name": "Vodafone",
                        "network_code": 0
                    },
                    "is_phone": True,
                    "model": "GT-S5360",
                    "model_type": "Samsung",
                    "operating_system": "android",
                    "operating_system_version": "29",
                    "screen_size": {
                        "height": 2300,
                        "resolution": 2.625,
                        "width": 1080
                    }
                },
                "do_not_track": False,
                "idfa": "0c26b7c3-4801-4815-a155-50e0e6c27eeb",
                "ip_address": "",
                "locale": "ru",
                "timezone": {
                    "location": "Asia\/Seoul",
                    "offset": "GMT+02:00"
                },
                "volume_enabled": True
            },
            "session_id": "7fe1956a-6184-4b59-8682-04ff31e24bc0",
            "date_created": 1633283996
        }
        self.headers = {
            "cookies": "__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096",
            "authorization": "Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA==",
            "X-Tapdaq-SDK-Version": "android-sdk_7.1.1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 9 Pro Build/QQ3A.200805.001; com.narvii.amino.master/3.4.33585)"
        }

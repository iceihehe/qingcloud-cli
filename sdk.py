import base64
import datetime
import hmac
import json
import random
import time
import urllib.parse
import hashlib
import uuid

import requests

from error import LoadConfigError
from util import load_config


_AUTH_KEY = "access_key_id"
_AUTH_SECRET = "secret_access_key"


class QingCloudApi:

    def __init__(self):
        self.host = "https://api.qingcloud.com"
        self.access_key_id = ""
        self.secret_access_key = ""
        self.signature_method = "HmacSHA256"
        self.version = 1
        self.signature_version = 1
        self._load_config()

    def _load_config(self):
        config = load_config()
        if not config or not config.get(_AUTH_KEY) or not config.get(_AUTH_SECRET):
            raise LoadConfigError("请先配置access_key_id和secret_access_key")
        self.access_key_id = config[_AUTH_KEY]
        self.secret_access_key = config[_AUTH_SECRET]

    @staticmethod
    def _gen_timestamp():
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _clear_none_value(params):
        res = {}
        for k, v in params.items():
            if v is None:
                continue
            res[k] = v
        return res

    @staticmethod
    def _gen_signature(secret_access_key, params, method, uri):
        querystring = "&".join([f"{k}={urllib.parse.quote_plus(str(params[k]))}" for k in sorted(params.keys())])
        string_to_sign = method + "\n" + uri + "\n" + querystring
        h = hmac.new(secret_access_key.encode(), digestmod=hashlib.sha256)
        h.update(string_to_sign.encode())
        sign = base64.b64encode(h.digest()).strip()
        signature = urllib.parse.quote_plus(sign)
        return signature

    def _request(self, method, uri, params, try_times=1):

        params = self._clear_none_value(params)
        signature = self._gen_signature(self.secret_access_key, params, "GET", f"{uri}")
        params.update({
            "signature": signature,
        })
        if method == "GET":
            querystring = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{self.host}{uri}?{querystring}"
            while try_times:
                try:
                    resp = requests.get(url)
                except Exception:
                    try_times -= 1
                    if try_times == 0:
                        raise
                    time.sleep(random.random() * (2 ** try_times))
                else:
                    return resp.text

        if method == "POST":
            pass

    def run_instances(self, image_id, login_mode, zone, instance_type=None, login_keypair=None, login_passwd=None, cpu=None, memory=None):

        params = {
            "access_key_id": self.access_key_id,
            "version": self.version,
            "signature_version": self.signature_version,
            "signature_method": self.signature_method,
            "action": "RunInstances",
            "time_stamp": self._gen_timestamp(),
            "image_id": image_id,
            "login_mode": login_mode,
            "zone": zone,
            "instance_type": instance_type,
            "login_keypair": login_keypair,
            "login_passwd": login_passwd,
            "cpu": cpu,
            "memory": memory,
        }
        resp = self._request("GET", "/iaas/", params)

        return resp

    def describe_instances(self, zone, instances__n=None, instance_class=None):

        params = {
            "access_key_id": self.access_key_id,
            "version": self.version,
            "signature_version": self.signature_version,
            "signature_method": self.signature_method,
            "action": "DescribeInstances",
            "time_stamp": self._gen_timestamp(),
            "zone": zone,
            "instance_class": instance_class,
        }
        params.update(self._dot_n("instances", instances__n))
        resp = self._request("GET", "/iaas/", params)

        return resp

    def terminate_instances(self, zone, instances__n=None, direct_cease=None):
        params = {
            "access_key_id": self.access_key_id,
            "version": self.version,
            "signature_version": self.signature_version,
            "signature_method": self.signature_method,
            "action": "TerminateInstances",
            "time_stamp": self._gen_timestamp(),
            "zone": zone,
            "direct_cease": direct_cease,
        }
        params.update(self._dot_n("instances", instances__n))
        resp = self._request("GET", "/iaas/", params)

        return resp

    @staticmethod
    def _dot_n(key, value):
        res = {}
        if not value:
            return {}
        i = 1
        for v in value:
            res[f"{key}.{i}"] = v
        return res

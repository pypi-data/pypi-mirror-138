import os

import redis
from pymongo import MongoClient


class MyApp:

    def __init__(self,
            app_config=None,
            proxy_config=None,
            redis_connect: redis.Redis = None,
            set_app_error=None,
            set_max_running_times=None,
            get_max_running_times=None,
            get_running_times=None,
            set_healthy_tolerance_second=None,
            get_healthy_tolerance_second=None,
            update_healthy_time=None,
            read_yaml=None,
            mongo_client=None
    ):
        self._app_config = app_config
        self._proxy_config = proxy_config
        self._redis_connect = redis_connect
        self._set_app_error = set_app_error
        self._set_max_running_times = set_max_running_times
        self._get_max_running_times = get_max_running_times
        self._get_running_times = get_running_times
        self._set_healthy_tolerance_second = set_healthy_tolerance_second
        self._get_healthy_tolerance_second = get_healthy_tolerance_second
        self._update_healthy_time = update_healthy_time
        self._read_yaml = read_yaml
        self._mongo_client = mongo_client

    ############################################################

    @property
    def app_config(self):
        return self._app_config

    @property
    def proxy_config(self):
        return self._proxy_config

    @property
    def redis_connect(self) -> redis.Redis:
        return self._redis_connect

    @property
    def set_app_error(self):
        return self._set_app_error

    @property
    def set_max_running_times(self):
        return self._set_max_running_times

    @property
    def get_max_running_times(self):
        return self._get_max_running_times

    @property
    def get_running_times(self):
        return self._get_running_times

    @property
    def set_healthy_tolerance_second(self):
        return self._set_healthy_tolerance_second

    @property
    def get_healthy_tolerance_second(self):
        return self._get_healthy_tolerance_second

    @property
    def update_healthy_time(self):
        return self._update_healthy_time

    @property
    def read_yaml(self):
        return self._read_yaml

    @property
    def mongo_client(self) -> MongoClient:
        return self._mongo_client

    ############################################################

    @property
    def proxies(self):
        if self._proxy_config is None:
            return {}

        host = self._proxy_config['host']
        port = self._proxy_config['port']

        return {
            "http": f"http://{host}:{port}",
            "https": f"http://{host}:{port}"
        }

    @property
    def socks5_proxies(self):
        if self._proxy_config is None:
            return {}

        host = self._proxy_config['socks5host']
        port = self._proxy_config['socks5port']

        return {
            "http": f"socks5h://{host}:{port}",
            "https": f"socks5h://{host}:{port}"
        }

    @property
    def is_debug(self) -> bool:
        dbg = os.getenv('DEBUG')
        if dbg is None:
            return False

        return len(dbg) > 0

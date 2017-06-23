import threading

import pyeureka.client as client


class SimpleEurekaClientWrapper:
    def __init__(self, eureka_url):
        self.client = client.EurekaClient(eureka_url)

    def app(self, app_name):
        return self.client.query(app=app_name)

    def instance(self, instance, app_name=None):
        return self.client.query(app=app_name, instance=instance)


class SimpleEurekaServiceWrapper:
    def __init__(self, eureka_url, instance_definition, heartbeat_interval):
        self.client = client.EurekaClient(eureka_url, instance_definition)
        self.heartbeat_interval = heartbeat_interval

    def run(self):
        self.client.register()
        self.timer = threading.Timer(self.heartbeat_interval, self._interval)
        self.timer.start()

    def _interval(self):
        self.client.heartbeat()
        self.timer = threading.Timer(self.heartbeat_interval, self._interval)
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        self.client.deregister()

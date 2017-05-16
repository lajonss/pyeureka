import eureka_client as client

class SimpleEurekaClientWrapper:
    def __init__(self, eureka_url):
        self.client = client.EurekaClient(eureka_url)
    def app(self, app_name):
        return self.client.query(app=app_name)
    def instance(self, instance, app_name=None):
        return self.client.query(app=app_name, instance=instance)

class SimpleEurekaServiceWrapper:
    pass

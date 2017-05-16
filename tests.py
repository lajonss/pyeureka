import pyeureka

app = 'pyeureka-test'
eureka_url = 'http://localhost:8765'
heartbeat = 5.0
instance = {
    'ipAddr': '127.0.0.1',
    'app': app
}

print("Eureka address: {}".format(eureka_url))
print("Service definition")
print(instance)
service_wrapper = pyeureka.SimpleEurekaServiceWrapper(
    eureka_url, instance, heartbeat)

print("Registering service")
service_wrapper.run()

print("Creating client")
client_wrapper = pyeureka.SimpleEurekaClientWrapper(eureka_url)

print("Fetching app data")
print(client_wrapper.app(app))

print("Stopping service")
service_wrapper.stop()

print("Done.")

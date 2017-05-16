import pyeureka

app = 'pyeureka-test'
eureka_url = 'http://localhost:8765'
heartbeat = 5.0
instance = {
    'ipAddr': '127.0.0.1',
    'app': app
}

print("[II] Eureka address: {}".format(eureka_url))
print("[II] Service definition")
print(instance)
service_wrapper = pyeureka.SimpleEurekaServiceWrapper(
    eureka_url, instance, heartbeat)

print("[II] Registering service")
service_wrapper.run()

print("[II] Creating client")
client_wrapper = pyeureka.SimpleEurekaClientWrapper(eureka_url)

print("[II] Fetching app data")
app_data = client_wrapper.app(app)
print(app_data)

print("[II] Interpreting app data")
print("[II] Client should connect to: {}".format(
    app_data['application']['instance'][0]['ipAddr']))

print("[II] Stopping service")
service_wrapper.stop()

print("[II] Done.")

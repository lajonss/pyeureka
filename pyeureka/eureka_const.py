import requests

EUREKA_DEFAULT_SAME_AS = 1
EUREKA_DEFAULT_VALUE = 2

EUREKA_INSTANCE_DEFINITION = {
    'needed': [
        'ipAddr', 'app'
    ],
    'needed-with-default': [
        ('hostName', EUREKA_DEFAULT_SAME_AS, 'ipAddr'),
        ('port', EUREKA_DEFAULT_VALUE, {
            '$': 80,
            '@enabled': 'false'
        }),
        ('securePort', EUREKA_DEFAULT_VALUE, {
            '$': 443,
            '@enabled': 'false'
        }),
        ('dataCenterInfo', EUREKA_DEFAULT_VALUE, {
            'name': 'MyOwn',
            '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo'
        }),
        ('homePageUrl', EUREKA_DEFAULT_SAME_AS, 'ipAddr'),
        ('healthCheckUrl', EUREKA_DEFAULT_SAME_AS, 'ipAddr')
    ],
    'transformations': [
        ('port', lambda p: is_number(p), lambda p: {
         '$': int(p), '@enabled': 'true'}),
        ('securePort', lambda p: is_number(p),
         lambda p: {'$': int(p), '@enabled': 'true'}),
    ]
}

EUREKA_HEADERS = {
    'POST': {'Content-Type': 'application/json'},
    'PUT': {},
    'GET': {'Accept': 'application/json'},
    'DELETE': {}
}

EUREKA_REQUESTS = {
    'POST': requests.post,
    'PUT': requests.put,
    'GET': requests.get,
    'DELETE': requests.delete
}


def is_number(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False

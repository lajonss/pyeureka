import time

import requests

import pyeureka.validator as validator
import pyeureka.const as c


def get_timestamp():
    return int(time.time())


class EurekaClientError(Exception):
    pass


class EurekaInstanceDoesNotExistException(Exception):
    pass


class EurekaClient:

    def __init__(self, eureka_url, instance_definition=None, verbose=False):
        """
        eureka_url is the address to send requests to.
        instance_definition is description of service
            NOT conforming (as of 16.05.17) to schema available in
            https://github.com/Netflix/eureka/wiki/Eureka-REST-operations
        Basic operations:
        service side:
            client = EurekaClient('localhost:8765', {'ipAddr': '127.0.0.1', 'port': 80, 'app': 'myapp'})
            client.register()
            client.heartbeat()
        client side:
            client = EurekaClient('localhost:8765')
            try:
                client.query(app='myapp')
            except EurekaClientError:
                print('operation failed')
        """
        self.eureka_url = eureka_url
        if instance_definition is not None:
            self.instance_definition = validator.validate_instance_definition(
                instance_definition)
            self.app_id = self.instance_definition['instance']['app']
            self.instance_id = self.instance_definition[
                'instance']['instanceId']
        self.verbose = verbose
        if verbose:
            print("EurekaClient running with verbosity enabled")
            print("instance_definition: {}".format(self.instance_definition))

    def register(self):
        request_uri = self.eureka_url + '/eureka/apps/' + self.app_id
        self._request('POST', request_uri, 'registration',
                      204, payload=self.instance_definition)

    def deregister(self):
        self._request('DELETE', comment='deregistration')

    def heartbeat(self):
        request_uri = self._instance_uri() + '?status=UP&lastDirtyTimestamp=' + \
            str(get_timestamp())
        self._request('PUT', uri=request_uri, comment='heartbeat',
                      errors={404: EurekaInstanceDoesNotExistException})

    def query(self, app=None, instance=None):
        request_uri = self.eureka_url + '/eureka/apps/'
        if app is not None:
            request_uri += app
            if instance is not None:
                request_uri += '/' + instance
        elif instance is not None:
            request_uri = self.eureka_url + '/eureka/instances/' + instance
        request = self._request('GET', request_uri, 'query')
        return request.json()

    def query_vip(self, vip):
        request_uri = self.eureka_url + '/eureka/vips/' + vip
        request = self._request('GET', request_uri, 'query vip')
        return request

    def query_svip(self, svip):
        request_uri = self.eureka_url + '/eureka/svips/' + svip
        request = self._request('GET', request_uri, 'query svip')
        return request

    def take_instance_out_of_service(self):
        request_uri = self._instance_uri() + '/status?value=OUT_OF_SERVICE'
        self._request('PUT', request_uri, 'out of service')

    def put_instance_back_into_service(self):
        request_uri = self._instance_uri() + '/status?value=UP'
        self._request('PUT', request_uri, 'up')

    def update_metadata(self, key, value):
        request_uri = self._instance_uri() + \
            '/metadata?{}={}'.format(key, value)
        self._request('PUT', request_uri, 'update_metadata')

    def _instance_uri(self):
        return self.eureka_url + '/eureka/apps/' + self.app_id + '/' + self.instance_id

    def _fail_code(self, code, request, comment, errors=None):
        if self.verbose:
            self._show_request(request, comment)
        if request.status_code != code:
            error = EurekaClientError
            if errors is not None and request.status_code in errors:
                error = errors[request.status_code]
            raise error({'request': request, 'comment': comment,
                         'status_code': request.status_code})

    def _show_request(self, request, comment):
        print("{}:".format(comment))
        print("Request code: {}".format(request.status_code))
        print("Request headers: {}".format(request.headers))
        print("Request response: {}".format(request.text))

    def _request(self, method, uri=None, comment='operation', accepted_code=200, errors=None, payload=None):
        if uri is None:
            uri = self._instance_uri()
        request = c.EUREKA_REQUESTS[method](
            uri, headers=c.EUREKA_HEADERS[method], json=payload)
        self._fail_code(accepted_code, request, comment, errors=errors)
        return request

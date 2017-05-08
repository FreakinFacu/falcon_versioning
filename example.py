import json
from wsgiref import simple_server

import falcon

from falcon_versioning import InvalidVersionError
from falcon_versioning import VersionedRouter

VERSION_1_0 = "1.0"
VERSION_1_1A = "1.1a"
VERSION_1_1B = "1.1b"


class SimpleResource(object):
    def __init__(self, message):
        self.message = message

    def on_get(self, req, resp):
        requested_version = req.context['requested_version'] if 'requested_version' in req.context else "None"
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"Message": self.message, "Requested_version": requested_version})


def handle_invalid_version_error(ex: InvalidVersionError, req, resp, params):
    raise falcon.HTTPError(falcon.HTTP_400, "Invalid API Version '%s'" % ex.invalid_version)


def initialize_app():
    # Initialize Router
    router = VersionedRouter()

    # Define your available versions
    router.add_version(VERSION_1_0, is_default=True)
    router.add_version(VERSION_1_1A, parent_version=VERSION_1_0)
    router.add_version(VERSION_1_1B, parent_version=VERSION_1_0)

    # Versioned router must be passed as a middleware and router for it to function correctly. See README.
    app = falcon.API(
        middleware=[router],
        router=router
    )

    # Add custom handler for InvalidVersionError
    app.add_error_handler(InvalidVersionError, handle_invalid_version_error)

    # Initialize v1.0
    app.add_route('/things', SimpleResource("Things in 1.0"), version=VERSION_1_0)
    app.add_route('/stuff', SimpleResource("Stuff in 1.0"), version=VERSION_1_0)

    # Initialize v1.1a
    app.add_route('/things', SimpleResource("Things in 1.1a"), version=VERSION_1_1A)
    # Endpoint /stuff will be available in 1.1a since it's parent version defines it

    # Initialize v1.1b
    app.add_route('/stuff', SimpleResource("Stuff in 1.1b"), version=VERSION_1_1B)
    # Endpoint /things will be available in 1.1b since it's parent version defines it

    return app

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, initialize_app())
    httpd.serve_forever()

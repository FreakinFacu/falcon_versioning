from falcon.routing.compiled import CompiledRouter

from falcon_versioning.invalid_version_error import InvalidVersionError
from falcon_versioning.version_parsers import parse_api_version_header


class VersionedRouter:
    # Picking something that's not a valid character in the uri path
    # https://tools.ietf.org/html/rfc3986#section-3.3
    SEPARATOR = "<>"

    def __init__(self, parse_version=None):
        self.versions = {}
        self.parent_versions = {}
        self.default_version = None
        self.parse_version = parse_version or parse_api_version_header
        
    ###
    # Router Methods
    # http://falcon.readthedocs.io/en/stable/api/routing.html
    ###
    def add_route(self, uri_template, method_map, resource, version):
        self._validate_version(version)
        self.versions[version].add_route(uri_template, method_map, resource)

    def find(self, uri):
        version, uri = uri.split(VersionedRouter.SEPARATOR)
        return self._versioned_find_helper(version, uri)

    ###
    # Middleware Methods
    # http://falcon.readthedocs.io/en/stable/api/middleware.html
    ###
    def process_request(self, req, resp):
        # Get the version. Validate that its a valid if found
        # Alter the req.path to include it

        version = self.parse_version(req)
        if version is not None:
            self._validate_version(version)
            req.context['requested_version'] = version
        else:
            version = self.default_version

        req.path = version + VersionedRouter.SEPARATOR + req.path

    ###
    # Public methods
    ###
    def add_version(self, version, parent_version=None, is_default=None):
        self.versions[version] = CompiledRouter()

        if parent_version is not None:
            self._validate_version(parent_version)

            self.parent_versions[version] = parent_version

        if is_default is not None and is_default:
            if self.default_version is not None:
                raise ValueError("Cannot define more than one version as default")
            self.default_version = version

    ###
    # Private methods
    ###
    def _validate_version(self, version):
        if version not in self.versions:
            raise InvalidVersionError(version)

    def _versioned_find_helper(self, version, uri):
        resource_info = self.versions[version].find(uri)

        # If we already found it return it
        if resource_info is not None:
            return resource_info

        # If version has a parent defined then look for the resource there
        if version in self.parent_versions:
            return self._versioned_find_helper(self.parent_versions[version], uri)
        else:
            return None

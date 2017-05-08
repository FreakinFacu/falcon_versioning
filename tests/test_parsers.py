from unittest import TestCase
from unittest.mock import Mock

from falcon_versioning.version_parsers import parse_accept_header
from falcon_versioning.version_parsers import parse_api_version_header


class TestApiVersionHeaderParser(TestCase):
    def test_valid(self):
        # Create a mock request and add the api_version header
        req = Mock()
        req.headers = {'API-VERSION': '1.0'}

        self.assertEqual(parse_api_version_header(req), '1.0')

    def test_none(self):
        # Create mock request and don't pass any headers through
        req = Mock()
        req.headers = {}
        self.assertIsNone(parse_api_version_header(req))


class TestAcceptHeaderParser(TestCase):
    def test_valid(self):
        req = Mock()
        req.headers = {'ACCEPT': 'application/json;version=1.0'}

        self.assertEqual(parse_accept_header(req), '1.0')

    def test_order(self):
        req = Mock()
        req.headers = {'ACCEPT': 'version=1.0;application/json'}

        self.assertEqual(parse_accept_header(req), '1.0')

    def test_short(self):
        req = Mock()
        req.headers = {'ACCEPT': 'version=1.0'}

        self.assertEqual(parse_accept_header(req), '1.0')

    def test_none(self):
        # Create mock request and don't pass any headers through
        req = Mock()
        req.headers = {}
        self.assertIsNone(parse_accept_header(req))

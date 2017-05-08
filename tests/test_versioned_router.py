from falcon_versioning import InvalidVersionError
from falcon_versioning import VersionedRouter

from unittest import TestCase


class TestVersionedRouter(TestCase):
    def test_init(self):
        router = VersionedRouter()
        router.add_version("1.0", is_default=True)
        router.add_version("1.1", parent_version="1.0")

    def test_invalid_parent(self):
        router = VersionedRouter()
        self.assertRaises(InvalidVersionError, router.add_version, "1.1", parent_version="1.0")

    def test_multiple_defaults(self):
        router = VersionedRouter()
        router.add_version("1.0", is_default=True)
        self.assertRaises(ValueError, router.add_version, "1.1", is_default=True)

from falcon import testing

from example import initialize_app


class TestExample(testing.TestCase):
    def setUp(self):
        super(TestExample, self).setUp()
        self.app = initialize_app()

    def test_gets(self):
        result = self.simulate_get('/things')
        self.assertEquals({'Requested_version': 'None', 'Message': 'Things in 1.0'}, result.json)

        result = self.simulate_get('/stuff')
        self.assertEquals({'Requested_version': 'None', 'Message': 'Stuff in 1.0'}, result.json)

        result = self.simulate_get('/things', headers={"API-Version": "1.0"})
        self.assertEquals({'Requested_version': '1.0', 'Message': 'Things in 1.0'}, result.json)

        result = self.simulate_get('/stuff', headers={"API-Version": "1.0"})
        self.assertEquals({'Requested_version': '1.0', 'Message': 'Stuff in 1.0'}, result.json)

        result = self.simulate_get('/things', headers={"API-Version": "1.1a"})
        self.assertEquals({'Requested_version': '1.1a', 'Message': 'Things in 1.1a'}, result.json)

        result = self.simulate_get('/stuff', headers={"API-Version": "1.1a"})
        self.assertEquals({'Requested_version': '1.1a', 'Message': 'Stuff in 1.0'}, result.json)

        result = self.simulate_get('/things', headers={"API-Version": "1.1b"})
        self.assertEquals({'Requested_version': '1.1b', 'Message': 'Things in 1.0'}, result.json)

        result = self.simulate_get('/stuff', headers={"API-Version": "1.1b"})
        self.assertEquals({'Requested_version': '1.1b', 'Message': 'Stuff in 1.1b'}, result.json)

    def test_failures(self):
        result = self.simulate_get("/not_found")
        self.assertEquals(404, result.status_code)

        # Unknown version
        result = self.simulate_get("/stuff", headers={"API-Version": "2.0"})
        self.assertEquals(400, result.status_code)
        self.assertEquals({'title': "Invalid API Version '2.0'"}, result.json)

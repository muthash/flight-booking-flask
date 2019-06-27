import unittest

from app import create_app


class TestDevelopmentConfig(unittest.TestCase):

    def test_app_is_development(self):
        self.app = create_app(config_name="development")
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['CSRF_ENABLED'] is True)


class TestTestingConfig(unittest.TestCase):

    def test_app_is_testing(self):
        self.app = create_app(config_name="testing")
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is True)


class TestProductionConfig(unittest.TestCase):

    def test_app_is_production(self):
        self.app = create_app(config_name="production")
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue(self.app.config['TESTING'] is False)


if __name__ == '__main__':
    unittest.main()

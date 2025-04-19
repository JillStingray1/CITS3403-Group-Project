import unittest
from middleware import middleware


class TestValidation(unittest.TestCase):

    def test_password_validation(self):
        self.assertEqual(middleware.validate_password("abcd8"), True)
        self.assertEqual(middleware.validate_password("; drop table *;"), False)

    def test_username_validation(self):
        self.assertEqual(middleware.validate_username("abcd8"), True)
        self.assertEqual(middleware.validate_username("Jill_Stingray"), True)
        self.assertEqual(middleware.validate_username("ACcd.8"), False)
        self.assertEqual(middleware.validate_username("ACcd?8"), False)
        self.assertEqual(middleware.validate_username("ACcd!8"), False)
        self.assertEqual(middleware.validate_username("ACcd.8"), False)

        self.assertEqual(middleware.validate_username("; drop table *;"), False)

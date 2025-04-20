import unittest
from middleware import middleware


class TestValidation(unittest.TestCase):

    def test_password_validation(self):
        # test cases for not meeting the length requirements
        self.assertEqual(
            middleware.validate_password("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
            False,
        )
        self.assertEqual(
            middleware.validate_password("A"),
            False,
        )

        # test cases for rejecting special characters
        self.assertEqual(middleware.validate_password(";::::;;;:"), False)
        self.assertEqual(middleware.validate_password("; drop table *;"), False)

        # good passwords tests
        self.assertEqual(middleware.validate_password("abcd8"), True)
        self.assertEqual(middleware.validate_password("!#+:=.?"), True)

    def test_username_validation(self):
        # test cases for not meeting the length requirments
        self.assertEqual(middleware.validate_username("aa"), False)
        self.assertEqual(
            middleware.validate_password("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
            False,
        )

        # test cases for rejecting special characters
        self.assertEqual(middleware.validate_username("ACcd.8"), False)
        self.assertEqual(middleware.validate_username("ACcd?8"), False)
        self.assertEqual(middleware.validate_username("ACcd!8"), False)
        self.assertEqual(middleware.validate_username("; drop table *;"), False)

        # good usernames tests
        self.assertEqual(middleware.validate_username("aaa"), True)
        self.assertEqual(middleware.validate_username("abcd8"), True)
        self.assertEqual(middleware.validate_username("Jill_Stingray"), True)

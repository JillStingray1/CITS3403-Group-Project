import unittest
import tools.tools as tools


class TestValidation(unittest.TestCase):

    def test_password_validation(self):
        # test cases for not meeting the length requirements
        self.assertEqual(
            tools.validate_password("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
            False,
        )
        self.assertEqual(
            tools.validate_password("A"),
            False,
        )

        # test cases for rejecting special characters
        self.assertEqual(tools.validate_password(";::::;;;:"), False)
        self.assertEqual(tools.validate_password("; drop table *;"), False)

        # good passwords tests
        self.assertEqual(tools.validate_password("abcd8"), True)
        self.assertEqual(tools.validate_password("!#+:=.?"), True)

    def test_username_validation(self):
        # test cases for not meeting the length requirments
        self.assertEqual(tools.validate_username("aa"), False)
        self.assertEqual(
            tools.validate_password("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"),
            False,
        )

        # test cases for rejecting special characters
        self.assertEqual(tools.validate_username("ACcd.8"), False)
        self.assertEqual(tools.validate_username("ACcd?8"), False)
        self.assertEqual(tools.validate_username("ACcd!8"), False)
        self.assertEqual(tools.validate_username("; drop table *;"), False)

        # good usernames tests
        self.assertEqual(tools.validate_username("aaa"), True)
        self.assertEqual(tools.validate_username("abcd8"), True)
        self.assertEqual(tools.validate_username("Jill_Stingray"), True)

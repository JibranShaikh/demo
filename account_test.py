import unittest
import account as AccountClass


class Test(unittest.TestCase):
    accInfo = AccountClass.account()


    def test_check(self):
        print("Checking possible passwords\n")
        passwordList = ["abcd","jibran","shaikh","aikh"]

        for password in passwordList:
            print("Checking password "+password+"\n")
            passInfo = self.accInfo.check_password_length(password)
            self.assertFalse(passInfo)

if __name__ == '__main__':
    unittest.main()

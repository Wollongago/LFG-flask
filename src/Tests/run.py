import unittest

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('Tests/cases', pattern='*.py')
    unittest.TextTestRunner().run(all_tests)

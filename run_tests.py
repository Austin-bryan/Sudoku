import unittest

# Discover and run all tests in the 'tests' directory
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner()

    runner.run(suite)

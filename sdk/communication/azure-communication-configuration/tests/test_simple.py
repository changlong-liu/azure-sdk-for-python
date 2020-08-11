# Testing Azure Packages has some additional complication/reading required.
# Reference https://github.com/Azure/azure-sdk-for-python/wiki/Contributing-to-the-tests
# Pytest should be leveraged to test your project.

from devtools_testutils import AzureMgmtTestCase
import unittest
import pytest

# this test case highlights that there are some additional Test capabilities present in devtools_testutils
# as a package owner you are not required to use these. Standard PyTest implementation will work.
# a placeholder for UserManagementTests.
# TODO: add tests
class UserManagementTest(AzureMgmtTestCase):
    def setUp(self):
        super(UserManagementTest, self).setUp()

    def test_sample(self):
        self.assertEqual(1,1)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
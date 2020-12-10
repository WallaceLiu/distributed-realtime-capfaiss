import unittest
from test.test_apireindex import ReindexApiTest
from test.test_apiadd import AddApiTest
from test.test_apidel import DelApiTest
from test.test_apisearch import SearchApiTest
from test.test_apimeta import MetaApiTest

if __name__ == '__main__':
    print('test begin...')

    suite = unittest.TestSuite()
    # suite.addTest(MetaApiTest('test'))
    suite.addTest(ReindexApiTest('test'))
    suite.addTest(SearchApiTest('test'))
    suite.addTest(AddApiTest('test'))
    suite.addTest(DelApiTest('test'))

    runner = unittest.TextTestRunner()
    runner.run(suite)

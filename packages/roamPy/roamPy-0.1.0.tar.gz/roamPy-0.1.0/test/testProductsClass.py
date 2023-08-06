from roamPy.roamClass import Roam
import unittest
import os

class Test_products(unittest.TestCase):

    token = os.environ.get('Roam_API_Key')

    roam = Roam(url='https://api.roam.plus/external/', token = token)


    def testGetProducts(self, roam=roam):
        result = roam.getAllProducts()
        self.assertIsInstance(result, list)


    def testGetAllProductswithPub(self, roam=roam):

        result = roam.getAllProductswithPub()
        self.assertIsInstance(result, list)



if __name__ == '__main__':
    unittest.main()
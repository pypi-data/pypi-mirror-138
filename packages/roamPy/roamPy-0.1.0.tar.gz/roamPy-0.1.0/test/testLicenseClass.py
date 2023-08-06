from roamPy.roamClass import Roam
import unittest
import os

class Test_license(unittest.TestCase):

    token = os.environ.get('Roam_API_Key')

    roam = Roam(url='https://api.roam.plus/external/', token = token)


    def testGetLicenses(self, roam=roam):

        result = roam.getLicenses()
        self.assertIsInstance(result, list)

    def testGetLicensewRels(self, roam=roam):

        result = roam.getLicenseswRels(['licensePeriods', 'publisher'])
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
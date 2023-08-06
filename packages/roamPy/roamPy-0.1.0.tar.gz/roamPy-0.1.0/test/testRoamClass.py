from roamPy.roamClass import Roam
import unittest
import os

class Test_roam(unittest.TestCase):

    token = os.environ.get('Roam_API_Key')

    roam = Roam(url='https://api.roam.plus/external/', token = token)

    def testGetWithURL(self, roam=roam):
        
        result = roam.getWithUrl('https://api.roam.plus/external/subscriptionPeriods/916/publisher')
        self.assertIsInstance(result, dict)
from roamPy.roamClass import Roam
import unittest
import os

class Test_heartbeat(unittest.TestCase):

    token = os.environ.get('Roam_API_Key')

    roam = Roam(url='https://api.roam.plus/external/', token = token)


    def testHeartbeat(self, roam=roam):

        result = roam.checkHeartbeat()
        self.assertIsInstance(result, dict)



if __name__ == '__main__':
    unittest.main()
from roamPy.roamClass import Roam
import unittest
import os


class Test_subscriptionPeriods(unittest.TestCase):

    token = os.environ.get('Roam_API_Key')

    roam = Roam(url='https://api.roam.plus/external/', token = token)

    def testGetAllSubPeriods(self, roam=roam):
        result = roam.getAllSubPeriods()
        self.assertIsInstance(result, list)

    def testGetSubPeriodsBefore(self, roam=roam):
        result = roam.getSubPeriodsBefore('2021-01-01')
        self.assertIsInstance(result, dict)

    def testGetSubPeriodsAfter(self, roam=roam):
        result = roam.getSubPeriodsAfter('2021-01-01')
        self.assertIsInstance(result, dict)

    def testGetSubPeriodsBetween(self, roam=roam):
        result = roam.getSubPeriodsBetween(startDate='2020-01-01', endDate='2021-01-01')
        self.assertIsInstance(result, dict)

    def testGetSubPeriodById(self, roam=roam):
        result = roam.getSubPeriodById('916')
        self.assertIsInstance(result, dict)

    def testGetSubPeriodByIdwithRel(self, roam=roam):
        result = roam.getSubPeriodByIdwithRel('916', ['product', 'vendor'])
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
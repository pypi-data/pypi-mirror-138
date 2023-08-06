from roamPy.heartbeatClass import heartbeat
from roamPy.subscriptionsClass import subscriptions
from roamPy.subscriptionPeriodsClass import subscriptionPeriod
from roamPy.productsClass import products
from roamPy.licensesClass import license
from requests import request

class Roam(heartbeat, subscriptions, subscriptionPeriod, products, license):

    def __init__(self, url, token):
        
        self.url = url
        self.header = {
                        'Authorization': "Token " + token, 
                        'Accept': 'application/vnd.api+json' ,
                        'Accept': 'application/vnd.api+json; version=1.0'
        }

        super(Roam, self).__init__(self.url, self.header)


    def getWithUrl(self, userUrl):
        """
        Returns metadata from Roam.plus when provided a complete API url. 

        :params self:  Inherits URL and Headers from roamClass
        :params userURL: A string of a complete URL for the Roam api
        :returns: Returns the corresponding metadata associated with the
                  provided endpoint. 
        """

        response = request("GET", url = userUrl, headers = self.header)

        return(response.json())

        
        





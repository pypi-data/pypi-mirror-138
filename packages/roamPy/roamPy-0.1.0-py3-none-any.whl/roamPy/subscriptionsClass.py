from requests import request
from roamPy.pageFunc import pageIterate


class subscriptions(object):
        
    def __init__(self, url, header):
        
        self.url = url 
        self.header = header
        

    def getAllSubscriptions(self):
        """
        Iterates through the paginated 'Subscriptions' endpoint to return metadata 
        for all Subscriptions in the Roam instance
        
        :param self: Inherits URL and Header constructors from the Roam Class
        :return: Returns a list of json objects with metadata for all subsriptions. 
                 One list item for each page of 40 datasets from the endpoint
        """
        urlSubs = self.url + 'subscriptions'
        
        res = pageIterate(url=urlSubs, header = self.header)

        return(res)


    def getOneSubscription(self, id):
        """
        Exports the metadata for a single subscription identified by its subscription ID

        :param self: Inherits URL and Header variables from Roam Class
        :param id:   A string that contains the numeric ID of the subscription
        :returns: A json object with metadata for a single subscription
        """

        urlOneSub = self.url + 'subscriptions/' + id
        
        oneSub = request("GET", url = urlOneSub, headers = self.header)
        
        return(oneSub.json())

        
    def getOneSubwithRelations(self, id, relations):
        """
        Retrieves the metadata for a subscription and includes corresponding urls to related records

        :param self: Inherits URL and header variables from Roam Class
        :param id: A string that contains the numeric ID of the subscription
        :param relations: A list of strings naming the relations that should be included in the response. 
                          Relations can be any of the following: product, subscriptionPeriods, notes, links,
                          files, licensePeriods.license.publisher, licensePeriods.licensePeriodStatus
        """
        relStr = ','.join([str(item) for item in relations])

        urlOneSubwRel = self.url + 'subscriptions/' + id + '?include=' + relStr

        oneSubwRel = request("GET", url = urlOneSubwRel, headers = self.header)

        return(oneSubwRel.json())

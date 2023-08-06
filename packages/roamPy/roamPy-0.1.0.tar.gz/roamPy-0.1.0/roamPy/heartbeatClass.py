from requests import request


class heartbeat(object):
        
    def __init__(self, url, header):

        self.url = url
        self.header = header
     
    def checkHeartbeat(self):
        """
        Calls the heartbeat endpoint for the Roam.plus api. Returns the status json. Used for testing the connection

        :param self: Inherits URL and Headers from roamClass
        :return: Returns a json object with the api status
        """

        response = request("GET", url = self.url, headers = self.header)
        
        return(response.json())


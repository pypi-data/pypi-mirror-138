
from roamPy.pageFunc import pageIterate


class license(object):

    def __init__(self, url, header):
        
        self.url = url 
        self.header = header

    def getLicenses(self):
        """
        Iterates through the paginated 'License' endpoint to return metadata 
        for all Licenses in the Roam instance.

        :params self: Inherits URL and Header constructors from the Roam Class
        :returns: Returns a list of json objects with metadata for all licenses. 
                  One list item for each page of 40 datasets from the endpoint
        """

        urlLic = self.url + 'licenses'

        res = pageIterate(urlLic, self.header)

        return(res)


    def getLicenseswRels(self, relations):
        """
        Iterates through the paginated 'License' endpoint to return metadata 
        for all Licenses in the Roam instance. Includes urls for related
        licensePeriods and Publishers. 

        :params self: Inherits URL and Header constructors from the Roam Class
        :params relations: A list for strings containing the relations to be 
                        included. Can contain licensePeriods, publisher or both
        :returns: Returns a list of json objects with metadata for all licenses. 
                  One list item for each page of 40 datasets from the endpoint
         """

        relStr = ','.join([str(item) for item in relations])

        urlLic = self.url + 'licenses?includes=' + relStr

        res = pageIterate(urlLic, self.header)

        return(res)

from roamPy.pageFunc import pageIterate

class products(object):

    def __init__(self, url, header):
        
        self.url = url 
        self.header = header


    def getAllProducts(self):
        """
        Iterates through the paginated 'Products' endpoint to return metadata 
        for all Products in the Roam instance
        
        :param self: Inherits URL and Header constructors from the Roam Class
        :return: Returns a list of json objects with metadata for all products. 
                 One list item for each page of 40 datasets from the endpoint
        """

        urlProds = self.url + 'products'

        res = pageIterate(urlProds, self.header)

        return(res)
        

    def getAllProductswithPub(self):
        """
        Iterates through the paginated 'Products' endpoint to return metadata
        for all Products in the Roam instance. Includes the url for Publisher
        information. 

        :param self: Inherits URL and Header constructors from the Roam Class
        :return: Returns a list of json objects with metadata for all products. 
                 One list item for each page of 40 datasets from the endpoint 
        """
        
        urlProds = self.url + 'products?include=publisher'

        res = pageIterate(urlProds, self.header)

        return(res)

        
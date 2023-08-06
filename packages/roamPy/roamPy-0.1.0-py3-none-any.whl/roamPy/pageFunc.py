from requests import request


def pageIterate(url, header):
    """
    Utility function to iterate through paginated end points. 

    :params url: complete endpoint url
    :params header: header object including api token
    """
    result = []

    firstPage = request("GET", url = url, headers = header)
    firstPage = firstPage.json()
    next = firstPage['links']['next']

    while next != None:
        page = request("GET", url = next, headers = header)
        page = page.json()

        result.append(page)
           
        try:
            next = page['links']['next']
        except: 
            next = None

    return(result)


class CellTypeResponse(object):
    def __init__(self, cell, response):
        self.cell     = cell
        self.response = response
        self.uri      = self.setUri()
        self.types    = self.setTypes()

    def setUri(self):
        #cause response was a tuple
        response = self.response[1]
        try:
            uri = response[response.index('URI="')+5:]
            return uri[:uri.find('"')]
        except:
            return -1

    def setTypes(self):
        response = self.response[1]
        try:
            types = response[response.index('<Resource '):]
            types = types[types.index('types="')+7:]
            return types[:types.find('"')]
        except:
            return -1

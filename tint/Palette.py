
class Palette(object):

    def __init__(self, paletteJson):
        self.name = paletteJson['name']
        self.colors = [Color(colorJson) for color in paletteJson['colors']]

    def addColor(self, color):
        self.colors.append(color)
    
    def filterColors(self, seachString):
        return [color for color in self.colors if seachString in color.hex]
    
    def findColor(self)

    def removeColor(self, color):


from Color import Color

class Palette(object):

    def __init__(self, paletteJson):
        self.name = paletteJson['name']
        self.colors = [Color(colorJson) for color in paletteJson['colors']]

    def addColor(self, color):
        self.colors.append(color)
    
    def findColors(self, seachString):
        return [color for color in self.colors if seachString in color.hex]

    def removeColor(self, color):
        if color in self.colors:
            self.colors.remove(color)

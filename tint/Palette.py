from Color import Color

class Palette(object):

    def __init__(self, library, name, colors):
        self.name = name
        self.colors = colors

    def addColor(self, color):
        self.colors.append(color)
        if self.library:
            self.library.save()
    
    def findColors(self, seachString):
        return [color for color in self.colors if seachString in color.hex]

    def removeColor(self, color):
        if color in self.colors:
            self.colors.remove(color)
            library.save()

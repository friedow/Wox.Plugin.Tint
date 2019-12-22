from Palette import Palette
from Color import Color

class Library(object):

    def __init__(self, path):
        self.path = path
        if os.path.isfile(self.path):
            self.__load()
        else:
            self.__create()

    def __load(self):
        libraryJson = {}
        with open(self.path, 'r') as libraryFile:
            libraryJson = json.load(libraryFile)

        for paletteJson in libraryJson['palettes']:
            paletteName = paletteJson['name']
            paletteColors = [Color(colorJson) for color in paletteJson['colors']]
            Palette(library, paletteName, paletteColors)

        self.palettes = [Palette(paletteJson) for paletteJson in libraryJson['palettes']]
        
    def __create(self):
        self.palettes = []
        self.save()

    def save(self):
        with open(self.path, 'w+') as libraryFile:
            json.dump(self.__dict__, libraryFile)
    
    def addPalette(self, palette):
        self.palettes.append(palette)
        self.save()
    
    def findPalettes(self, searchString):
        return [palette for palette in self.palettes if seachString in palette.name]
    
    def removePalette(self, palette):
        if palette in self.palettes:
            self.palettes.remove(palette)
            library.save()

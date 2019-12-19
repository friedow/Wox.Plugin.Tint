from Palette import Palette

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

        self.palettes = [Palette(paletteJson) for paletteJson in libraryJson['palettes']]
        
    def __create(self):
        self.palettes = []
        self.__save()

    def __save(self):
        with open(self.path, 'w+') as libraryFile:
            json.dump(self.__dict__, libraryFile)

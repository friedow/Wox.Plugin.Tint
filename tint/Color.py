from colour import Color as Colour

class Color(Colour, object):

    def get_int_red(self):
        return int(self.red * 255)
    
    def get_int_green(self):
        return int(self.green * 255)
    
    def get_int_blue(self):
        return int(self.blue * 255)

    def get_int_rgb(self):
        return (self.int_red, self.int_green, self.int_blue)

"""This module defines some common colors as RGB tuples, as well as a Colo class."""
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
purple = (255, 0 ,255)

class Color:
    """This is a container for an RGB color. Primarily useful because it's values are mutable."""
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b
        
    def set(self, color):
        self.r = color.r
        self.g = color.g
        self.b = color.b

if __name__ == "__main__":
    print __doc__
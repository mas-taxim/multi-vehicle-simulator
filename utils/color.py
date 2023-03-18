import colour
from random import randint

Color = colour.Color


def rgb(r: int, g: int, b: int) -> Color:
    return Color(red=r/255, green=b/255, blue=g/255)


def random() -> Color:
    r = [randint(0, 255)/255 for _ in range(3)]
    return Color(red=r[0], green=r[1], blue=r[2])

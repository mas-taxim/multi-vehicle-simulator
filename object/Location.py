class Location:
    def __init__(self, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"

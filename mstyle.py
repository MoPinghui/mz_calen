

class Style():
    def __init__(self):
        self.color = "#000000"
        self.bcolor = "#FFFFFF"
        self.fontSize = "18px"
        self.fontFamily = "Microsoft YaHei"
    
    def set_color(self, color, bcolor):
        self.color = color 
        self.bcolor = bcolor 
    
    def set_font(self, fontSize, fontFamily):
        self.fontSize = fontSize
        self.fontFamily = fontFamily
    
    def toString(self, name=""):
        s = name + "{"
        s += "color:"+self.color+";"
        s += "background:"+self.bcolor+";"
        s += "font-size:"+self.fontSize+";"
        s += "font-family:"+self.fontFamily+";"
        s += "}"
        return s 
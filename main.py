import random

from PIL import Image, ImageDraw
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


class PhotoEditorApp(App):
    pass


class PhotoEditorScreen(Screen):
    def display_image(self,imageload):
        self.ids.image.source=imageload


    def sepia(self):
        pic = self.ids.image.source
        img = Image.open(pic)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = int(pixels[x, y][0] * .393 + pixels[x, y][1] * 0.769 + pixels[x, y][2] * 0.189)
                green = int(pixels[x, y][0] * .349 + pixels[x, y][1] * 0.686 + pixels[x, y][2] * 0.168)
                blue = int(pixels[x, y][0] * .272 + pixels[x, y][1] * 0.534 + pixels[x, y][2] * 0.131)
                pixels[x, y] = (red, green, blue)
        img.save("sepia.png")
        self.ids.image.source="sepia.png"

    def invert(self):
        pic = self.ids.image.source
        img = Image.open(pic)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = 255 - pixels[x, y][0]
                blue = 255 - pixels[x, y][1]
                green = 255 - pixels[x, y][2]
                pixels[x, y] = (red, green, blue)
        img.save("invert.png")
        self.ids.image.source="invert.png"

    def two_tone(self):
        pic = self.ids.image.source
        img = Image.open(pic)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = pixels[x, y][0]
                green = pixels[x, y][1]
                blue = pixels[x, y][2]
                average = (red + green + blue) / 3
                if average > 127:
                    pixels[x, y] = (255, 255, 255)
                else:
                    pixels[x, y] = (0, 0, 0)
        img.save("twotone.png")
        self.ids.image.source="twotone.png"

    def pointillism(self):
        pic = self.ids.image.source
        img = Image.open(pic)
        pixels = img.load()
        countnum = 0
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        while countnum <= 15000:
            countnum += 1
            size = random.randint(3, 5)
            x = random.randint(0, img.size[0] - 5)
            y = random.randint(0, img.size[1] - 5)

            ellipsebox = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
            del draw
        canvas.save("pointillism.png")
        self.ids.image.source="pointillism.png"

    def mirror(self):
        pic = self.ids.image.source
        img = Image.open(pic)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(int((img.size[0]) / 2), img.size[0]):
                temp = pixels[-x, y]
                pixels[-x, y] = pixels[x, y]
                pixels[x, y] = temp
        img.save("flip.png")
        self.ids.image.source="flip.png"
class MouseTouch(Widget):
    def on_touch_down(self,touch):
        x,y=touch.x,touch.y
        self.coordinates.append(int(x))
        self.coordinates.append(int(y))
        if len(self.coordinates)>4:
            self.coordinates=self.coordinates[2:]
        print(self.coordinates)
        touch.push()
        touch.apply_transform_2d(self.to.local)

    def on_touch_move(self,touch):
        pass
    def on_touch_up(self,touch):
        print("\nMouse Button Released")
        coords = touch.pos
        print("x coordinate: " + str(int(coords[0])))
        print("y coordinate: " + str(int(coords[1])))
PhotoEditorApp().run()
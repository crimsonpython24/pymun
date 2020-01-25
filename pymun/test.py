from PIL import Image, ImageDraw, ImageFont
import random

W, H = (512, 512)
msg = "IS"

myFont = ImageFont.truetype('/Library/Fonts/Arial.ttf', 300)

img = Image.new('RGB', (W, H), color=(random.randrange(0, 70), random.randrange(0, 70), random.randrange(0, 70)))
draw = ImageDraw.Draw(img)
w, h = draw.textsize(msg, font=myFont)
draw.text(((W-w)/2, (H-h)/2), msg, fill=(255, 255, 225), font=myFont)

img.save("hello.png", "PNG")

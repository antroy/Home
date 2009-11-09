import Image

im = Image.open("oxygen.png")

print im.size

out = ""

for i in range(0,628, 7):
    px = im.getpixel((i, 50))
    if not (px[0] == px[1] and px[0] == px[2]):
        break
    out += chr(px[0])

print out
#for pixel in imlist:
#    print pixel
     
newvals = [105, 110, 116, 101, 103, 114, 105, 116, 121]
vals = [chr(x) for x in newvals]
out = ''.join(vals)

print out


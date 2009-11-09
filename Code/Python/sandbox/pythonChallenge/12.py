#  http://www.pythonchallenge.com/pc/return/5808.html
#
# cave.jpg

import Image

def halve(size):
    return (size[0]/2, size[1]/2)


img = Image.open('cave.jpg')

px = img.getpixel((30,25))

print px[0]
print px[1]
print px[2]

size = img.size

newsize = halve(size)

imgodd = Image.new("RGB", newsize)
imgeven = Image.new("RGB", newsize)

for i in range(size[0]):
    for j in range(size[1]):
        imgthis = None
        if i % 2 == 0:
            imgthis = imgeven
        else:
            imgthis = imgodd
        pixel = img.getpixel((i,j))
        imgthis.putpixel(halve((i,j)), pixel)
        
        
imgodd.save("caveodd.jpg")
imgeven.save("caveeven.jpg")


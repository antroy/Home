#  http://www.pythonchallenge.com/pc/return/evil.html
#
# 

import Image

def halve(size):
    return (size[0]/2, size[1]/2)

def hand(ij):
    i = ij[0] % 2
    j = ij[1] % 2
    
    if (i == 0 and j == 0):
        return 0
    elif (i == 1 and j == 0):
        return 1
    elif (i == 0 and j == 1):
        return 2
    else:
        return 3
        
original = Image.open('evil1.jpg')
        
images = []

for i in range(4):
    images.append(Image.new("RGB", halve(original.size)))

for i in range(640):
    for j in range(480):
        im = images[hand((i,j))]
        px = original.getpixel((i,j))
        im.putpixel((i/2, j/2), px)
        
for i in range(4):
    pass
    #images[i].save("deal" + str(i) + ".jpg")
    
images = []

for i in range(6):
    images.append(Image.new("RGB", (640,80)))
    
for i in range(640):
    for j in range(480):
        im = images[j % 6]
        px = original.getpixel((i,j))
        im.putpixel((i, j/6), px)
    
for i in range(6):
    images[i].save("six" + str(i) + ".jpg")
    
original = Image.open("six5.jpg")
images = []

for i in range(2):
    images.append(Image.new("RGB", (320,80)))
    
for i in range(640):
    for j in range(80):
        im = images[i % 2]
        px = original.getpixel((i,j))
        im.putpixel((i/2, j), px)
    
for i in range(2):
    images[i].save("two" + str(i) + ".jpg")

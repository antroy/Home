from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import sys, os

def getImage(infile):
    file, ext = os.path.splitext(infile)
    path, file = os.path.split(file)
    im = Image.open(infile)

    im1 = im.filter(ImageFilter.FIND_EDGES)
    enhancer = ImageEnhance.Color(im1)
    im1 = enhancer.enhance(0.0)
    im1 = ImageOps.invert(im1)

    im1.show()
    im1.save(os.path.join(path, 'processed', file + ".edge" + ext), "JPEG")

    return im1

def compareImages(im1, im2):
    x1, y1 = im1.size
    x2, y2 = im2.size
    if not x1 == x2 or not y1 == y2:
        raise "Images are incomparable"

    ok = True

    for i, block in enumerate(split_grid(x1, y1, 100)):
        b_ok = block_ok(im1, im2, block)
        ok = ok and b_ok
        print i, b_ok

    return ok

def block_ok(im1, im2, block):
    count1 = count_black(im1, block)
    count2 = count_black(im2, block)
    
    print count1, count2

    if count1 == count2:
        return True

    maxval = float(max(count1, count2))
    minval = float(min(count1, count2))
    
    lower_limit = maxval * 0.85

    return minval > lower_limit

def count_black(im, block):
    x1, y1 = im.size
    iter = (im.getpixel((x, y))[0] ==  255 for x, y in block)

    count = 0

    for z in iter:
        if z:
            count += 1

    return count
    
def split_grid(maxx, maxy, step):
    lastx, lasty, currentx, currenty = 0, 0, 0, 0

    for i in range(step, maxx, step):
        currentx = i
        for j in range(step, maxy, step):
            currenty = j
            yield [(x,y) for x in range(lastx, currentx) for y in range(lasty, currenty)]
            lasty = currenty
        lastx = currentx

    yield [(x,y) for x in range(lastx, maxx) for y in range(lasty, maxy)]

def main():
    im1 = getImage(sys.argv[1])
    im2 = getImage(sys.argv[2])
    ok = compareImages(im1, im2)
    print "OK" if ok else "FAIL"

def main2():
    last = None
    for i, z in enumerate(split_grid(1020, 983, 100)):
        last = z
        if i < 2:
            print "+" * 20
            print z
    print "=" * 20
    print last


if __name__ == "__main__":
    main()




import Image, sys, os, os.path as path
from optparse import OptionParser

ROTATE_MAP = {"L":Image.ROTATE_90, "U": Image.ROTATE_180, "R": Image.ROTATE_270}

class Manipulator(object):
    def __init__(self, imagepath, options=None):
        if not options:
            self.options = get_default_options()
        else:
            self.options = options
        self.image = imagepath
        
    def createThumb(self, thumbname=""):
        im = Image.open(self.image)
        im.thumbnail((200,200), Image.ANTIALIAS)
        
        if thumbname == "":
            name, ext = os.path.splitext(self.image)
            thumbname = name + "-thumb" + ext
        
        im.save(thumbname, "JPEG")
      
    def process(self):
        image = Image.open(self.image)
        options = self.options
        
        newfile = "%s-small%s" % path.splitext(self.image)
        
        if options.overwrite:
            newfile = self.image
        
        if options.crop:
            print "Cropping", self.image
            image = image.crop(get_crop_box(image.size, options))
        
        if not options.suppress:
            print "Shrinking", self.image
            image = image.resize(get_new_size(image.size, options), Image.ANTIALIAS)
        
        if options.rotate and len(options.rotate) > 0:
            direction = ROTATE_MAP.get(options.rotate[:1].upper())
            if direction:
                print "Rotating in direction %s (%s)" % (options.rotate, direction)
                image = image.transpose(direction)
            else:
                print "Rotation argument invalid. Assuming 0 degrees."
        
        print "Saving as", newfile
        image.save(newfile)

def get_crop_box(size, options):
    right, bottom = size
    if options.right != None:
        right = options.right
    if options.bottom != None:
        bottom = options.bottom
        
    return (options.left, options.top, right, bottom)
    
def get_new_size(size, options):
    w, h = size
    w_out, h_out = w, h
    if options.height != None:
        h_out = options.height
        r = float(h_out) / float(h)
        w_out = int(r * w)
    else:
        w_out = options.width
        r = float(w_out) / float(w)
        h_out = int(r * h)
    return (w_out, h_out)
    
def get_default_options():
    class optionclass(object):
        pass
    out = optionclass()
    out.crop = False
    out.left = 0
    out.top = 0
    out.width = 600
    out.rotate = None
    out.suppress = False
    out.overwrite = False
    out.height = None
    
    return out

def processable(f):
    out = path.isfile(f) and (f.lower().endswith(".jpg") or f.lower().endswith(".png"))
    return out

if __name__ == "__main__":
    pass

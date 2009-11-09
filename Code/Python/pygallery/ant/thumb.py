import Image, os

__all__ = ["createThumb"]

def createThumb(filename, thumbname=""):
    im = Image.open(filename)
    im.thumbnail((200,200), Image.ANTIALIAS)
    
    if thumbname == "":
        file, ext = os.path.splitext(filename)
        thumbname = file + "-thumb" + ext
    
    im.save(thumbname, "JPEG")
    
if __name__ == "__main__":
    createThumb("Sunset.jpg")


import os, sys, os.path as path, Image

args = sys.argv

if len(args) < 2:
    print "Usage: ", args[0], "FOLDER/FILE_LIST [width | *] [height]"
    sys.exit(0)

folder = args[1]

if path.exists(folder):
    for root, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(".jpg") and not f.endswith("_reduced.jpg"):
                split = f.split('.')
                newf = split[0] + "_reduced.jpg"
                img = Image.open(path.join(root, f))
                
                imwidth, imheight = img.size
                width = 700.0
                
                ratio = width / imwidth
                height = int(imheight * ratio)
                width = int(width)
                
                out = img.resize((width, height))
                
                out.save(path.join(root, newf))
                
                #print "Old:", f, "; new:", newf
            
        

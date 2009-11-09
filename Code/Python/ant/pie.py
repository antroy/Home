import Image, ImageDraw, math

_colours = ["red", "blue", "green", "cyan", "magenta", "yellow", "orange", "purple"]

def colour_iterator(colours):
    while(True):
        for colour in colours:
            yield colour

def makePie(data, filename, colours=_colours, size=(100,100)):
    total = reduce(lambda x, y: x+y, data)
    angles = [360.0 * x / total for x in data]
    colorIterator = colour_iterator(colours)
    
    im = Image.new("RGBA", size, (0xff, 0xff, 0xff, 0x00))
    
    draw = ImageDraw.Draw(im)
    
    current_angle = 0
    current_color = None
    shift = 5
    shadow_bb = (shift, shift, size[0], size[1])
    pie_bb = (0, 0, size[0] - shift, size[1] - shift)
    
    #draw.pieslice(shadow_bb, 0, 360, fill="darkgray")
    
    for angle in angles:
        start = current_angle
        current_angle = current_angle + int(angle)
        current_color = colorIterator.next()
        print start, current_angle
        draw.pieslice(pie_bb, start + 180, current_angle + 180, fill=current_color)
        
    if current_angle < 360:
        draw.pieslice((0,0,150,150), current_angle, 360, fill=current_color)
        
    #draw.arc(pie_bb, 0, 360)
    
    del draw 
    
    im.save(filename, "PNG")
    
if __name__ == "__main__":
    makePie([30, 50], "test.png", colours=["red", "darkblue"])
    

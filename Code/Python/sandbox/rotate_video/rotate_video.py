#! /bin/env python
import sys, os, time
import pymedia.muxer as muxer
import pymedia.video.vcodec as vcodec
import pygame
import Image

def dumpVideo( inFile, outFilePattern, fmt=2 ):
    pygame.init()

    dm= muxer.Demuxer( inFile.split( '.' )[ -1 ] )
    i= 1
    f= open( inFile, 'rb' )
    s= f.read( 400000 )
    r= dm.parse( s )
    
    print dm.getInfo()
    sys.exit(0)

    v= filter( lambda x: x[ 'type' ]== muxer.CODEC_TYPE_VIDEO, dm.streams )
    if len( v )== 0:
        raise 'There is no video stream in a file %s' % inFile

    v_id= v[ 0 ][ 'index' ]
    print 'Assume video stream at %d index: ' % v_id
    c= vcodec.Decoder( dm.streams[ v_id ] )
    while len( s )> 0:
        for fr in r:
            if fr[ 0 ]== v_id:
                d= c.decode( fr[ 1 ] )
                # Save file as RGB BMP

                if d:
                    dd= d.convert( fmt )
                    img= pygame.image.fromstring( dd.data, dd.size, "RGB" )
                    pygame.image.save( img, outFilePattern % i )
                    i+= 1

        s= f.read( 400000 )
        r= dm.parse( s )

    pygame.quit()
    print 'Saved %d frames' % i

def rotate_images(inPattern):
    i = 1
    while True:
        frame = inPattern % i
        print "Rotating %s" % frame
        if os.path.isfile(frame):
            im = Image.open(frame)
            im2 = im.rotate(90)
            im2.save(frame)
        else:
            break
        i += 1


def makeVideo( inPattern, outFile, outCodec ):
    # Get video stream dimensions from the image size

    pygame.init()
    i= 1
    # Opening mpeg file for output

    e= None
    i= 1
    fw= open( outFile, 'wb' )
    while i:
        print "Adding Frame %i (%s)" % (i, inPattern % i )
        if os.path.isfile( inPattern % i ):
            s= pygame.image.load( inPattern % i )
            if not e:
                if outCodec== 'mpeg1video':
                    bitrate= 2700000
                else:
                    bitrate= 9800000

                params= { \
                  'type': 0,
                  'gop_size': 12,
                  'frame_rate_base': 125,
                  'max_b_frames': 0,
                  'height': s.get_height(),
                  'width': s.get_width(),
                  'frame_rate': 2997,
                  'deinterlace': 0,
                  'bitrate': bitrate,
                  'id': vcodec.getCodecID( outCodec )
                }
                print 'Setting codec to ', params
                e= vcodec.Encoder( params )
                t= time.time()

            # Create VFrame

            ss= pygame.image.tostring(s, "RGB")
            bmpFrame= vcodec.VFrame( vcodec.formats.PIX_FMT_RGB24, s.get_size(), (ss,None,None))
            yuvFrame= bmpFrame.convert( vcodec.formats.PIX_FMT_YUV420P )
            d= e.encode( yuvFrame )
            #print "\n\n", type(e), type(d), "\n\n"
            fw.write( d )
            i+= 1
        else:
            print '%d frames written in %.2f secs( %.2f fps )' % ( i, time.time()- t, float( i )/ ( time.time()- t ) )
            i= 0

    fw.close()
    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <filename>" % sys.argv[0]
        sys.exit(1)

    tempDir = ".temp"

    while os.path.exists(tempDir):
        tempDir += '0'

    os.mkdir(tempDir)

    filename = sys.argv[1]
    file_patt = tempDir + "/xxx-%d.bmp"

    dumpVideo(filename, file_patt)
    rotate_images(file_patt)
    makeVideo(file_patt, "xxxx.avi", "mpeg2video")

    for root, folders, files in os.walk(tempDir, topdown=False):
        for f in files:
            os.remove(os.path.join(root, f))
        for f in folders:
            os.rmdir(os.path.join(root, f))
    os.rmdir(tempDir)

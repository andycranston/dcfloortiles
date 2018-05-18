#! /usr/bin/python3
#
# @(!--#) @(#) dcft.py, version 003, 18-may-2018
#
# create a PNG image of a data centre floor tile layout
#

############################################################

#
# imports
#

import sys
import os
import argparse
import zlib
import html
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

############################################################

DEFAULT_TILES_ACROSS  = 8
DEFAULT_TILES_DEEP    = 4
DEFAULT_PIXELS_ACROSS = 60
DEFAULT_PIXELS_DEEP   = 60
DEFAULT_BORDER_PIXELS = 2
DEFAULT_IMAGE_FILE    = "floortiles.png"

############################################################

def dword(i):
    b0 = (i & 0x000000FF) // 0x00000001
    b1 = (i & 0x0000FF00) // 0x00000100
    b2 = (i & 0x00FF0000) // 0x00010000
    b3 = (i & 0xFF000000) // 0x01000000

    return bytes([b3, b2, b1, b0])

############################################################

def writeimage(filename):
    global pixelsacross
    global pixelsdeep
    global pixels

    f = open(filename, "wb")

    bitdepth = 8             # one byte per pixel
    colourtype = 0           # true grayscale (no palette)
    compression = 0          # zlib
    filtertype = 0           # adaptive (each scanline seperately)
    interlaced = 0           # no interlacing

    ### print("Pixels across {}".format(pixelsacross - 1))
    ### print("Pixels deep {}".format(pixelsdeep))

    # create png header
    pnghdr = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')

    f.write(pnghdr)

    # create and add IHDR
    data = b""

    data += dword(pixelsacross - 1) + dword(pixelsdeep)
    data += bytes([bitdepth])
    data += bytes([colourtype])
    data += bytes([compression])
    data += bytes([filtertype])
    data += bytes([interlaced])

    block = "IHDR".encode('ascii') + data

    ihdr = dword(len(data)) + block + dword(zlib.crc32(block))

    f.write(ihdr)

    # create and add IDAT
    data = b""

    compressor = zlib.compressobj()
    data = compressor.compress(pixels)
    data += compressor.flush()       #!! what!?

    block = "IDAT".encode('ascii') + data

    idat = dword(len(data)) + block + dword(zlib.crc32(block))

    f.write(idat)

    # create and add IEND
    data = b""

    block = "IEND".encode('ascii') + data

    iend = dword(len(data)) + block + dword(zlib.crc32(block))

    f.write(iend)

    f.flush()

    f.close()

    return

############################################################

def plot(x, y):
    global pixelsacross
    global pixelsdeep
    global pixels

    pixels[(y * pixelsacross) + x] = 0

############################################################

def unplot(x, y):
    global pixelsacross
    global pixelsdeep
    global pixels

    pixels[(y * pixelsacross) + x] = 0xFF

############################################################

def drawbox(x, y, across, deep):
    for i in range(0, across):
        plot(x + i, y)
        plot(x + i, y + deep - 1)
    for i in range(0, deep):
        plot(x,             y + i)
        plot(x + across -1, y + i)
    
############################################################

def drawtile(x, y, across, deep, border):
    while border > 0:
        drawbox(x, y, across, deep)
        x += 1
        y += 1
        across -= 2
        deep -= 2
        border -= 1

############################################################

def printpixels():
    global pixelsacross
    global pixelsdeep
    global pixels

    for y in range(0, pixelsdeep):
        for x in range(0, pixelsacross):
            if pixels[(y * pixelsacross) + x] == 0xFF:
                print(".", sep='', end='')
            elif pixels[(y * pixelsacross) + x] == 0:
                print("#", sep='', end='')
            else:
                print("?", sep='', end='')
        print("")

############################################################

def genfloortiles(ta, td, pa, pd, bp, image):
    global pixelsacross
    global pixelsdeep
    global pixels

    ### print("{} tiles across by {} tiles deep".format(ta, td))
    ### print("{} pixels across per tile / {} pixels deep per tile".format(pa, pd))
    ### print("{} pixels to border each tile".format(bp))

    pixelsacross = (ta * pa) + 1
    pixelsdeep   = td * pd

    pixels = bytearray(pixelsacross * pixelsdeep)

    ### print("{} total pixels will be in final image".format(len(pixels)))

    # change all pixels to white
    ### print("Blanking image")
    for x in range(1, pixelsacross):
        for y in range(0, pixelsdeep):
            unplot(x, y)
    ### printpixels()

    # draw the tiles
    ### print("Drawing tiles")
    for x in range(0, ta):
        for y in range(0, td):
            drawtile((x * pa) + 1, y * pd, pa, pd, bp)
    ###printpixels()

    ### print(pixels)

    ### print("Writing PNG file")
    writeimage(image)
    ### print("Done")

    return

############################################################

def nextfreefile(prefix, suffix):
    i = 1

    while True:
        filename = "{}{:04d}.{}".format(prefix, i, suffix)

        if os.path.exists(filename):
            i += 1
        else:
            break

    return filename

############################################################

def commandline():
    parser = argparse.ArgumentParser()

    parser.add_argument("--ta", help="number of tiles across the data hall", default=DEFAULT_TILES_ACROSS)
    parser.add_argument("--td", help="number of tiles deep into the data hall", default=DEFAULT_TILES_DEEP)
    parser.add_argument("--pa", help="number of pixels across per tile", default=DEFAULT_PIXELS_ACROSS)
    parser.add_argument("--pd", help="number of pixels deep per tile", default=DEFAULT_PIXELS_DEEP)
    parser.add_argument("--bp", help="number of pixels to border each tile", default=DEFAULT_BORDER_PIXELS)
    parser.add_argument("--image", help="image file name", default=DEFAULT_IMAGE_FILE)

    args = parser.parse_args()

    ta = int(args.ta)
    td = int(args.td)
    pa = int(args.pa)
    pd = int(args.pd)
    bp = int(args.bp)
    image = args.image

    genfloortiles(ta, td, pa, pd, bp, image)

    return

############################################################

def htmlform():
    title = 'Create Data Centre floor tile PNG image'

    scriptname = os.path.basename(sys.argv[0])

    print('Content-type: text/html')
    print('')

    print('<head>');
    print('<title>{}</title>'.format(html.escape(title)))
    print('</head>');

    print('<body>')

    print('<h1>{}</h1>'.format(html.escape(title)))

    form = cgi.FieldStorage()

    ta = form.getfirst("ta", DEFAULT_TILES_ACROSS)
    td = form.getfirst("td", DEFAULT_TILES_DEEP)
    pa = form.getfirst("pa", DEFAULT_PIXELS_ACROSS)
    pd = form.getfirst("pd", DEFAULT_PIXELS_DEEP)
    bp = form.getfirst("bp", DEFAULT_BORDER_PIXELS)
    ### image = form.getfirst("image", "dcfloor.png")
   
    createimagebutton = form.getfirst("createimagebutton", "")

    print('<form method="post" action="{}">'.format(scriptname))

    print('<pre>')
    print('Number of tiles across the data hall: <input type="text" name="ta"    size="4"  value="{}">'.format(ta))
    print('<br>')
    print('Number of tiles deep into data hall:  <input type="text" name="td"    size="4"  value="{}">'.format(td))
    print('<br>')
    print('Number of pixels across per tile:     <input type="text" name="pa"    size="4"  value="{}">'.format(pa))
    print('<br>')
    print('Number of pixels deep per tile:       <input type="text" name="pd"    size="4"  value="{}">'.format(pd))
    print('<br>')
    print('Number of pixels to border each tile: <input type="text" name="bp"    size="4"  value="{}">'.format(bp))
    print('</pre>')
    print('<br>')
    print('<input type="submit" name="createimagebutton" value="Create PNG Image">')

    print('</form>')

    if createimagebutton != '':
        print('<pre>')
        print('Creating image ... ', end='')

        image = nextfreefile("floortiles", "png")
        genfloortiles(int(ta), int(td), int(pa), int(pd), int(bp), image)

        print('done')

        print('<br>')
        print('<a href="{}">Download the floor tile image</a>'.format(image))
        print('<br>')
        print('<img src="{}">'.format(image))
        print('</pre>')

    print('</body>')
    print('</html>')

    return

############################################################

#
# Main
#

try:
    gatewayinterface = os.environ['GATEWAY_INTERFACE']
except KeyError:
    gatewayinterface = ""

if gatewayinterface == "":
    commandline()
else:
    htmlform()

sys.exit(0)

############################################################

# end of file

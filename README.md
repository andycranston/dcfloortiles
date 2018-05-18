# dcfloortiles

A Python 3 program to create PNG images with tiles to represent a data
centre floor.

Look at the:

```
examplefloor.png
```

PNG image in the repository to get an idea.

It runs as a CGI script called `dcft.py` on a webserver with CGI scripting
enabled and a Python 3 interpreter available to the called CGI programs.

Alternatively it can be run from the command line (Windows and UNIX/Linux)
providing Python 3 is installed.

## How to get started - running on a webserver

Copy the `dcft.py` script to a directory on your
web server that contains CGI scripts - commonly a subdirectory
called `cgi-bin` under the main document root.

For example my webserver (lighttpd) has a document root:

```
/home/andyc/www
```

with a subdirectory:

```
/home/andyc/www/cgi-bin
```

for CGI scripts so I copy `dcft.py` to:

```
/home/andyc/www/cgi-bin/dcft.py
```

and make sure it is executable:

```
chmod a+x /home/andyc/www/cgi-bin/dcft.py
```

Now from a web browser I type the URL:

    http://mywebserver/cgi-bin/dcft.py

Note `mywebserver` is the hostname of the webserver.  Change
as appropriate for your environment.

One final thing!  The `cgi-bin` subdirectory must be writable by the
webserver process as it creates image files called:

```
floortiles0001.png
floortiles0002.png
floortiles0003.png
floortiles0004.png
etc.
```

in that directory.

If all is good when you access the URL you should get a page with content
similar to:

```
Create Data Centre floor tile PNG image

Number of tiles across the data hall: [8]
Number of tiles deep into data hall: [4]
Number of pixels across per tile: [60]
Number of pixels deep per tile: [60]
Number of pixels to border each tile: [2]

[[Create PNG Image]]
```

Click the `Create PNG Image` button and see what happens.

Change some of the values and click the button again.  Get the idea?

When you have a tile image you will find handy click the
`Download the floor tile image` link. It displays just the image and
from there you can use your browser to save the image to your
local storage.


## How to get started - running on the command line

NB: These instructions for command line usage assume
that typing `python` invokes the Python 3 interpreter.  If you
have different versions of Python coexisting in your environment
you may need to type `python3` instead of `python` in the
instructions below.

Copy the `dcft.py` script to a directory on your local machine.

From a command line window change to the directory where
you copied the script to and type:

```
python dcft.py
```

The program will create a file called:

```
floortiles.png
```

in the current directory.  Open this file using a graphical editor of
your choice.

To see the available command line arguments type:

```
python dcft.py -h
```

So running:

```
python dcft.py --ta 20 --td 10 --pa 32 --pd 32 --dp 4 --image mytiles.png
```

will create a file called `mytiles.png` with each tile measuring 32
pixels across by 32 pixel deep and 20 tiles across and 10 tiles deep.
The width of the tile border will be 4 pixels.

## Performance

The bigger an image you ask the script to create the longer it will take.
The image is created in memory as a Python byte array with one pixel
taking up one byte and then this data gets compressed using the zlib
library.  Big images take alot of memory, take time to create and more
memory and time to compress. Please be patient.

## "It breaks really easily!"

The code has minimal error checking so you can break it really easily.
If you think you have found a bug though please let me know - especially
in the PNG image creation part of the code.

## "It doesn't work on webserver XYZ"

I have only run this on `lighttpd` so it may not port to other
webservers but if you look at the code it doesn't do anything
particularly platform dependent so I don't expect there to be
any issues.

## Reference links

[Python 3 cgi - Common Gateway Interface support](https://docs.python.org/3/library/cgi.html)

[PNG (Portable Network Graphics) Specification, Version 1.2](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html)

[lighttpd webserver](http://www.lighttpd.net/)

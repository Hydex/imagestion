## http://docs.python.org/reference/index.html
from Imagen import *
#from array import *
#import thread

## http://luispedro.org/pymorph-apidocs/html/genindex.html
#from pymorph import *

## REALIZAR CAMBIOS EN: 
## sudo gedit /usr/lib/python2.6/dist-packages/PIL/Image.py
## http://hg.effbot.org/pil-2009-raclette/changeset/fb7ce579f5f9
##
##1494    def split(self):
##1495        "Split image into bands"
##1496
##1497        self.load()
##1498        if self.im.bands == 1:
##1499            ims = [self.copy()]
##1500        else:
##1501            ims = []
##1502            for i in range(self.im.bands):
##1503                ims.append(self._new(self.im.getband(i)))
##1504        return tuple(ims)


img = Imagen('../../webcam/img01.jpg')
print 'ancho:', img.getAncho() ,' alto:', img.getAlto()

#r = img.getR()
#g = img.getG()
#b = img.getB()

#r.show()
#g.show()
#b.show()

img.getRGB().show()

#g = img._erode(img.getG())
#G = img._erode(G)
#g = img._dilate(g)

#G.show()

#g.show()

img.dilate()

img.getRGB().show()

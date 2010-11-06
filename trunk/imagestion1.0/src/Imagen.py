# +-----------------------------------------------------------------------+
# | IMAGESTION                                                            |
# |                                                                       |
# | Copyright (C) 2010-Today, GNUCHILE.CL	- Santiago de Chile       |
# | Licensed under the GNU GPL                                            |
# |                                                                       |
# | Redistribution and use in source and binary forms, with or without    |
# | modification, are permitted provided that the following conditions    |
# | are met:                                                              |
# |                                                                       |
# | o Redistributions of source code must retain the above copyright      |
# |   notice, this list of conditions and the following disclaimer.       |
# | o Redistributions in binary form must reproduce the above copyright   |
# |   notice, this list of conditions and the following disclaimer in the |
# |   documentation and/or other materials provided with the distribution.|
# | o The names of the authors may not be used to endorse or promote      |
# |   products derived from this software without specific prior written  |
# |   permission.                                                         |
# |                                                                       |
# | THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS   |
# | "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT     |
# | LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR |
# | A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  |
# | OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, |
# | SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT      |
# | LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, |
# | DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY |
# | THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT   |
# | (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE |
# | OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  |
# |                                                                       |
# +-----------------------------------------------------------------------+
# | Author: Miguel Vargas Welch <miguelote@gmail.com>                     |
# +-----------------------------------------------------------------------+

import Image
import thread

## Referencias apoyo:
## http://www.pythonware.com/library/pil/handbook/introduction.htm
## http://www.pythonware.com/library/pil/handbook/image.htm
## http://www.tutorialspoint.com/python/python_multithreading.htm
## http://ostermiller.org/dilate_and_erode.html

class Imagen(object):
    
    def __init__(self,ruta):
        self.path = ruta
        self.busy = 0
        self.reload()
        pass
        
    def reload(self):
        self.RGB  = Image.open(self.path)
        self.ancho, self.alto  = self.RGB.size
        self.R, self.G, self.B = self.RGB.split()
        pass
        
    def dilate(self):
        self.busy = 3

        try:
           thread.start_new_thread( self._dilate, ([self.R, None], 0, 0, self.alto, self.ancho) )
           thread.start_new_thread( self._dilate, (self.G, 'G', 0, 0, self.alto, self.ancho) )
           thread.start_new_thread( self._dilate, (self.B, 'B', 0, 0, self.alto, self.ancho) )
        except:
           print "Error: unable to start thread"

        while self.busy > 0:
           pass

        print self.busy

    def erode(self):
        self.busy = 3

        try:
           thread.start_new_thread( self._erode, (self.R, 'R') )
           thread.start_new_thread( self._erode, (self.G, 'G') )
           thread.start_new_thread( self._erode, (self.B, 'B') )
        except:
           print "Error: unable to start thread"

        while self.busy > 0:
           pass

        print self.busy
        
    def _dilate(self, im, y1, x1, y2, x2):
        """
         
        @return  :
        @author
        """
        print "tarea dilate "
        print self.busy
        copia = im.copy()
        
        for y in range(self.alto):
            for x in range(self.ancho):
                punto = im.getpixel((x,y))
                ##norte = im.getpixel((x,y-1))
                ##sur   = im.getpixel((x,y+1))
                ##este  = im.getpixel((x+1,y))
                ##oeste = im.getpixel((x-1,y))

                if y>0 and punto>im.getpixel((x,y-1)):
                    copia.putpixel((x,y-1),punto)
                    
                if x>0 and punto>im.getpixel((x-1,y)):
                    copia.putpixel((x-1,y),punto)
        
                if y<self.alto-1 and punto>im.getpixel((x,y+1)):
                    copia.putpixel((x,y+1),punto)
                    
                if x<self.ancho-1 and punto>im.getpixel((x+1,y)):
                    copia.putpixel((x+1,y),punto)

        self.busy = self.busy -1
        print "fin tarea "+mapa+" "
        print self.busy

#        if mapa == 'R':
#            self.R = copia
#            return
#
#        if mapa == 'G':
#            self.G = copia
#            return
#
#        if mapa == 'B':
#            self.B = copia
#            return

        return im2

    def _erode(self,im, mapa, y1, x1, y2, x2):
        """
         
        @return  :
        @author
        """
        print "tarea erode "+mapa+" "
        print self.busy

        im2 = im.copy()
        
        for y in range(self.alto):
            for x in range(self.ancho):
                punto = im.getpixel((x,y))
                ##norte = im.getpixel((x,y-1))
                ##sur   = im.getpixel((x,y+1))
                ##este  = im.getpixel((x+1,y))
                ##oeste = im.getpixel((x-1,y))

                if y>0 and punto>im.getpixel((x,y-1)):
                    im2.putpixel((x,y),im.getpixel((x,y-1)))
                    
                if x>0 and punto>im.getpixel((x-1,y)):
                    im2.putpixel((x,y),im.getpixel((x-1,y)))
        
                if y<self.alto-1 and punto>im.getpixel((x,y+1)):
                    im2.putpixel((x,y),im.getpixel((x,y+1)))
                    
                if x<self.ancho-1 and punto>im.getpixel((x+1,y)):
                    im2.putpixel((x,y),im.getpixel((x+1,y)))

        self.busy = self.busy -1
        print "fin tarea "+mapa+" "
        print self.busy

        if mapa == 'R':
            self.R = im2
            return

        if mapa == 'G':
            self.G = im2
            return

        if mapa == 'B':
            self.B = im2
            return

        return im2

    def rgb2gray(self):
        """
         
        @return  :
        @author
        """
        pass

    def getR(self):
        """
         
        @return int[][] :
        @author
        """
        return self.R
        pass

    def getG(self):
        """
         
        @return int[][] :
        @author
        """
        return self.G
        pass

    def getB(self):
        """
         
        @return int[][] :
        @author
        """
        return self.B
        pass

    def getRGB(self):
        """
         
        @return int[][][3] :
        @author
        """
        self.RGB = Image.merge("RGB", (self.R, self.G, self.B))
        return self.RGB
        pass

    def getAlto(self):
        return self.alto
        pass

    def getAncho(self):
        return self.ancho
        pass
    
    def getPath(self):
        return self.path
        pass

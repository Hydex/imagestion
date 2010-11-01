import Image
import thread

## http://www.pythonware.com/library/pil/handbook/introduction.htm
## http://www.pythonware.com/library/pil/handbook/image.htm
## http://www.tutorialspoint.com/python/python_multithreading.htm

class Imagen(object):
    
    def __init__(self,ruta):
        self.path = ruta
        self.reload()
        pass
        
    def reload(self):
        self.RGB  = Image.open(self.path)
        self.ancho, self.alto  = self.RGB.size
        self.R, self.G, self.B = self.RGB.split()
        pass
        
    def dilate(self):
        try:
           self.R = thread.start_new_thread( self._dilate, (self.R) )
           self.G = thread.start_new_thread( self._dilate, (self.G) )
           self.B = thread.start_new_thread( self._dilate, (self.B) )
        except:
           print "Error: unable to start thread"
        pass

    def erode(self):
        try:
           self.R = thread.start_new_thread( self._erode, (self.R) )
           self.G = thread.start_new_thread( self._erode, (self.G) )
           self.B = thread.start_new_thread( self._erode, (self.B) )
        except:
           print "Error: unable to start thread"
        pass
        
    def _dilate(self, im):
        """
         
        @return  :
        @author
        """
        pass
        im2 = im.copy()
        
        for y in range(self.alto):
            for x in range(self.ancho):
                punto = im.getpixel((x,y))
                ##norte = im.getpixel((x,y-1))
                ##sur   = im.getpixel((x,y+1))
                ##este  = im.getpixel((x+1,y))
                ##oeste = im.getpixel((x-1,y))

                if y>0 and punto>im.getpixel((x,y-1)):
                    im2.putpixel((x,y-1),punto)
                    
                if x>0 and punto>im.getpixel((x-1,y)):
                    im2.putpixel((x-1,y),punto)
        
                if y<self.alto-1 and punto>im.getpixel((x,y+1)):
                    im2.putpixel((x,y+1),punto)
                    
                if x<self.ancho-1 and punto>im.getpixel((x+1,y)):
                    im2.putpixel((x+1,y),punto)
        return im2

    def _erode(self,im):
        """
         
        @return  :
        @author
        """
        pass
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

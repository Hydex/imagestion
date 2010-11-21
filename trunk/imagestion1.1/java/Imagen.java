/*-----------------------------------------------------------------------*\
 | IMAGESTION                                                            |
 |                                                                       |
 | Copyright (C) 2010-Today, GNUCHILE.CL       - Santiago de Chile       |
 | Licensed under the GNU GPL                                            |
 |                                                                       |
 | Redistribution and use in source and binary forms, with or without    |
 | modification, are permitted provided that the following conditions    |
 | are met:                                                              |
 |                                                                       |
 | o Redistributions of source code must retain the above copyright      |
 |   notice, this list of conditions and the following disclaimer.       |
 | o Redistributions in binary form must reproduce the above copyright   |
 |   notice, this list of conditions and the following disclaimer in the |
 |   documentation and/or other materials provided with the distribution.|
 | o The names of the authors may not be used to endorse or promote      |
 |   products derived from this software without specific prior written  |
 |   permission.                                                         |
 |                                                                       |
 | THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS   |
 | "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT     |
 | LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR |
 | A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  |
 | OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, |
 | SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT      |
 | LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, |
 | DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY |
 | THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT   |
 | (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE |
 | OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  |
 |                                                                       |
 *-----------------------------------------------------------------------*
 | Author: Miguel Vargas Welch <miguelote@gmail.com>                     |
\*-----------------------------------------------------------------------*/


import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;

/**
 * Class Imagen
 */
public class Imagen
{
    private static final int COPIAR = 1;
    private static final int ERODE  = 2;
    private static final int DILATE = 3;
    private static final int BORDER = 4;
    private static final int JOIN   = 5;

  //
  // Fields
  //

    private String path;
    private int alto;
    private int ancho;
    protected int[][] R;
    protected int[][] G;
    protected int[][] B;
    private int[][] gray;
    private Image RGB;
    private static BufferedImage imagen;
    private int busy;
    public static int instancia = 0;

    protected class Layer extends Thread
    {
        char frame;
        int y1;
        int x1;
        int y2;
        int x2;
        int accion = 0;
        
        public Layer(int action, char _frame, int _y1, int _x1, int _y2, int _x2)
        {
            frame  = _frame;
            y1     = _y1;
            x1     = _x1;
            y2     = _y2;
            x2     = _x2;
            accion = action;
        }

        public void copy()
        {
            int mask;
            instancia++;

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    int pixel = imagen.getRGB(y, x);
                    int color = 0;

                    switch (frame)
                    {
                        case 'R':
                          mask = 0xFF0000;
                          color = pixel & mask;
                          color >>= 16;
                          R[y][x] = color;
                          break;
                        case 'G':
                          mask = 0x00FF00;
                          color = pixel & mask;
                          color >>= 8;
                          G[y][x] = color;
                          break;
                        case 'B':
                          mask = 0x0000FF;
                          color = pixel & mask;
                          B[y][x] = color;
                          break;
                    }
                }

            instancia--;

            if(instancia == 1)
                instancia = 0;
        }

        public void joint()
        {
            instancia++;

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    int colorR = R[y][x];
                    int colorG = G[y][x];
                    int colorB = B[y][x];

                    colorR <<= 16;
                    colorG <<= 8;

                    int color = colorR | colorG | colorB;

                    imagen.setRGB(x, y, color);
                }

            instancia--;

            if(instancia == 1)
                instancia = 0;
        }

        public void dilate()
        {
            int mask,color,punto;
            int n,ne,e,se,s,so,o,no;

            instancia++;

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    ne = se = so = no = 0;
                    n  = s  = e  = o  = 0;
                    color = punto = 0;
                    mask  = frame == 'R' ?0xFF0000
                           :frame == 'G' ?0x00FF00
                                         :0x0000FF;

                    int pixel = mask & imagen.getRGB(y, x);

                    if(y>0)                n  = mask & imagen.getRGB(y-1,x);
                    if(y<alto)             s  = mask & imagen.getRGB(y+1,x);
                    if(x>0)                o  = mask & imagen.getRGB(y,x-1);
                    if(x<ancho)            e  = mask & imagen.getRGB(y,x+1);
                    if(y>0 && x>0)         no = mask & imagen.getRGB(y-1,x-1);
                    if(y<alto && x>0)      so = mask & imagen.getRGB(y+1,x-1);
                    if(y>0 && x<ancho)     ne = mask & imagen.getRGB(y-1,x+1);
                    if(y<alto && x<ancho)  se = mask & imagen.getRGB(y+1,x+1);

                    switch (frame)
                    {
                        case 'R':
                            pixel >>= 16;
                            n  >>= 16;
                            s  >>= 16;
                            o  >>= 16;
                            e  >>= 16;
                            no >>= 16;
                            so >>= 16;
                            ne >>= 16;
                            se >>= 16;

                            if(y>0 && pixel>n)                     R[y-1][x]   = pixel;
                            if(x>0 && pixel>o)                     R[y][x-1]   = pixel;
                            if(y<alto-1 && pixel>s)                R[y+1][x]   = pixel;
                            if(x<ancho-1 && pixel>e)               R[y][x+1]   = pixel;
                            if(y>0 && x>0 && pixel>no)             R[y-1][x-1] = pixel;
                            if(y>0 && x<ancho-1 && pixel>ne)       R[y-1][x+1] = pixel;
                            if(y<alto-1 && x>0 && pixel>so)        R[y+1][x-1] = pixel;
                            if(y<alto-1 && x<ancho-1 && pixel>se)  R[y+1][x+1] = pixel;

                            break;
                        case 'G':
                            pixel >>= 8;
                            n  >>= 8;
                            s  >>= 8;
                            o  >>= 8;
                            e  >>= 8;
                            no >>= 8;
                            so >>= 8;
                            ne >>= 8;
                            se >>= 8;

                            if(y>0 && pixel>n)                     G[y-1][x]   = pixel;
                            if(x>0 && pixel>o)                     G[y][x-1]   = pixel;
                            if(y<alto-1 && pixel>s)                G[y+1][x]   = pixel;
                            if(x<ancho-1 && pixel>e)               G[y][x+1]   = pixel;
                            if(y>0 && x>0 && pixel>no)             G[y-1][x-1] = pixel;
                            if(y>0 && x<ancho-1 && pixel>ne)       G[y-1][x+1] = pixel;
                            if(y<alto-1 && x>0 && pixel>so)        G[y+1][x-1] = pixel;
                            if(y<alto-1 && x<ancho-1 && pixel>se)  G[y+1][x+1] = pixel;

                            break;
                        case 'B':
                            if(y>0 && pixel>n)                     B[y-1][x]   = pixel;
                            if(x>0 && pixel>o)                     B[y][x-1]   = pixel;
                            if(y<alto-1 && pixel>s)                B[y+1][x]   = pixel;
                            if(x<ancho-1 && pixel>e)               B[y][x+1]   = pixel;
                            if(y>0 && x>0 && pixel>no)             B[y-1][x-1] = pixel;
                            if(y>0 && x<ancho-1 && pixel>ne)       B[y-1][x+1] = pixel;
                            if(y<alto-1 && x>0 && pixel>so)        B[y+1][x-1] = pixel;
                            if(y<alto-1 && x<ancho-1 && pixel>se)  B[y+1][x+1] = pixel;

                            break;
                    }

                }

            instancia--;

            if(instancia == 1)
                instancia = 0;
        }

        public void run()
        {
            int alto    = y2 - y1;
            int ancho   = x2 - x1;
            int difY    = alto  % 2;
            int difX    = ancho % 2;
            int offsetY = difY==0 ?alto/2  :(alto/2)+difY;
            int offsetX = difX==0 ?ancho/2 :(ancho/2)+difX;

            try
            {
                if(alto > 100 && ancho > 100)
                {
                    Layer ne = new Layer(accion,frame,y1,x1,y2+offsetY,x2-offsetX);
                    Layer no = new Layer(accion,frame,y1,x1+offsetX,y2-offsetY,x2);
                    Layer se = new Layer(accion,frame,y1+offsetY,x1,y2,x2-offsetX);
                    Layer so = new Layer(accion,frame,y1+offsetY,x1+offsetX,y2,x2);

                    ne.start();
                    no.start();
                    se.start();
                    so.start();
                }
                else
                    switch(accion)
                    {
                        case COPIAR:
                            copy();
                            break;
                        case ERODE:
                            break;
                        case DILATE:
                            break;
                        case BORDER:
                            break;
                        case JOIN:
                            joint();
                            break;
                    }
            }
            catch(Exception ex)
            {
                Logger.getLogger(Layer.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

  //
  // Constructors
  //

    public Imagen (String ruta) throws IOException
    {
        path    = ruta;
        imagen  = ImageIO.read(new File(this.path));
        alto    = imagen.getHeight();
        ancho   = imagen.getWidth();
        busy    = 0;
        reload();
    };

    public void reload()
    {
        instancia = 1;

//        try
//        {
            Layer Red   = new Layer(COPIAR, 'R', 0, 0, alto, ancho);
            Layer Green = new Layer(COPIAR, 'G', 0, 0, alto, ancho);
            Layer Blue  = new Layer(COPIAR, 'B', 0, 0, alto, ancho);

            Red.start();
            Green.start();
            Blue.start();

            while(instancia > 0) {}
//        }
//        catch(Exception ex)
//        {
//            Logger.getLogger(Imagen.class.getName()).log(Level.SEVERE, null, ex);
//        }
    }



  //
  // Methods
  //

    public void guardar(String nombre) throws IOException
    {
        /* "png" "jpeg" format desired, no "gif" yet. */
        ImageIO.write( imagen, "jpeg" , new File ( nombre ) );
    }
    
  //
  // Accessor methods
  //

  /**
   * Set the value of path
   * @param newVar the new value of path
   */
    
  public void setPath ( String newVar ) {
    path = newVar;
  }

  /**
   * Get the value of path
   * @return the value of path
   */
  public String getPath ( ) {
    return path;
  }

  /**
   * Set the value of alto
   * @param newVar the new value of alto
   */
  public void setAlto ( int newVar ) {
    alto = newVar;
  }

  /**
   * Get the value of alto
   * @return the value of alto
   */
  public int getAlto ( ) {
    return alto;
  }

  /**
   * Set the value of ancho
   * @param newVar the new value of ancho
   */
  public void setAncho ( int newVar ) {
    ancho = newVar;
  }

  /**
   * Get the value of ancho
   * @return the value of ancho
   */
  public int getAncho ( ) {
    return ancho;
  }

  /**
   * Set the value of R
   * @param newVar the new value of R
   */
  public void setR ( int[][] newVar ) {
    R = newVar;
  }

  /**
   * Get the value of R
   * @return the value of R
   */
  public int[][] getR ( ) {
    return R;
  }

  /**
   * Set the value of G
   * @param newVar the new value of G
   */
  public void setG ( int[][] newVar ) {
    G = newVar;
  }

  /**
   * Get the value of G
   * @return the value of G
   */
  public int[][] getG ( ) {
    return G;
  }

  /**
   * Set the value of B
   * @param newVar the new value of B
   */
  public void setB ( int[][] newVar ) {
    B = newVar;
  }

  /**
   * Get the value of B
   * @return the value of B
   */
  public int[][] getB ( ) {
    return B;
  }

  /**
   * Set the value of gray
   * @param newVar the new value of gray
   */
  public void setGray ( int[][] newVar ) {
    gray = newVar;
  }

  /**
   * Get the value of gray
   * @return the value of gray
   */
  public int[][] getGray ( ) {
    return gray;
  }

  /**
   * Set the value of RGB
   * @param newVar the new value of RGB
   */
  public void setRGB ( Image newVar ) {
    RGB = newVar;
  }

  /**
   * Get the value of RGB
   * @return the value of RGB
   */
  public Image getRGB ( ) {
    return RGB;
  }

  //
  // Other methods
  //

  /**
   * @param        path
   */
  public void load( String path )
  {
  }


  /**
   */
  public void erode(  )
  {
  }


  /**
   */
  public void dilate(  )
  {
      instancia = 1;

  }


  /**
   */
  public void rgb2gray(  )
  {
  }

}

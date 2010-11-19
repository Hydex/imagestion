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


    protected class Layer extends Thread
    {
        char frame;
        int[][] map;
        int y1;
        int x1;
        int y2;
        int x2;
        
        public Layer(char _frame, int[][] _map, int _y1, int _x1, int _y2, int _x2)
        {
            frame = _frame;
            map   = _map;
            y1    = _y1;
            x1    = _x1;
            y2    = _y2;
            x2    = _x2;
        }

        public void copy()
        {
            int mask;

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
                          break;
                        case 'G':
                          mask = 0x00FF00;
                          color = pixel & mask;
                          color >>= 8;
                          break;
                        case 'B':
                          mask = 0x0000FF;
                          color = pixel & mask;
                          break;
                    }

                    map[y][x] = color;
                }
        }

        public void run()
        {

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
        Layer Red   = new Layer('R', R, 0, 0, alto, ancho);
        Layer Green = new Layer('G', G, 0, 0, alto, ancho);
        Layer Blue  = new Layer('B', B, 0, 0, alto, ancho);

        Red.start();
        Green.start();
        Blue.start();
    }



  //
  // Methods
  //

    public void Guardar(String nombre) throws IOException
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
  }


  /**
   */
  public void rgb2gray(  )
  {
  }

}

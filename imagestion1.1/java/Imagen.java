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
    protected Integer[][] R;
    protected Integer[][] G;
    protected Integer[][] B;
    private Image RGB;
    private static BufferedImage imagen;
    protected static int instancia = 0;
    public boolean debug = false;

    protected class Layer extends Thread
    {
        char frame;
        int y1;
        int x1;
        int y2;
        int x2;
        int accion = 0;
        int id;
        
        public Layer(int action, char _frame, int _y1, int _x1, int _y2, int _x2)
        {
            frame  = _frame;
            y1     = _y1;
            x1     = _x1;
            y2     = _y2;
            x2     = _x2;
            accion = action;
            id     = instancia;
            if(debug) System.out.println("ID:"+id+" - Layer(act:"+accion+",frm:"+frame+",y1:"+y1+",x1:"+x1+",y2:"+y2+",x2:"+x2+")");
        }

        public void copy()
        {
            int mask;
            int x = 0;
            int y = 0;
            String msg = "";

            if(debug) System.out.println("ID:"+id+" - Layer.copy - act:"+accion+" - Instancia:"+instancia+" IN");

            try
            {
                for(y=y1; y<y2; y++)
                    for(x=x1; x<x2; x++)
                    {
                        int pixel = imagen.getRGB(x,y);
                        R[y][x] = pixel & 0xFF0000;
                        G[y][x] = pixel & 0x00FF00;
                        B[y][x] = pixel & 0x0000FF;
                    }
            }
            catch(Exception ex)
            {
                System.out.println("ID:"+id+" - Layer.copy - Instancia:"+instancia+" ERROR: frm:"+frame+",y1:"+y1+",x1:"+x1+",y2:"+y2+",x2:"+x2+" [y:"+y+",x:"+x+"] "+ex.getMessage());
                Logger.getLogger(Layer.class.getName()).log(Level.SEVERE, null, ex);
                msg = " with error";
            }
        }

        public void joint()
        {
            int x=0, y=0;
            String msg = "";

            if(debug) System.out.println("ID:"+id+" - Layer.joint - act:"+accion+" - Instancia:"+instancia+" IN");

            try
            {
                for(y=y1; y<y2; y++)
                    for(x=x1; x<x2; x++)
                    {
                        int colorR = R[y][x];
                        int colorG = G[y][x];
                        int colorB = B[y][x];

                        colorR <<= 16;
                        colorG <<= 8;

                        int color = colorR | colorG | colorB;

                        imagen.setRGB(x, y, color);
                    }
            }
            catch(Exception ex)
            {
                System.out.println("ID:"+id+" - Layer.joint - Instancia:"+instancia+" ERROR: y1:"+y1+",x1:"+x1+",y2:"+y2+",x2:"+x2+" [y:"+y+",x:"+x+"] "+ex.getMessage());
                Logger.getLogger(Layer.class.getName()).log(Level.SEVERE, null, ex);
                msg = " with error";
            }
        }

        public void dilate()
        {
            int maskR = 0xFF0000;
            int maskG = 0x00FF00;
            int maskB = 0x0000FF;

            if(debug) System.out.println("ID:"+id+" - Layer.dilate - act:"+accion+" - Instancia:"+instancia+" IN");

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    int pixel  = imagen.getRGB(x,y);
                    int pixelR = pixel & maskR;
                    int pixelG = pixel & maskG;
                    int pixelB = pixel & maskB;

                    if(y>0)                    
                    {
                        int color = 0;                   
                        int pix = imagen.getRGB(x,y-1);
                        int n[] = {pix&maskR, pix&maskG, pix&maskB};
                        //int n[] = {R[y-1][x], G[y-1][x], B[y-1][x]};
                         
                        R[y-1][x]= (pixelR > n[0]) ?pixelR :n[0];
                        G[y-1][x]= (pixelG > n[1]) ?pixelG :n[1];
                        B[y-1][x]= (pixelB > n[2]) ?pixelB :n[2];
                        
                        //imagen.setRGB(x,y-1,color);
                    }

                    if(y<alto-1)
                    {
                        int color = 0;
                        int pix = imagen.getRGB(x,y+1);
                        int s[] = {pix&maskR, pix&maskG, pix&maskB};
                        //int s[] = {R[y+1][x], G[y+1][x], B[y+1][x]};
                        
                        R[y+1][x]= (pixelR > s[0]) ?pixelR :s[0];
                        G[y+1][x]= (pixelG > s[1]) ?pixelG :s[1];
                        B[y+1][x]= (pixelB > s[2]) ?pixelB :s[2];
                        
                        //imagen.setRGB(x,y+1,color);
                    }

                    if(x>0)
                    {
                        int color = 0;
                        int pix = imagen.getRGB(x-1,y);
                        int o[] = {pix&maskR, pix&maskG, pix&maskB};
                        //int o[] = {R[y][x-1], G[y][x-1], B[y][x-1]};
                        
                        R[y][x-1]= (pixelR > o[0]) ?pixelR :o[0];
                        G[y][x-1]= (pixelG > o[1]) ?pixelG :o[1];
                        B[y][x-1]= (pixelB > o[2]) ?pixelB :o[2];
                        
                        //imagen.setRGB(x-1,y,color);
                    }

                    if(x<ancho-1)
                    {
                        int color = 0;
                        int pix = imagen.getRGB(x+1,y);
                        int e[] = {pix&maskR, pix&maskG, pix&maskB};
                        //int e[] = {R[y][x+1], G[y][x+1], B[y][x+1]};
                        
                        R[y][x+1]= (pixelR > e[0]) ?pixelR :e[0];
                        G[y][x+1]= (pixelG > e[1]) ?pixelG :e[1];
                        B[y][x+1]= (pixelB > e[2]) ?pixelB :e[2];
                        
                        //imagen.setRGB(x+1,y,color);
                    }

//                    if(y>0 && x>0)
//                    {
//                        int color = 0;
//                        int pix = imagen.getRGB(x-1,y-1);
//                        int no[] = {pix&maskR, pix&maskG, pix&maskB};
//
//                        if(R[y][x]>(no[0]&maskR)) color |= colR;
//                        if(G[y][x]>(no[1]&maskG)) color |= colG;
//                        if(B[y][x]>(no[2]&maskB)) color |= colB;
//
//                        imagen.setRGB(x-1,y-1,color);
//                    }
//
//                    if(y<alto-1 && x>0)
//                    {
//                        int color = 0;
//                        int pix = imagen.getRGB(x-1,y+1);
//                        int so[] = {pix&maskR, pix&maskG, pix&maskB};
//
//                        if(R[y][x]>(so[0]&maskR)) color |= colR;
//                        if(G[y][x]>(so[1]&maskG)) color |= colG;
//                        if(B[y][x]>(so[2]&maskB)) color |= colB;
//
//                        imagen.setRGB(x-1,y+1,color);
//                    }
//
//                    if(y>0 && x<ancho-1){
//                        int color = 0;
//                        int pix = imagen.getRGB(x+1,y-1);
//                        int ne[] = {pix&maskR, pix&maskG, pix&maskB};
//
//                        if(R[y][x]>(ne[0]&maskR)) color |= colR;
//                        if(G[y][x]>(ne[1]&maskG)) color |= colG;
//                        if(B[y][x]>(ne[2]&maskB)) color |= colB;
//
//                        imagen.setRGB(x+1,y-1,color);
//                    }
//
//                    if(y<alto-1 && x<ancho-1)
//                    {
//                        int color = 0;
//                        int pix = imagen.getRGB(x+1,y+1);
//                        int se[] = {pix&maskR, pix&maskG, pix&maskB};
//
//                        if(R[y][x]>(se[0]&maskR)) color |= colR;
//                        if(G[y][x]>(se[1]&maskG)) color |= colG;
//                        if(B[y][x]>(se[2]&maskB)) color |= colB;
//
//                        imagen.setRGB(x+1,y+1,color);
//                    }
                }
        }

        @Override
        public void run()
        {
            int alto    = y2 - y1;
            int ancho   = x2 - x1;
            int difY    = alto  % 2;
            int difX    = ancho % 2;
            int offsetY = alto/2;  //difY==0 ?alto/2  :(alto/2)+difY;
            int offsetX = ancho/2; //difX==0 ?ancho/2 :(ancho/2)+difX;
            String method = "";

            try
            {
                if(alto > 100 && ancho > 100)
                {
                    Layer ne = new Layer(accion,frame,y1,x1,y2-offsetY,x2-offsetX);
                    Layer no = new Layer(accion,frame,y1,x1+offsetX,y2-offsetY,x2);
                    Layer se = new Layer(accion,frame,y1+offsetY,x1,y2,x2-offsetX);
                    Layer so = new Layer(accion,frame,y1+offsetY,x1+offsetX,y2,x2);

                    ne.start();
                    no.start();
                    se.start();
                    so.start();
                }
                else
                {
                    instancia++;

                    switch(accion)
                    {
                        case COPIAR:
                            copy();
                            method = "Layer.copy";
                            break;
                        case ERODE:
                            break;
                        case DILATE:
                            dilate();
                            method = "Layer.dilate";
                            break;
                        case BORDER:
                            break;
                        case JOIN:
                            joint();
                            method = "Layer.joint";
                            break;
                    }

                    instancia--;
                    if(debug) System.out.println("ID:"+id+" - "+method+" - act:"+accion+" - Instancia:"+instancia+" OUT");

                    if(instancia == 1)
                        instancia = 0;
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
        R       = new Integer[alto][ancho];
        G       = new Integer[alto][ancho];
        B       = new Integer[alto][ancho];
        reload();
    };

    public void reload()
    {
        instancia = 1;
        if(debug) System.out.println("Imagen.reload - Instancia:"+instancia+" IN");

        Layer img   = new Layer(COPIAR, ' ', 0, 0, alto, ancho);
        img.start();

        while(instancia > 0) {}

        if(debug) System.out.println("Imagen.reload - Instancia:"+instancia+" OUT");
    }

    private void join()
    {
        instancia = 1;
        if(debug) System.out.println("Imagen.join - Instancia:"+instancia+" IN");

        Layer rgb = new Layer(JOIN  , ' ', 0, 0, alto, ancho);
        rgb.start();

        while(instancia > 0) {}

        if(debug) System.out.println("Imagen.join - Instancia:"+instancia+" OUT");
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
  public void setR ( Integer[][] newVar ) {
    R = newVar;
  }

  /**
   * Get the value of R
   * @return the value of R
   */
  public Integer[][] getR ( ) {
    return R;
  }

  /**
   * Set the value of G
   * @param newVar the new value of G
   */
  public void setG ( Integer[][] newVar ) {
    G = newVar;
  }

  /**
   * Get the value of G
   * @return the value of G
   */
  public Integer[][] getG ( ) {
    return G;
  }

  /**
   * Set the value of B
   * @param newVar the new value of B
   */
  public void setB ( Integer[][] newVar ) {
    B = newVar;
  }

  /**
   * Get the value of B
   * @return the value of B
   */
  public Integer[][] getB ( ) {
    return B;
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
        if(debug) System.out.println("Imagen.dilate - Instancia:"+instancia+" IN");

        Layer color = new Layer(DILATE, ' ', 0, 0, alto, ancho);
        color.start();

        while(instancia > 0) {}

        join();

//        Layer img   = new Layer(COPIAR, ' ', 0, 0, alto, ancho);
//        img.start();
//
//        while(instancia > 0) {}

        if(debug) System.out.println("Imagen.dilate - Instancia:"+instancia+" OUT");
  }


  /**
   */
  public void rgb2gray(  )
  {
  }

}

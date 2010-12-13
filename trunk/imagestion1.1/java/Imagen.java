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
    enum operacion {UNDEFINED, COPIAR, ERODE, QERODE, DILATE, QDILATE, BORDER, JOIN};

  //
  // Fields
  //

    private String path;
    private int alto;
    private int ancho;
    protected Integer[][] R;
    protected Integer[][] G;
    protected Integer[][] B;
    protected Integer[][] struct;
    protected int structWd;
    protected int structHg;
    private Image RGB;
    private static BufferedImage imagen;
    protected static int instancia = 0;
    public boolean debug = false;

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
        struct  = new Integer[1][1];
        struct[0][0] = 1;
        structWd = 1;
        structHg = 1;

        reload();
    };

    private Imagen() {  }

    protected class Layer extends Thread
    {
        char frame;
        int y1;
        int x1;
        int y2;
        int x2;
        operacion accion = operacion.UNDEFINED;
        int id;
        
        public Layer(operacion action, char _frame, int _y1, int _x1, int _y2, int _x2)
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

        private void setPunto(int x, int y, char frame, int pixel)
        {
            int height = structHg;
            int width  = structWd;
            int i=0, j=0;
            int cy     = height>1     ?height/2 :0;
            int cx     = width>1      ?width/2  :0;

            for(i=0; i<height; i++)
                for(j=0; j<width; j++)
                    switch(frame)
                    {
                        case 'R':
                            if(struct[i][j]>0)
                                if(0 < y+i-cy && 0 < x+j-cx && alto > y+i-cy && ancho > x+j-cx)
                                    R[y+i-cy][x+j-cx] = pixel;
                            break;
                        case 'G':
                            if(struct[i][j]>0)
                                if(0 < y+i-cy && 0 < x+j-cx && alto > y+i-cy && ancho > x+j-cx)
                                    G[y+i-cy][x+j-cx] = pixel;
                            break;
                        case 'B':
                            if(struct[i][j]>0)
                                if(0 < y+i-cy && 0 < x+j-cx && alto > y+i-cy && ancho > x+j-cx)
                                    B[y+i-cy][x+j-cx] = pixel;
                            break;
                    }
        }

        private int getMinimo(int x, int y, char frame)
        {
            int height = structHg;
            int width  = structWd;
            int cy     = height>1     ?height/2 :0;
            int cx     = width>1      ?width/2  :0;
            int mask   = frame == 'R' ?0xFF0000
                        :frame == 'G' ?0x00FF00
                                      :0x0000FF;
            int min    = mask;

            for(int i=0; i<height; i++)
                for(int j=0; j<width; j++)
                    if(struct[i][j]>0)
                        if(0 < y+i-cy && 0 < x+j-cx && alto > y+i-cy && ancho > x+j-cx)
                        {
                            int pixel = mask & imagen.getRGB(x+j-cx,y+i-cy);
                            min = min > pixel ?pixel :min;
                        }

            return min;
        }

        private int getMaximo(int x, int y, char frame)
        {
            int height = structHg;
            int width  = structWd;
            int cy     = height>1 ?height/2 :0;
            int cx     = width>1  ?width/2  :0;
            int mask   = frame == 'R' ?0xFF0000
                        :frame == 'G' ?0x00FF00
                                      :0x0000FF;
            int max    = 0;

            for(int i=0; i<height; i++)
                for(int j=0; j<width; j++)
                    if(struct[i][j]>0)
                        if(0 < y+i-cy && 0 < x+j-cx && alto > y+i-cy && ancho > x+j-cx)
                        {
                            int pixel = mask & imagen.getRGB(x+j-cx,y+i-cy);
                            max = max < pixel ?pixel :max;
                        }

            return max;
        }

        public void dilate()
        {
            int despX = structWd;
            int despY = structHg;

            if(debug) System.out.println("ID:"+id+" - Layer.dilate - act:"+accion+" - Instancia:"+instancia+" IN");

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    int color = getMaximo(x,y,frame);
                    setPunto(x,y,frame,color);
                }

            if(debug) System.out.println("ID:"+id+" - Layer.dilate - act:"+accion+" - Instancia:"+instancia+" OUT");
        }

        public void erode()
        {
            int despX = structWd;
            int despY = structHg;

            if(debug) System.out.println("ID:"+id+" - Layer.dilate - act:"+accion+" - Instancia:"+instancia+" IN");

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    int color = getMinimo(x,y,frame);
                    setPunto(x,y,frame,color);
                }

            if(debug) System.out.println("ID:"+id+" - Layer.dilate - act:"+accion+" - Instancia:"+instancia+" OUT");
        }

        public void dilate_quick()
        {
            int maskR = 0xFF0000;
            int maskG = 0x00FF00;
            int maskB = 0x0000FF;

            if(debug) System.out.println("ID:"+id+" - Layer.dilate - act:"+accion+" - Instancia:"+instancia+" IN");

            for(int y=y1; y<y2; y++)
                for(int x=x1; x<x2; x++)
                {
                    int pixel  = imagen.getRGB(x,y);
                    int pixelR = R[y][x];
                    int pixelG = G[y][x];
                    int pixelB = B[y][x];

                    if(x>0)
                    {
                        int col[] = {R[y][x-1], G[y][x-1], B[y][x-1]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x-1,y,pixel);
                    }

                    if(y>0)
                    {
                        int col[] = {R[y-1][x], G[y-1][x], B[y-1][x]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x,y-1,pixel);
                    }

                    if(x<ancho-1)
                    {
                        int col[] = {R[y][x+1], G[y][x+1], B[y][x+1]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x+1,y,pixel);
                    }

                    if(y<alto-1)
                    {
                        int col[] = {R[y+1][x], G[y+1][x], B[y+1][x]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x,y+1,pixel);
                    }

                    if(y>0 && x>0)
                    {
                        int col[] = {R[y-1][x-1], G[y-1][x-1], B[y-1][x-1]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x-1,y-1,pixel);
                    }

                    if(y<alto-1 && x>0)
                    {
                        int col[] = {R[y+1][x-1], G[y+1][x-1], B[y+1][x-1]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x-1,y+1,pixel);
                    }

                    if(y>0 && x<ancho-1)
                    {
                        int col[] = {R[y-1][x+1], G[y-1][x+1], B[y-1][x+1]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x+1,y-1,pixel);
                    }

                    if(y<alto-1 && x<ancho-1)
                    {
                        int col[] = {R[y+1][x+1], G[y+1][x+1], B[y+1][x+1]};
                        if(pixelR > col[0] && pixelG > col[1] && pixelB > col[2])
                            imagen.setRGB(x+1,y+1,pixel);
                    }
                }
        }

        @Override
        public void run()
        {
            int alto    = y2 - y1;
            int ancho   = x2 - x1;
            int offsetY = alto/2;  
            int offsetX = ancho/2; 
            String method = "";

            try
            {
                if(alto > 480 && ancho > 640)
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
                            erode();
                            method = "Layer.erode";
                            break;
                        case QERODE:
                            break;
                        case DILATE:
                            dilate();
                            method = "Layer.dilate";
                            break;
                        case QDILATE:
                            dilate_quick();
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


    public void reload()
    {
        instancia = 1;
        if(debug) System.out.println("Imagen.reload - Instancia:"+instancia+" IN");

        Layer img   = new Layer(operacion.COPIAR, ' ', 0, 0, alto, ancho);
        img.start();

        while(instancia > 0) {}

        if(debug) System.out.println("Imagen.reload - Instancia:"+instancia+" OUT");
    }

    private void join()
    {
        instancia = 1;
        if(debug) System.out.println("Imagen.join - Instancia:"+instancia+" IN");

        Layer rgb = new Layer(operacion.JOIN  , ' ', 0, 0, alto, ancho);
        rgb.start();
        while(instancia > 0) {}

        if(debug) System.out.println("Imagen.join - Instancia:"+instancia+" OUT");
    }

    private void copiar()
    {
        instancia = 1;
        if(debug) System.out.println("Imagen.copiar - Instancia:"+instancia+" IN");

        Layer img   = new Layer(operacion.COPIAR, ' ', 0, 0, alto, ancho);
        img.start();
        while(instancia > 0) {}

        if(debug) System.out.println("Imagen.copiar - Instancia:"+instancia+" OUT");
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
        instancia = 1;
        if(debug) System.out.println("Imagen.erode - Instancia:"+instancia+" IN");

        Layer colorR = new Layer(operacion.ERODE, 'R', 0, 0, alto, ancho);
        Layer colorG = new Layer(operacion.ERODE, 'G', 0, 0, alto, ancho);
        Layer colorB = new Layer(operacion.ERODE, 'B', 0, 0, alto, ancho);
        colorR.start();
        colorG.start();
        colorB.start();

        while(instancia > 0) {}

        join();

        if(debug) System.out.println("Imagen.erode - Instancia:"+instancia+" OUT");
  }


  /**
   */
  public void dilate(  )
  {
        instancia = 1;
        if(debug) System.out.println("Imagen.dilate - Instancia:"+instancia+" IN");

        Layer colorR = new Layer(operacion.DILATE, 'R', 0, 0, alto, ancho);
        Layer colorG = new Layer(operacion.DILATE, 'G', 0, 0, alto, ancho);
        Layer colorB = new Layer(operacion.DILATE, 'B', 0, 0, alto, ancho);
        colorR.start();
        colorG.start();
        colorB.start();

        while(instancia > 0) {}

        join();

        if(debug) System.out.println("Imagen.dilate - Instancia:"+instancia+" OUT");
  }


/**
   */
  public void quickDilate(  )
  {
        instancia = 1;
        if(debug) System.out.println("Imagen.quickDilate - Instancia:"+instancia+" IN");

        Layer color = new Layer(operacion.QDILATE, ' ', 0, 0, alto, ancho);
        color.start();
        while(instancia > 0) {}

        copiar();

        if(debug) System.out.println("Imagen.quickDilate - Instancia:"+instancia+" OUT");
  }

  public int getPixel(int x, int y)
  {
      return this.imagen.getRGB(x, y);
  }

  public void setPixel(int x, int y, int color)
  {
      this.imagen.setRGB(x, y, color);
  }

  public void resta(Imagen img)
  {
    for(int y=0; y<this.alto; y++)
        for(int x=0; x<this.ancho; x++)
        {
            int pix1 = this.imagen.getRGB(x, y);
            int pix2 = img.getPixel(x, y);
            int r = (pix1 & 0xFF0000 - pix2 & 0xFF0000);
            int g = (pix1 & 0x00FF00 - pix2 & 0x00FF00);
            int b = (pix1 & 0x0000FF - pix2 & 0x0000FF);
            this.imagen.setRGB(x, y, Math.abs(r|g|b));
        }
  }
  
  public void setBorder(int borde) throws IOException
  {
//    if (structWd == 1 && structHg == 1)
//        this.setElementoEstructurante(borde, borde, null);
    
    this.rgb2gray();
//    Imagen img = new Imagen();
//    img.setRGB(this.getRGB());

    this.erode();
    this.dilate();

    Imagen img = new Imagen(this.getPath());
    img.setRGB(this.getRGB());

    img.setElementoEstructurante(borde, borde, null);
    img.rgb2gray();
    img.erode();
    img.dilate();

    this.resta(img);
    //this.dilate();
  }

  /**
   */
  public void rgb2gray(  )
  {
    for(int y=0; y<this.alto; y++)
        for(int x=0; x<this.ancho; x++)
        {
            int pixel = this.getPixel(x, y);
            int r = (pixel & 0xFF0000)>>16;
            int g = (pixel & 0x00FF00)>>8;
            int b = pixel & 0x0000FF;

            int avg = r;
            avg = avg<g ?g :avg;
            avg = avg<b ?b: avg;
            
            int gris = (avg<<16 | avg<<8 | avg);
            this.setPixel(x, y, gris);
        }
  }

  public void setElementoEstructurante(int alto, int ancho, Integer[][] matriz)
  {
    structWd = ancho;
    structHg = alto;
    struct   = new Integer[alto][ancho];

    for(int y=0; y<alto; y++)
        for(int x=0; x<ancho; x++)
            struct[y][x] = matriz!=null ?matriz[y][x] :1;
  }
}
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

/**
 *
 * @author miguel
 */
public class Imagestion {
    public static void main(String args[])
    {
        String file  = new String();
        String file2 = new String();

        if(args.length != 1)
        {
            System.out.println("Digite: java -jar Imagestion 'archivo.jpg'");
            System.exit(1);
        }
        else
        {
            file = args[0];
            file2 = file+".borde.jpg";

            try
            {
                Integer[][] se = {{0,1,1,0},{1,1,1,1},{1,1,1,1},{0,1,1,0}};
                
                Imagen img = new Imagen(file);
                img.setElementoEstructurante(4, 4, se);
                //img.debug = true;
                img.erode();
                img.dilate();
                //img.setElementoEstructurante(4, 4, null);
                //img.dilate();

                Imagen img2 = new Imagen(file);
                //img2.setRGB(img.getRGB());

                img2.setElementoEstructurante(5, 5, null);
                img2.erode();
                img2.dilate();

                //img.setElementoEstructurante(2, 2, null);
                //img.dilate();

                img.resta(img2);
                img.rgb2gray();
                img.guardar(file2);

                System.out.println(file2+"\nOK\n");
            }
            catch(Exception e)
            {
                System.err.println("Exception: "+e.getMessage());
            }
        }
    }
}

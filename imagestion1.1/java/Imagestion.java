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
        String arg   = new String();
        byte[] opt;

        if(args.length != 2)
        {
            System.out.println("Digite: java -jar Imagestion -[i|t] 'archivo'");
            System.exit(1);
        }
        else
        {
            arg  = args[0].replaceAll("\\W", "");
            file = args[1];
            opt  = arg.toLowerCase().getBytes();
            
            switch((char)opt[0])
            {
                case 'i':
                    testImage(file);
                    break;
                case 't':
                    testPerceptron(file);
                    break;
                default:
                    break;
            }
        }
    }

    private static void testImage(String file)
    {
        String file2 = file+".borde.jpg";

        try
        {
            Integer[][] se = {{0,1,1,0},{1,1,1,1},{1,1,1,1},{0,1,1,0}};

            Imagen img = new Imagen(file);

            img.setBorder(1);
            img.setElementoEstructurante(4, 4, se);
            img.dilate();
            img.guardar(file2);

            System.out.println(file2+"\nOK\n");
        }
        catch(Exception e)
        {
            System.err.println("Exception: "+e.getMessage());
        }
    }
    
    private static void testPerceptron(String file)
    {
        Red net;
        try
        {
            int[] layers = {3,2,1};
            String[] functions = {"logsig","tansig","purelin"};
            net = new Red(layers, 1, functions);

            System.out.println("configuracion:\n"+net.getConfiguracion().toString()+"\n");
        }
        catch(Exception e)
        {
            System.err.println("Exception: "+e.getMessage());
        }       
    }
}

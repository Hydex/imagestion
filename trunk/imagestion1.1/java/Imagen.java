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

/**
 * Class Imagen
 */
public class Imagen {

  //
  // Fields
  //

  private String path;
  private int alto;
  private int ancho;
  private int[][] R;
  private int[][] G;
  private int[][] B;
  private int[][] gray;
  private Image RGB;
  
  //
  // Constructors
  //
  public Imagen () { };
  
  //
  // Methods
  //


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

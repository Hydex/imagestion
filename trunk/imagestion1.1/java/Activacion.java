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
public class Activacion {
    //
    // Methods
    //
    private Double hardlim(double val)
    {
        return val<0.0 ?0.0 :1.0;
    }

    private Double hardlims(double val)
    {
        return val<0 ?-1.0 :1.0;
    }

    private Double poslin(double val)
    {
        return val<0.0 ?0.0 :val;
    }

    private Double purelin(double val)
    {
        return val;
    }

    private Double satlin(double val)
    {
        return  val<0.0 ?0.0 :
                val>1.0 ?1.0 :val;
    }

    private Double satlins(double val)
    {
        return  val<-1.0 ?-1.0 :
                val>1.0  ?1.0  :val;
    }

    private Double logsig(double val)
    {
        return 1/(1 + Math.exp(-val));
    }

    private Double logsig_derivada(double val)
    {
        return val*(1-val);
    }

    private Double tansig(double val)
    {
        return (Math.exp(val) - Math.exp(-val))/(Math.exp(val) + Math.exp(-val));
    }

    private Double tansig_derivada(double val)
    {
        return 1 - Math.pow(this.tansig(val),2);
    }
}

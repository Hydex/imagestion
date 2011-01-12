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
 * Class Perceptron
 */
public class Perceptron
{

    //
    // Fields
    //
    public  Double[]   entradas;
    private Double[]   pesos;
    public  Double     bias;
    private Double     wBias;
    public  Double     salida;
    public  double     sigma;
    public  double     rata;
    private Activacion fnTransf;


//    private enum FuncionesTransferencia {HARDLIM, HARDLIMS, POSLIN, PURELIN, SATLIN, SATLINS, LOGSIG, TANSIG, UNDEFINED};
//    private FuncionesTransferencia funcion = FuncionesTransferencia.UNDEFINED;

    //
    // Constructors
    //
    public Perceptron (int inputs, String funcion)
    {
        entradas = new Double[inputs];
        pesos    = new Double[inputs];
        wBias    = 0d;
        salida   = 0d;
        sigma    = 0d;
        rata     = 1d;   // valor inicial con tolerancia 100%    rango [0..1]
        fnTransf = new Activacion(funcion);

        for(int i=0; i<inputs; i++)
            entradas[i] = pesos[i] = 0.0;

    }
  
    //
    // Methods
    //
    public Double calcular()
    {
        Double suma = 0.0;

        for(int i=0; i<this.entradas.length; i++)
            suma += this.entradas[i] * this.pesos[i];

        this.salida = suma + this.bias;

        return this.fnTransf.exec(this.salida);
    }

    public double setError(double error)   // error = diferencia del parametro de entrada contra valor esperado del entrenamiento
    {
        sigma = this.fnTransf.train(salida) * error;
        return sigma;
    }

    public Double backPropagation(double Sigma)  // valor Sigma debe provenir del controlador del ciclo principal
    {
        // ver la forma de ir registrando los valoes de los pesos y salidas de cada iteracion
        for(int i = 0; i<this.pesos.length; i++)
        {
            double peso = pesos[i];
            double delta = rata * Sigma * salida;
            pesos[i] = peso * delta;
        }

        return null;  // evaluar si debe retornar valor
    }
    //
    // Accessor methods
    //
    public Double getBias() {
        return bias;
    }

    public void setBias(Double bias) {
        this.bias = bias;
    }

    public Double getSalida() {
        return salida;
    }

    public void setSalida(Double salida) {
        this.salida = salida;
    }

    public Double getwBias() {
        return wBias;
    }

    public void setwBias(Double wBias) {
        this.wBias = wBias;
    }

    public void setPeso(int idx, Double valor)
    {
        this.pesos[idx] = valor;
    }

    public Double getPeso(int idx)
    {
        return this.pesos[idx];
    }

    public double getRata() {
        return rata;
    }

    public void setRata(double rata) {
        this.rata = rata;
    }

    public double getSigma() {
        return sigma;
    }

    public void setSigma(double sigma) {
        this.sigma = sigma;
    }

    //
    // Other methods
    //

    public String getConfiguracion()
    {
        return null;
    }

    public void setConfiguracion()
    {

    }
}

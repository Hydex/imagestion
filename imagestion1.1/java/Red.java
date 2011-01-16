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
 * Class Red
 */
public class Red {

    //
    // Fields
    //
    private int entradas = 0;
    private int salidas  = 0;
    private int nCapas;
    private Perceptron[][] capas;
    private Double[][] sinapsis;

    //
    // Constructors
    //
    public Red (int[] inputs, int outputs, String[] funciones) 
    { 
        nCapas   = inputs.length;
        entradas = inputs[0];
        salidas  = outputs;
        int max  = 0;

        for(int i=0; i<nCapas; i++)
            max = inputs[i]>max ?inputs[i] :max;

        capas    = new Perceptron[nCapas][max];
        sinapsis = new Double[nCapas+1][max];
        limpiarSinapsis();

        for(int i=0; i<nCapas; i++)
            for(int j=0; j<max; j++)
                capas[i][j] = j<inputs[i] ?new Perceptron(inputs[i], funciones[i]) :null;
    }
    
    public Red(String xml)
    {
        
    }

    //
    // Methods
    //
    private void limpiarSinapsis()
    {
        for(int i=0; i<sinapsis.length; i++)
            for(int j=0; j<sinapsis[i].length; j++)
                sinapsis[i][j] = null;
    }

    public Double[] simular(Double[] inputs)
    {
        Double outputs[] = new Double[salidas];

        for(int n=0; n<inputs.length && n<sinapsis[0].length; n++)
            sinapsis[0][n] = inputs[n];

        for(int i=0; i<nCapas; i++)
        {
            for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
            {
                for(int n=0; n<sinapsis[i].length && sinapsis[i][n] != null; n++)
                    capas[i][j].entradas[n] = sinapsis[i][n];
                
                sinapsis[i+1][j] = capas[i][j].calcular();

                if(i == nCapas-1)
                    outputs[j] = capas[i][j].salida;
            }
        }

        return outputs;
    }

    /**
     * Estructura y aprendizaje Capa de entrada con n neuronas.
     * Capa de salida con m neuronas. Al menos una capa oculta de neuronas.
     * Cada neurona de una capa recibe entradas de todas las neuronas de la
     * capa anterior y envía su salida a todas las neuronas de la capa posterior.
     * No hay conexiones hacia atrás ni laterales entre neuronas de la misma capa.
     *
     **/
    public Double entrenar(Double[][] inputs, Double[][] outputs)
    {
        Double[][] salidas = new Double[outputs.length][outputs[0].length], 
                   error   = new Double[outputs.length][outputs[0].length];
        
        // paso 1: Se inicializan los pesos de todas las neuronas con valores
        //         aleatorios rango [0..1]
        for(int i=0; i<nCapas; i++)
            for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                capas[i][j].inicializarPesos();

        for(int iteracion=0; iteracion < inputs.length; iteracion++)
        {
            // paso 2: Seleccionar el siguiente par de entrenamiento del conjunto de 
            //         entrenamiento, aplicando el vector de entrada a la entrada de la red. 
            //         Estructura y aprendizaje:
            //         - Capa de entrada con n neuronas.
            //         - Capa de salida con m neuronas.
            //         - Al menos una capa oculta de neuronas.
            //         - Cada neurona de una capa recibe entradas de todas las
            //           neuronas de la capa anterior y envía su salida a todas
            //           las neuronas de la capa posterior. No hay conexiones
            //           hacia atrás ni laterales entre neuronas de la misma capa.
            Double[] entradas = inputs[iteracion];

            // paso 3: Calcular salida de la red
            salidas[iteracion] = this.simular(entradas);

            // paso 4: Calcular el error entre la salida de la red y la salida deseada
            //         (vector objetivo de par de entrenamiento)
            for(int j=0; j<salidas[iteracion].length; j++)
                error[iteracion][j] = outputs[iteracion][j] - salidas[iteracion][j];

            // paso 5: Ajustar los pesos de la red para minimizar este error
            for(int i=nCapas-1; i>=0; i--)
                for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                {
                    double sigma = capas[i][j].setSigma(error[iteracion][j]);
                    capas[i][j].backPropagation(sigma);
                }

            // paso 6: Repetir de 1 al 4 para cada vector del conjunto de entrenamiento
            //         hasta que el error del conjunto entero sea aceptablemente bajo
        }

        return null;
    }

    //
    // Accessor methods
    //

    public int getEntradas() {
        return entradas;
    }

    public void setEntradas(int entradas) {
        this.entradas = entradas;
    }

    public int getNcapas() {
        return nCapas;
    }

    public void setNcapas(int nCapas) {
        this.nCapas = nCapas;
    }

    public int getSalidas() {
        return salidas;
    }

    public void setSalidas(int salidas) {
        this.salidas = salidas;
    }
    
    //
    // Other methods
    //

}

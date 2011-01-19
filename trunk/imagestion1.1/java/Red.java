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


import java.util.ArrayList;
import java.util.Hashtable;

/**
 * Class Red
 */
public class Red {

    //
    // Fields
    //
    private int   entradas = 0;
    private int   salidas  = 0;
    private int   nCapas;
    private Perceptron[][] capas;
    private Double[][]     sinapsis;
    public  double rata    = 0.01;
    public  double minimo  = 0.001;
    public  int    ciclos  = 10;

    //
    // Constructors
    //
    public Red (int[] inputs, int outputs, String[] funciones) 
    { 
        nCapas   = inputs.length;
        entradas = inputs[0];
        salidas  = outputs;
        int max  = 0;
        byte[] ascii = (new String("A")).getBytes();

        for(int i=0; i<nCapas; i++)
            max = inputs[i]>max ?inputs[i] :max;

        capas    = new Perceptron[nCapas][max];
        sinapsis = new Double[nCapas+1][max];
        limpiarSinapsis();

        for(int i=0; i<nCapas; i++)
            for(int j=0; j<max; j++)
            {
                capas[i][j] = j<inputs[i] ?new Perceptron(inputs[i], funciones[i]) :null;
                if(capas[i][j] != null)
                    capas[i][j].setId(((char)(ascii[0]+i))+i+""+j);
            }
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

    /** entrenar
     *
     * Estructura y aprendizaje:
     * - Capa de entrada con n neuronas.
     * - Capa de salida con m neuronas.
     * - Al menos una capa oculta de neuronas.
     * - Cada neurona de una capa recibe entradas de todas las
     *   neuronas de la capa anterior y envía su salida a todas
     *   las neuronas de la capa posterior. No hay conexiones
     *   hacia atrás ni laterales entre neuronas de la misma capa.
     *
     * Mas detalle en profundidad visitar:
     * http://galaxy.agh.edu.pl/~vlsi/AI/backp_t_en/backprop.html
     **/
    public Double entrenar(Double[][] inputs, Double[][] outputs)
    {
        Double[][] salidas = new Double[outputs.length][outputs[0].length], 
                   sigma   = new Double[outputs.length][outputs[0].length];
        
        // paso 1: Se inicializan los pesos de todas las neuronas con valores
        //         aleatorios rango [0..1]
        for(int i=0; i<nCapas; i++)
            for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                capas[i][j].inicializarPesos();

        for(int datos=0; datos < inputs.length; datos++)
        {
            int intentos = ciclos;
            do
            {
                // paso 2: Seleccionar el siguiente par de entrenamiento del conjunto de
                //         entrenamiento, aplicando el vector de entrada a la entrada de la red.
                Double[] entradas = inputs[datos];

                // paso 3: Calcular salida de la red
                salidas[datos] = simular(entradas);
                double error = 0.0;
                for(int i=0; i<outputs[datos].length; i++)
                    error += outputs[datos][i] - salidas[datos][i];

                if(error < minimo) break;

                // paso 4: Calcular el error entre la salida de la red y la salida deseada
                //         (vector objetivo de par de entrenamiento)
                for(int i=nCapas-1; i>=0; i--)
                    for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                    {
                        double delta = i == nCapas-1 ?outputs[i][j] - salidas[i][j]: getError(i+1,j);
                        capas[i][j].setSigma(delta);
                    }

                // paso 5: Ajustar los pesos de la red para minimizar este error
                for(int i=0; i<nCapas; i++)
                    for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                        capas[i][j].backPropagation(capas[i][j].getError(rata)); // * sinapsis[i][j]);

                // paso 6: Repetir de 1 al 4 para cada vector del conjunto de entrenamiento
                //         hasta que el error del conjunto entero sea aceptablemente bajo
            }
            while(--intentos > 0);
        }

        return null;
    }

    //
    // Accessor methods
    //

    public double getError(int capa, int peso)
    {
        double error = 0.0;

        for(int i=0; i<capas[capa].length && capas[capa][i] != null; i++)
            error += capas[capa][i].getSigma() * capas[capa][i].getPeso(peso);

        return error;
    }

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

    public Hashtable getConfiguracion()
    {
        Hashtable conf = new Hashtable();
        byte[] ascii = (new String("A")).getBytes();

        for(int i=0; i<nCapas; i++)
        {
            String capa = ""+((char)(ascii[0]+i));
            conf.put(capa, new ArrayList());

            for(int j=0; j<capas[i].length && capas[i][j] != null; j++)
                ((ArrayList)conf.get(capa)).add(capas[i][j].getConfiguracion());
        }

        return conf;
    }

}

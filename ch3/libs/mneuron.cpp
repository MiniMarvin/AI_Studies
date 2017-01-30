#ifndef __NEURON
	#define __NEURON

#include <iostream>

using namespace std;

/**
 * @brief      Class for neuron.
 */
class Neuron {
public:
	float* weights;	///< Neuron Object weights.
	float BIAS;			///< Neuron Object BIAS.
	int abc;			///< Input size.
	       			
	/**
	 * @brief      Definition of the Neuron Structure.
	 *
	 * @param      weights  The weights of the Neuron inputs.
	 * @param[in]  size     The size of the input array, necessary for C++ dynamic control of arrays.
	 * @param[in]  BIAS     The bias of the Neuron, the threshold fire.
	 */
	Neuron(float w[], int s, float b) {
		//abc = 0;
		weights = (float*) malloc(s);
		weights[s];

		abc = s;

		for(int i = 0; i < s; i++) {
			weights[i] = w[i];
		}

		BIAS = b;
	}

	/**
	 * @brief      Destroys the object.
	 */
	~Neuron(){}

	 /**
	  * @brief      Activate the Neuron with a certain float input.
	  *
	  * @param      input  The input values on the Neuron axons.
	  *
	  * @return     If the weighted sum comes bigger than BIAS, it fires 1, except it fires 0.
	  */
	int active(float input[], int size) {
		float result = 0;

		cout << "\n\n" << abc << "\n\n";

		//cout << abc << endl;
		for(int i = 0; i < size; i++) {
			result += input[i]*this->weights[i];
			//cout << "here" << endl;
		}
		result += this->BIAS;

		if(result >= 0) return 1;
		return 0;
	}

};

#endif
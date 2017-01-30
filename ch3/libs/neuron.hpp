#ifndef __NEURON
	#define __NEURON
/**
 * @brief      Class for neuron.
 */
class Neuron {
public:
	float* weights;	///< Neuron Object weights.
	float BIAS;			///< Neuron Object BIAS.
	int size;			///< Input size.

	/**
	 * @brief      Definition of the Neuron Structure.
	 *
	 * @param      weights  The weights of the Neuron inputs.
	 * @param[in]  size     The size of the input array, necessary for C++ dynamic control of arrays.
	 * @param[in]  BIAS     The bias of the Neuron, the threshold fire.
	 */
	Neuron(float* weights, int size, float BIAS);

	/**
	 * @brief      Destroys the object.
	 */
	~Neuron();

	 /**
	  * @brief      Activate the Neuron with a certain float input.
	  *
	  * @param      input  The input values on the Neuron axons.
	  *
	  * @return     If the weighted sum comes bigger than BIAS, it fires 1, except it fires 0.
	  */
	int active(float input[]);
	
};

#endif
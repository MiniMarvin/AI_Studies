#include "neuron.hpp"
#include <iostream>
#include <cstdlib>

using namespace std;

Neuron::Neuron(float weights[], int size, float BIAS) {
	
	this->weights = new float[size];
	this->size = size;

	for(int i = 0; i < size; i++) {
		this->weights[i] = weights[i];	
	}

	this->BIAS = BIAS;
}

int Neuron::active(float input[]) {
	float result = 0;
	for(int i = 0; i < size; i++) {
		result += input[i]*this->weights[i];
	}
	result += this->BIAS;

	if(result >= 0) return 1;
	return 0;
}

Neuron::~Neuron(){
	//free(this->weights);
}
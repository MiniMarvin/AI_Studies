/**
 * @Author: Caio M. Gomes.
 * @Date: 28/01/2017.
 * @Location: Abreu e Lima - Pernambuco.
 * @Description: Exercise 5 of chapter 3 from A Systematic Introduction to Neural Networks
 * and them return an image just with the edges in the binary image.
 */

#include <bits/stdc++.h>
#include <cv.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "libs/neuron.hpp"

#include <pthread.h>

//#define USE_THREADS	//uncomment to use threads
#define NUM_THREADS     4
#define DIV_VAL			100

using namespace std;
using namespace cv;


/**
 * @brief      Class that contain all the params of the pthread funcion, because we are allowed just to pass a single void pointer as argument of the function.
 */
class thel
{
public:
	Mat* src;	///source image.
	Mat* dst;	///image that will contain the borders after the procedure.
	int lp;		///the line iterator.

	thel(){};
	~thel(){};
	
};

/**
 * @brief      The Function to process the lines in the multithreading model.
 *             
 * @param      input  The input object that contain all the data necessary to be used for make the edge detection in every row.
 *
 * @return     Returns nothing.
 */
void *processLine(void* input) {
	thel* obj = (thel*) input;
	int lineNum = obj->lp;

	int msize = 9;
 	float myarr[] = {-1,-1,-1,-1, 8,-1,-1,-1,-1};
 	Neuron n(myarr, msize, 0.5);

	for (int i = lineNum+1; i < (*(obj->dst)).rows-1; i += NUM_THREADS) {
		for (int j = 1; j < (*(obj->dst)).cols - 1; ++j) {
			float* arr = new float[9];
			for (int k = 0; k < 3; ++k) {
				for (int l = 0; l < 3; ++l) {
					arr[k*3+l] = (int) (*(obj->src)).at<uchar>(i+k-1, j+l-1)/DIV_VAL;
				}
			}
			
			(*(obj->dst)).at<uchar>(i, j) = 255*n.active(arr);
		}
	}

	delete &n;

	return NULL;
}

/**
 * @brief      Make the procedure to get the gray image, then make the eecution of the routine to make the image borders become visible.
 *
 * @param[in]  argc  The argc shows how many params the program received.
 * @param      argv  The argv contin the arguments itself, in this program there should be only one param and it is the image that will be read.
 *
 * @return     returns 0 to end the program.
 */
int main(int argc, char const *argv[]) {
 	
 	int msize = 9;
 	float myarr[] = {-1,-1,-1,-1, 8,-1,-1,-1,-1};	///The array of weights for edge detection
 	Neuron n(myarr, msize, 0.5);					///The default Neuron

 	Mat original = imread( argv[1], 0 );
 	Mat img = original.clone();
 	
 	//-----------------------------------Threads-----------------------------------//
 	#ifdef USE_THREADS

 	
		pthread_t threads[NUM_THREADS];
		int rc;
		int i;
		pthread_attr_t attr;
		void *status;

		// Initialize and set thread joinable
		pthread_attr_init(&attr);
		pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

		thel buffer[NUM_THREADS];

		for( i=0; i < NUM_THREADS; i++ ){
			cout << "main() : creating thread, " << i << endl;
			buffer[i].src = &original;
			buffer[i].dst = &img;
			buffer[i].lp = i;
			rc = pthread_create(&threads[i], &attr, processLine, (void*)&buffer[i]);

			if (rc){
				cout << "Error:unable to create thread," << rc << endl;
				exit(-1);
			}
		}

		// free attribute and wait for the other threads
		pthread_attr_destroy(&attr);

		for( i=0; i < NUM_THREADS; i++ ) {
			rc = pthread_join(threads[i], &status);

			if (rc) {
				cout << "Error:unable to join," << rc << endl;
				exit(-1);
			}

			cout << "Main: completed thread id :" << i ;
			cout << "  exiting with status :" << status << endl;
		}


	//-----------------------------------------------------------------------------//
 	#else

 	for(int i = 1; i < img.rows - 1; i++) {
 		for (int j = 1; j < img.cols - 1; ++j) {
 			float* arr = new float[9];
 			for (int k = 0; k < 3; ++k) {
 				for (int l = 0; l < 3; ++l) {
 					arr[k*3+l] = (int) original.at<uchar>(i+k-1, j+l-1)/DIV_VAL;
 				}
 			}
 			img.at<uchar>(i, j) = 255*n.active(arr);
 		}
 	}	

 	#endif

 	namedWindow("original", WINDOW_NORMAL);
 	namedWindow("edges", WINDOW_NORMAL);
    imshow( "original", original );				// Show our image inside it.
    imshow( "edges", img );				// Show our image inside it.

    char c = 0;
    do{
    	c = waitKey(1);
    }
    while(c != 'q');

 	return 0;
}

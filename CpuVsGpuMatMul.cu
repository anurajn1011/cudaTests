#include <cuda_runtime.h>
#include <nvtx3/nvToolsExt.h>
#include <iostream>
#include <random>
#include <cmath>
#include <stdio.h>


#define MACRO_N 3

using namespace std;


// #1      #2
//  1 3    2 0
//  4 6    5 4

// 15
// 12
// 30
// 24
void cpuMatMul( int matrix1ColCount, int matrix1RowCount, auto  &matrix1, int matrix2ColCount, int matrix2RowCount, auto &matrix2) {
    int returnArr[matrix1ColCount][matrix2RowCount];
    // 
    for (int i = 0; i < matrix1RowCount; i++){
        int sum = 0;
        // 
        for (int j = 0; j < matrix2RowCount; j++ ){
            returnArr[i][j] = 0;
            // goes through matrix 2 columns
            for (int k = 0; k < matrix2RowCount; k++) {
                returnArr[i][j] += matrix1[i][k]*matrix2[k][j];
                
            }
            cout << returnArr[i][j] << endl;
        }       
    }

    // return returnArr;

}

// ordinary multipliction, not GMEM
__global__ void gpuMatMul(int M, int N, int K, int *matrix1, int *matrix2, int *res)
{
	// the thread locates the indices of C for which it is responsible for
	int x = blockIdx.x * blockDim.x + threadIdx.x;
	int y = blockIdx.y * blockDim.y + threadIdx.y;
	
	if (x < M && y < N) {
		int sum = 0;
		for (int i = 0; i < K; ++i) {
			sum += matrix1[x * K + i] * matrix2[i * N + y];
			
            /*# if __CUDA_ARCH__>=200
            printf("%$d", res[x * N + y]);
            #endif*/
		}
		res[x * N + y] = sum; // explicit definition of indices, GPU isn't immediately zero'd.
	}
}
	

int main() {
    cout<< "57" <<endl;
    // int matLen = 2;
    //int matrix1[2][2] = {{1,3},{4,6}};
    //int matrix2[2][2] = {{2,0},{5,4}};
    //cpuMatMul(2,2, matrix1, 2,2, matrix2);
	
    
   // int A[2][2] = {{2,0},{5,4}};
    //int B[2][2] = {{1,3},{4,6}};
    //int C[2][2];
	//dim3 threadsPerBlock(2, 2);
	//gpuMatMul<<<1, threadsPerBlock>>>(A, B, C);
	
	int *matrix1, *matrix2, *res;
	int *deviceMatrix1, *deviceMatrix2, *deviceRes;
	size_t size = MACRO_N * MACRO_N * sizeof(int); // N is a macro
	
    cout<< "74" <<endl;
	// allocate host memory
	matrix1 = (int*)malloc(size);
	matrix2 = (int*)malloc(size);
	res = (int*)malloc(size);

    cout<< "80" <<endl;
	
	// creating host arrays, 
	for (int i = 1; i < MACRO_N*MACRO_N + 1; ++i) {
		matrix1[i-1] = i;
		matrix2[i-1] = i;
	}
	

	for (int i = 0; i <MACRO_N*MACRO_N; i++){
        cout<< matrix1[i]  << " " ;
    }

    cout<< "80" <<endl;
	// allocation of memory
	cudaMalloc(&deviceMatrix1, size);
	cudaMalloc(&deviceMatrix2, size);
	cudaMalloc(&deviceRes, size);
	
    cout<< "95" <<endl;

	// move data from host to device
	cudaMemcpy(deviceMatrix1, matrix1, size, cudaMemcpyHostToDevice);
	cudaMemcpy(deviceMatrix2, matrix2, size, cudaMemcpyHostToDevice);
	// cudaMemcpy(deviceRes, res, size, cudaMemcpyHostToDevice); only do this if res has initial vals

    cout<< "101" <<endl;

	// run kernel
	dim3 threadsPerBlock(MACRO_N, MACRO_N);
    dim3 blocksPerGrid(1, 1);
	gpuMatMul<<<blocksPerGrid, threadsPerBlock>>>(MACRO_N, MACRO_N, MACRO_N, deviceMatrix1, deviceMatrix2, deviceRes);
	
    cout<< "108" <<endl;

	// moving result to host
	cudaMemcpy(res, deviceRes, size, cudaMemcpyDeviceToHost);
	
	cudaError_t error = cudaGetLastError();
	if (error != cudaSuccess) {
		cout << "CUDA Error: " << cudaGetErrorString(error) << endl;
	}

    cout<< "113" <<endl;


    cout<< "119" <<endl;

    for (int i = 0; i <MACRO_N*MACRO_N; i++){
        cout<< res[i]  << " " ;
    }
    cout<< endl;
	
    cout<< "126" <<endl;
	// freeing memory
	free(matrix1);
	free(matrix2);
	free(res);
	
	cudaFree(deviceMatrix1);
	cudaFree(deviceMatrix2);
	cudaFree(deviceRes);
    
  
  return 0;
}








// 15 18 21 
// 42 54 66
// 69 90 111
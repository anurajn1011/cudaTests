#include <cuda_runtime.h>
#include <nvtx3/nvToolsExt.h>
#include <iostream>
#include <random>

#define N 1000

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
__global__ void gpuMatMul(int M, int N, int K, int &matrix1, int &matrix2, int &res)
{
	// the thread locates the indices of C for which it is responsible for
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	int j = blockIdx.y * blockDim.y + threadIdx.y;
	
	if (i < M && j < N) {
		for (int i = 0; i < K; ++i) {
			res[x * N + y] += matrix1[x * K + i] * matrix2[i * N + y];
		}
	}
}
	

int main() {
    // int matLen = 2;
    //int matrix1[2][2] = {{1,3},{4,6}};
    //int matrix2[2][2] = {{2,0},{5,4}};
    //cpuMatMul(2,2, matrix1, 2,2, matrix2);
	
    
   // int A[2][2] = {{2,0},{5,4}};
    //int B[2][2] = {{1,3},{4,6}};
    //int C[2][2];
	//dim3 threadsPerBlock(2, 2);
	//gpuMatMul<<<1, threadsPerBlock>>>(A, B, C);
	
	int **matrix1, **matrix2, **res;
	int **deviceMatrix1, **deviceMatrix2, **deviceRes;
	size_t size = N * N * sizeof(int); // N is a macro
	
	// allocate host memory
	matrix1 = (*int)malloc(size);
	matrix2 = (*int)malloc(size);
	res = (*int)malloc(size);
	
	// creating host arrays, 
	for (int i = 0; i < N; ++i) {
		for (int j = 0; j < N; ++j) {
			matrix1[i][j] = j;
			matrix2[i][j] = j;
			res[i][j] = 0;
		}
	}
	
	// allocation of memory
	cudaMalloc(&deviceMatrix1, size);
	cudaMalloc(&deviceMatrix2, size);
	cudaMalloc(&deviceRes, size);
	
	// move data from host to device
	cudaMemcpy(deviceMatrix1, matrix1, size, cudaMemcpyHostToDevice);
	cudaMemcpy(deviceMatrix2, matrix2, size, cudaMemcpyHostToDevice);
	
	// run kernel
	dim3 gridDim(CEIL_DIV(N, 32), CEIL_DIV(N, 32), 1);
	dim3 blockDim(32, 32, 1);
	gpuMatMul<<<gridDim, blockDim>>>(N, N, N, deviceMatrix1, deviceMatrix2, deviceRes);
	
	// moving result to host
	cudaMemcpy(res, deviceRes, cudaMemcpyDeviceToHost);
	
	// freeing memory
	free(matrix1);
	free(matrix2)
	free(res)
	
	cudaFree(deviceMatrix1);
	cudaFree(deviceMatrix2);
	cudaFree(deviceRes);
    
  
  return 0;
}


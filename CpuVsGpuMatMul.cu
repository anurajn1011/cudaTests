#include <cuda_runtime.h>
#include <nvtx3/nvToolsExt.h>
#include <iostream>

5 3 7
8 2 9

int[] cpuMatMul( int matrix1colCount, int matrix1rowCount, int[] matrix1, int matrix2colCount, int matrix2rowCount, int[] matrix2) {
    int returnArr[matrix2colCount];
    // for loop of column count of matrix 2 
    for (int i = 0; i < matrix2columnCount){
        int sum  = 0
        // for loop on column count of matrix 1
        for (int j = 0; j < matrix1colCount; j++ ){
            int product = matrix1[j]*matrix2[j*matrix2colCount];
            sum += product;
        }
        returnArr[i] = sum;
        
    }

    return returnArr


}

int main() {
  
  return 0;
}
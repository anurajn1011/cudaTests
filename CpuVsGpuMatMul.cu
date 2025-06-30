#include <cuda_runtime.h>
#include <nvtx3/nvToolsExt.h>
#include <iostream>


// #1      #2
//  1 3    2 0
//  4 6    5 4

int[][] cpuMatMul( int &matrix1colCount, int &matrix1rowCount, int[][] &matrix1, int &matrix2colCount, int &matrix2rowCount, int[][] &matrix2) {
    int returnArr[matrix1colCount][matrix2rowCount];
    // 
    for (int i = 0; i < matrix1RowCount){
        int sum = 0;
        // 
        for (int j = 0; j < matrix2rowCount; j++ ){
            returnArr[i][j] = 0;
            // goes through matrix 2 columns
            for (int k = 0; k < matrix2RowCount; k++) {
                returnArr[i][j] = matrix1[i][k]*matrix2[k][j];
            }
        }       
    }

    return returnArr;

}

int main() {
    int matLen = 2
    int[matLen][matLen] matrix1 = {{1,3},{4,6}};
    int[matLen][matLen] matrix2 = {{2,0},{5,4}};
    int[matLen][matLen] cpuMatMulOutput = cpuMatMul(2,2, matrix1, 2,2, matrix2);
    
  
  return 0;
}
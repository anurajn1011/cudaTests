#include <cuda_runtime.h>
#include <nvtx3/nvToolsExt.h>
#include <iostream>
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

int main() {
    int matLen = 2;
    int matrix1[2][2] = {{1,3},{4,6}};
    int matrix2[2][2] = {{2,0},{5,4}};
    cpuMatMul(2,2, matrix1, 2,2, matrix2);
    
  
  return 0;
}


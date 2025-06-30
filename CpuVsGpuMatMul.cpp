// #include <cuda_runtime.h>
// #include <nvtx3/nvToolsExt.h>
#include <iostream>
#include <vector>

using namespace std;


// #1      #2
//  1 3    2 0
//  4 6    5 4

vector<vector<int>> cpuMatMulVec(vector<vector<int>> &matrix1, vector<vector<int>> &matrix2) 
{
	int ROW1 = matrix1.size();
	int COL1 = matrix1[0].size();
	int ROW2 = matrix2.size();
	int COL2 = matrix2[0].size();
	
	vector<vector<int>> res(ROW1, vector<int>(COL2, 0));
	
	for (int i = 0; i < ROW1; ++i) {
		for (int j = 0; j < COL2; ++j) {
			for (int k = 0; k < COL1; ++k) {
				res[i][j] += matrix1[i][k] * matrix2[k][j];
			}
			cout << res[i][j] << endl;
		}
	}
	
	return res;
}	

//int[][] cpuMatMul( int &matrix1colCount, int &matrix1rowCount, int[][] &matrix1, int &matrix2colCount, int &matrix2rowCount, int[][] &matrix2) {
    //int returnArr[matrix1colCount][matrix2rowCount];
    // 
   // for (int i = 0; i < matrix1RowCount){
     //   int sum = 0;
        // 
      //  for (int j = 0; j < matrix2rowCount; j++ ){
            //returnArr[i][j] = 0;
            // goes through matrix 2 columns
        ////////    for (int k = 0; k < matrix2RowCount; k++) {
         //////       returnArr[i][j] = matrix1[i][k]*matrix2[k][j];
         ////   }
       // }   
		//cout << returnArr[i][j] << endl;	
   // }

    //return returnArr;

//}

int main() {
    //int matLen = 2
    //int[matLen][matLen] matrix1 = {{1,3},{4,6}};
    //int[matLen][matLen] matrix2 = {{2,0},{5,4}};
    //cpuMatMul(2,2, matrix1, 2,2, matrix2);
	
	vector<vector<int>> matrix1 = {{1,3}, {4, 6}};
	vector<vector<int>> matrix2 = {{2, 0}, {5, 4}};
	
	vector<vector<int>> answer = cpuMatMulVec(matrix1, matrix2);
    
	//for (const auto& row : answer) {
        //for (int val : row)
         //   cout << val << " ";
       // cout << "\n";
 //   }
  
	return 0;
}
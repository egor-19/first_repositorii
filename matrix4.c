#include <stdio.h>
#include <math.h>
#include <stdlib.h>

struct Matrix_2 create_matrix_from3to2( int C[3][3], int y,int x);
struct Matrix_3 create_matrix_from4to3( int C[4][4], int y,int x);

struct Matrix_2 {
    int data[2][2];
};

struct Matrix_3 {
	int data[3][3];
};


int matrix_2 (int C[2][2]){
    return C[0][0]*C[1][1] - C[1][0]*C[0][1];
}

int matrix_3 (int F[3][3]){
	int result = 0;

	for (int j = 0; j<3;j++){

		struct Matrix_2 minor = create_matrix_from3to2(F,1,j+1);
		
		result+= pow(-1,j)*F[0][j]*matrix_2(minor.data);
	}	
	return result;
}

int matrix_4 (int F[4][4]){
	int result = 0;

	for (int j = 0; j<4;j++){
	struct Matrix_3 minor = create_matrix_from4to3(F,1,j+1);
	result += pow(-1,j)*F[0][j]*matrix_3(minor.data);
	}
	return result;

}

struct Matrix_2 create_matrix_from3to2( int C[3][3], int y,int x) {
	struct Matrix_2 K;
    x-=1;
    y-=1; //  пользователи номеруют строки и стобцы с 1 
	
    int i_ = 0;
    int j_=0;

    for (int i = 0; i<3;i++){
	if (i==y)
	    continue;
	j_=0;
	for (int j = 0; j<3;j++){
		if (j==x)
		    continue;
	
		K.data[i_][j_] = C[i][j];
		j_ += 1;
	}
	i_+=1;
    }
    
    return K;
}

struct Matrix_3 create_matrix_from4to3 (int C[4][4], int y,int x){
	struct Matrix_3 K;
	x -=1;
	y -= 1;

	int i_ =0;

	for (int i = 0;i<4;i++){
		if (i == y)
			continue;
		int j_=0;
		for (int j = 0; j<4;j++){
			if (j==x)
				continue;
			
			K.data[i_][j_] = C[i][j];
			j_+=1;
		}
		i_+=1;
	}

	return K;
}

void read_and_print_matrix (int SIZE,int matrix[SIZE][SIZE]){
	// проверка корректности ввода размера матрицы
	if (SIZE <2 || SIZE >4){
		printf("ошибка! введен неверный размер\n");
        exit(1);
	}

	printf("Введите элементы матрицы %d на %d:\n",  SIZE, SIZE);
	for (int i = 0; i < SIZE; i++) {
		for (int j = 0; j < SIZE; j++) {
			printf("Элемент A[%d][%d]: ", i+1, j+1);
			scanf("%d", &matrix[i][j]);
		}
	}

	printf("\n");
	printf("Более читаемый вид матрицы: \n");

	for (int i = 0; i < SIZE; i++) {
		for (int j = 0; j < SIZE; j++) {
			printf("%d\t",matrix[i][j]);
		}
		printf("\n");
	}
}

int count_res_of_matrix (int SIZE,int matrix[SIZE][SIZE]){
	int opredelitel; // будущий подсчитанный определитель
	
	if (SIZE == 2)
	opredelitel = matrix_2(matrix);
	else if (SIZE == 3)
		opredelitel = matrix_3(matrix);
	else
		opredelitel = matrix_2(matrix);

	printf("\n");
	printf("Определитель = %d\n", opredelitel);

}

int main() {

int SIZE; //РАЗМЕР МАТРИЦЫ
printf("Введите размер матрицы: 2, 3 или 4 \n"); //считывем данные
scanf("%d", &SIZE);

int matrix[SIZE][SIZE];  // объявляем матрицу

read_and_print_matrix(SIZE,matrix);
count_res_of_matrix(SIZE,matrix);

return 0;
}

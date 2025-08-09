#include <stdio.h>



void print_field(int* pole, int rows,int columns){
    for (int i = 0; i<rows;i++){
        for (int j = 0; j<columns;j++)
            printf("%d ", pole[i*columns+j]);
        printf("\n");
    }
}

int check_cell(int x,int y,int* pole,int rows, int columns){
    if  (y>=rows || y<0 || x<0 || x>=columns)
        return 0;
    return pole[y*columns+x];
} 

int count_cells(int x, int y, int* pole, int rows, int columns) {
    return (
        check_cell(x-1, y-1, pole, rows, columns) +
        check_cell(x,   y-1, pole, rows, columns)+
        check_cell(x+1, y-1, pole, rows, columns) +
        check_cell(x-1, y,   pole, rows, columns)+
        check_cell(x+1, y,   pole, rows, columns)+
        check_cell(x-1, y+1, pole, rows, columns)+
        check_cell(x,   y+1, pole, rows, columns)+
        check_cell(x+1, y+1, pole, rows, columns)
    );
}

int rules (int x, int y, int* pole, int rows, int columns){
    int k = count_cells(x,y,pole,rows, columns);
    if (pole[y*columns+x]== 0){ 
        if (k == 3)
            return 1;
        else
            return 0;
    }
    else{
        if (k == 3 || k == 2)
            return  1;
        else
            return 0;
    }
}




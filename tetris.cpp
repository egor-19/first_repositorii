#include <iostream>
#include <ncurses.h>
#include <stdlib.h>
#include <chrono>
#include <thread>
#include <time.h>
#include<sys/time.h>
using namespace std;



char figures[2][3][3 ] ={ { {'0','0','0'},
                            {'0','0','0'},
                            {'1','1','1'} },
	                  { {'1','0','0'}, {'1','0','0'}, {'1','0','0'} } };
#define WIDTH_FIGURE 3
#define HEIGHT_FIGURE 3
#define QUANTITY 2
void pr_f (char A [WIDTH_FIGURE][HEIGHT_FIGURE]){
    for ( int y = 0; y<WIDTH_FIGURE;y++){
    for ( int x = 0; x<HEIGHT_FIGURE;x++)
        cout<<A[y][x];
    cout<<endl;
    }
}

#define WIDTH_GLASS 10
#define HEIGHT_GLASS 10
int yh =0 ;
int xh =(WIDTH_GLASS - HEIGHT_GLASS)/2;

void print_glass (char A[WIDTH_GLASS][HEIGHT_GLASS]){
    for ( int y = 0; y<WIDTH_GLASS;y++){
    for ( int x = 0; x<HEIGHT_GLASS;x++)
        mvaddch(y,x,A[y][x]);
    }
}

void copy_gl( char glass_from[WIDTH_GLASS][HEIGHT_GLASS] ,char glass_to[WIDTH_GLASS][HEIGHT_GLASS] ){
    for ( int y = 0; y<WIDTH_GLASS;y++){
	for( int x = 0; x<HEIGHT_GLASS;x++){
	    glass_to[y][x] = glass_from[y][x];
	}
    }
}
void vstavka (char glass[WIDTH_GLASS][HEIGHT_GLASS], char figure [WIDTH_FIGURE][HEIGHT_FIGURE], int xx, int yy) {
    for (int y = 0; y < WIDTH_FIGURE; y++) {
        for (int x = 0; x < HEIGHT_FIGURE; x++) {
            if (y + yy<= WIDTH_GLASS && x + xx <= HEIGHT_GLASS && figure[y][x]!='0')
                glass[y + yy][x + xx] = figure[y][x];
        }
    }
}

bool is_bottom_collision( char figure[WIDTH_FIGURE][HEIGHT_FIGURE], char glass[WIDTH_GLASS][HEIGHT_GLASS], int yy,int xx){
    for (int y = 0; y <HEIGHT_FIGURE; y++){
        for (int x = 0; x< WIDTH_FIGURE; x++){
            if (figure[y][x] == '1'  && (y+yy >= HEIGHT_GLASS) || figure[y][x] == '1' && glass[y+yy][xx+x] =='1')
            return false;
        }
    }
    return true;
}

bool is_right_collision (char figure[WIDTH_FIGURE][HEIGHT_FIGURE], int xx){
    for (int y = 0;y<HEIGHT_FIGURE;y++){
        for (int x = 0;x< WIDTH_FIGURE;x++){
            if ( (figure[y][x] =='1' ) && (x+xx>= WIDTH_GLASS) )
                return false;
        }
    }
    return true;
}

bool is_left_collision (char figure[WIDTH_FIGURE][HEIGHT_FIGURE], int xx){
    for (int y = 0;y<HEIGHT_FIGURE;y++){
        for (int x = 0;x< WIDTH_FIGURE;x++){
            if ( (figure[y][x] =='1' ) && (x+xx<0 ))
                return false;
        }
    }
    return true;
}

void transponir ( char A [WIDTH_FIGURE][HEIGHT_FIGURE]){
    char B [WIDTH_FIGURE][HEIGHT_FIGURE];   
    for ( int y = 0; y<WIDTH_FIGURE;y++){
        for (int x =0 ; x<HEIGHT_FIGURE;x++)
        B[y][x] = A[x][y];
    }
    for ( int y = 0; y <WIDTH_FIGURE; y++){
        for (int x =0 ; x<HEIGHT_FIGURE; x++)
        A[y][x] = B[y][x];
    }
}


void delete_fulllines(char glass[WIDTH_GLASS][HEIGHT_GLASS]) {
    int count = 0;
    for (int y = 0; y < HEIGHT_GLASS; y++) {
        for (int x = 0; x < WIDTH_GLASS; x++) {
            if (glass[y][x] == '1') {
                count += 1;
            }
        }
        if (count == WIDTH_GLASS) {
            for (int yy = y; yy>0; yy--){
                for (int x = 0; x < WIDTH_GLASS; x++) {
                    glass[yy][x] = glass[yy-1][x]; 
                }
            } 
        }
        count = 0;
    }
}

void figure_in_glass ( char GLASS[WIDTH_GLASS][HEIGHT_GLASS], char figure[WIDTH_FIGURE][HEIGHT_FIGURE], int x, int y){
    char glass[WIDTH_GLASS][HEIGHT_GLASS];
    copy_gl(GLASS,glass);
    vstavka(glass,figure,x,y);
    print_glass(glass);
}     


long long timeInMilliseconds(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (((long long)tv.tv_sec) * 1000) + (tv.tv_usec / 1000);
}

void wait( long long milliseconds,char GLASS[WIDTH_GLASS][HEIGHT_GLASS], char figure[WIDTH_FIGURE][HEIGHT_FIGURE]) {
    long long start_time = timeInMilliseconds();
    long long end_time = start_time + milliseconds;
    while (timeInMilliseconds() < end_time) {
	char symbol = getch();
	if (symbol == 'a'){
            if ( is_left_collision(figure,xh-1) == true ){
                xh--;
	    figure_in_glass(GLASS,figure,xh,yh);
            }
	}
        else if (symbol == 'd' ){
            if ( is_right_collision(figure,xh+1)== true){ 
                xh++;
		figure_in_glass(GLASS,figure,xh,yh);
	    }
        }
        else if (symbol =='s')
	    break;
        else if(symbol == 'w'){
            transponir(figure);
	    figure_in_glass(GLASS,figure,xh,yh);
	}
    }
}



void choose_figure(char figures[QUANTITY][WIDTH_FIGURE][HEIGHT_FIGURE], char figure[WIDTH_FIGURE][HEIGHT_FIGURE]) {
    int k = rand() % QUANTITY;
    for (int y = 0; y < WIDTH_FIGURE; y++) {
        for (int x = 0; x < HEIGHT_FIGURE; x++) {
            figure[y][x] = figures[k][y][x];
        }
    }
}


void interface( char GLASS[WIDTH_GLASS][HEIGHT_GLASS], char figure[WIDTH_FIGURE][HEIGHT_FIGURE]){
    choose_figure(figures,figure);
    initscr();
    nodelay(stdscr,true);
    while ( true ){
        delete_fulllines(GLASS);
        figure_in_glass(GLASS,figure,xh,yh);
	wait(900,GLASS,figure);
            if (is_bottom_collision(figure,GLASS,yh+1,xh)== false){
    		vstavka(GLASS,figure,xh,yh);
		choose_figure(figures,figure);
                yh = 0;
		if (is_bottom_collision(figure,GLASS,yh,xh)== false)
		    break;    
	    }
            else
                yh+=1;
            }
    endwin();
}




void pr_g (char A[WIDTH_GLASS][HEIGHT_GLASS]){
    for ( int y = 0; y<WIDTH_GLASS;y++){
    for ( int x = 0; x<HEIGHT_GLASS;x++)
        cout<<A[y][x];
    cout<<endl;
    }
}

bool check_vstavka (char glass[WIDTH_GLASS][HEIGHT_GLASS], char figure [WIDTH_FIGURE][HEIGHT_FIGURE], int xx, int yy){
    for (int y = yy; y < yy+WIDTH_FIGURE; y++) {
        for (int x = xx ;x < xx+HEIGHT_FIGURE; x++) {
            if (  (y> WIDTH_GLASS || x>HEIGHT_GLASS) || (glass [y][x]!= '*') && (figure[y-yy][x-xx]!='0') )
                return false;
        }
    }
    return true;
}


void wait0 (time_t  seconds ){
    time_t  exit_time = time(NULL) + seconds;
    while ( time( NULL ) <= exit_time){
    }
}






int main ( ) {
    int X, Y;
    char figure [3][3] ={ {'0','1','0'}, {'0','1','0'}, {'0','1','0'} };
    char figure2 [3][3] = { {'0','0','0'}, {'0','0','0'}, {'0','0','0'} };
    char figures[2][3][3 ] ={ { {'0','1','0'}, {'0','1','0'}, {'0','1','0'}  },
			      { {'1','0','0'}, {'1','0','0'}, {'1','0','0'} } };
    char glass [WIDTH_GLASS][HEIGHT_GLASS];
    for ( int y = 0;y<WIDTH_GLASS;y++){
	for ( int x = 0; x<HEIGHT_GLASS;x++){
         glass[y][x] = '*';
        }   
    }




    interface( glass,figure );
    return 0;

}

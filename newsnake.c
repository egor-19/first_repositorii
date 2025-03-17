#include <ncurses.h>
#include <stdlib.h>
int *xcord;
int *ycord;
int SIZE;
int k=0;
int tail = 0;
void print (){
	if (tail< k){
		for (int i = tail; i<k;i++){
		mvaddstr(ycord[i],xcord[i],"*");
		} 
	}
	else{
	    for (int i= tail;i<SIZE;i++)
		mvaddstr(ycord[i],xcord[i],"*");
	    for (int  i = 0; i<k; i++)
		mvaddstr(ycord[i],xcord[i],"*"); 
	}   
} 
int endgame (int x, int y ){
	for (int i = 0; i<k;i++){
	    if ( x==xcord[i] && y==ycord[i]){
		return 1;
	    }
	}
	return 0;
	}    
	


    
void delete () {
    tail++;
    if (tail >= SIZE)
	tail = 0;
	}

void addel (int x,int y){
	xcord[k]=x;
	ycord[k]=y;
	k++;
	if (k>=SIZE)
	    k = 0;  
}
int main( ) {
    int x = 10,y=10;
    int xa=2,ya=2;    
    int X, Y;
    char h;
    initscr();
    halfdelay(90);  
    getmaxyx(stdscr,Y,X);
    SIZE = 10;
    xcord = malloc(SIZE*sizeof(int));
    ycord= malloc (SIZE*sizeof(int));
    addel(x,y);
    while (1) {
	erase();
//	mvaddstr(y,x,"*");
	print();
	mvaddstr(ya,xa,"@");
	h=getch();
	if (h== 'd'){
	    x+=1;  
	}
	else if ( h== 'w'){
	    y-=1;
	}
	else if ( h == 's'){
	    y+=1;
	}
	else if ( h == 'a'){
	    x-=1;
	}
	if (x==X)
	    x = 0;
	else if (x<0)
	    x =X-1;
	if (y<0)
	    y = Y-1;
	else if (y==Y)
	    y = 0;
//	if (endgame(x,y) == 1)
//	    break;
        addel(x,y);

	if (y==ya && x==xa){
	    xa = rand()%X;
	    ya = rand()%Y;
	}
	else
	    delete();
	

    // 3 4 6 7 1
     //  3 3 3 3

    }
    endwin();
    

    return 0;
    }
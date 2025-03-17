#include <iostream>
#include <cstring>
#include <stdexcept>
#include <vector>

using namespace std;

char* appendr_char(char* A, char B) {
    char* C = new char[strlen(A) + 2];
    strcpy(C, A);
    C[strlen(A)] = B;
    C[strlen(A) + 1] = '\0';
    return C;
}

class Matrix {
    public:
    char* A ;
    int y,x;
    Matrix (int x, int y){
    A = (char *)malloc(sizeof(char) * x*y);
    for (int i = 0; i<x*y;i++){
	    A[i] = '_';
    }
    this->x = x;
    this->y = y;
    }

    Matrix (int x, int y, char  array[] ){
	A = (char *)malloc(sizeof(char) *x *y);
	for ( int i = 0;i<x*y;i++){
		A[i] = array[i];
	}
	this->x=x;
	this->y = y;
    }

    operator char *(void){
	char *B = (char *)"";
    for ( int i = 0; i<x;i++){
	    for ( int j = 0; j<y;j++)
	    B = appendr_char(B,obr(i,j));
        B = appendr_char(B,'\n');
    }
    return B;
    }

    char & obr (int i, int j){
        if (i>=x || j>=y)
            //throw out_of_range("Exit beyond borders of Matrix");
            cout<<"Try again please"<<endl;
        return A[y*i+j];
    }
};


void print(Matrix A) {
    for (int i = 0; i < A.x; i++) {
        for (int j = 0; j < A.y; j++) {
            cout << A.obr(i, j);
        }
        cout << '\n';
    }
}

struct sNode {
    sNode* next;
    Matrix A;
};

sNode* add_el(Matrix A, sNode* V) {
    sNode * neww = (sNode *)malloc (sizeof(sNode));
    neww->next = V;
    neww->A = A;
    neww->A.A = (char *)malloc(sizeof(char) * A.x * A.y);
    for (int i = 0; i < A.x * A.y; i++) {
        neww->A.A[i] = A.A[i];
    }
    return neww;
}


void emptycellnum(Matrix A) {
    int k = -1;
    for (int i = 0; i < 3; i++) {
        k += 2;
        for (int j = 0; j < 3; j++) {
            if (A.obr(i,j) == '_')
                cout << (i + j + k) << ' ';
        }
    }
}

bool full(Matrix A) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (A.obr(i,j) == '_')
                return false;
        }
    }
    return true;
}

char win(Matrix A) {
    for (int i = 0; i < 3; i++) {
        if (A.obr(i,0) == A.obr(i,1) && A.obr(i,1) == A.obr(i,2) && A.obr(i,0) != '_')
            return A.obr(i,0);
    }
    for (int j = 0; j < 3; j++) {
        if (A.obr(0,j) == A.obr(1,j) && A.obr(1,j)== A.obr(2,j) && A.obr(1,j) != '_')
            return A.obr(1,j);
    }
    if ((A.obr(0,0) == A.obr(1,1) && A.obr(1,1) == A.obr(2,2)) || (A.obr(0,2) == A.obr(1,1) && A.obr(1,1) == A.obr(2,0))) {
        return A.obr(1,1);
    }
    if (full(A))
        return '*';
    else
        return '_';
}

void game(Matrix A) {
    int i = 0, choice;
    while (!full(A)) {
        i += 1;
        print(A);
        if (win(A) != '_')
            break;
        else {
            emptycellnum(A);
            cout << '\n';
            cin >> choice;
            if (A.obr( (choice - 1) / 3, (choice - 1) % 3 ) != '_') { 
                cout << "Choose again" << '\n';
                cin >> choice;
            }
            if (i % 2 == 0)
                A.obr( (choice - 1) / 3, (choice - 1) % 3 ) = 'O';  
            else
               A.obr( (choice - 1) / 3, (choice - 1) % 3 ) = 'X';
        }
    }
    cout << "The winner is " << win(A);
}



sNode* variants(Matrix A, char symvol) {
    sNode* K = NULL;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (A.obr(i,j) == '_') {
                A.obr(i,j) = symvol;
                K = add_el(A, K);
                A.obr(i,j) = '_';
            }
        }
    }
    return K;
}

void print_spisok( sNode * Q){
    while (Q!= NULL){
        print (Q->A);
        Q = Q->next;
        cout<<endl;
    }
}



char* stroka(int x) {
    char* s = (char *)"";
    while (x != 0) {
        s = appendr_char(s, (x % 10) + 48);
        x = x / 10;
    }
    return s;
}

char cheredov (char sym){
     if (sym == 'X')
        return 'O';
    else
        return 'X';
}

int count (Matrix A, char symbol){
    if (win(A)!='*' && win(A) != 'X' && win(A)!= 'O'){
        sNode* K = variants(A,symbol) ;
        int i = 1;
        while (K != NULL){
            i+=count(K->A,cheredov(symbol));
            K = K->next;

        }
         return i;
    }
    else
        return 1;
       
}


// pc -x ;
// human - o;

int max ( vector <int> V){
    int a =V[0];
    for ( int i = 1; i<V.size(); i++){
	if ( V[i] >a)
	    a = V[i];
    }
    return a;
}

int min ( vector <int> V){
    int a = V[0];
    for ( int i = 0; i<V.size();i++){
	if ( V[i] <a)
	    a = V[i];
    }
    return a;
}

void hor_print ( sNode * C){
    for ( int k = 0; k<3;k++){
	sNode * B = C;
	while (B!= NULL){
	    for ( int i = 0;i<3;i++)
		cout<<B->A.obr(k,i);
	    cout<<"  ";
	    B = B->next;
	}
	cout<<endl;
    }	
}

int minimax (Matrix A, char symbol){
    if ( win(A) == 'X')
	return 1;
    if ( win(A) == 'O')	
	return -1;
    if ( win(A) == '*') 
	return 0;
    else{
	char symbol_old = symbol;
	vector <int> Znach;
	sNode *K = variants(A,symbol);
	//hor_print(K);
	symbol = cheredov(symbol);
	while ( K != NULL){
	    Znach.push_back(minimax(K->A, symbol));
	    K = K->next;
	}
	if ( symbol_old == 'O')
	    return min(Znach);
	else
	    return max(Znach);
    } 
}

Matrix  best_board ( Matrix A){
    Matrix W(3,3);
    int a = -10;
    sNode * Q = variants (A, 'X'); 
    while ( Q != NULL){
	int b = minimax (Q->A,'O');
	if (a <b  ){
	    W = Q->A;
	    a = b;
	}
	Q = Q->next;
    }     
    return W;	
} 

void gameWithComputer() {
    Matrix A(3, 3);

    int choice;
    int i=0;

    while (win(A) == '_' && !full(A)) {
        if(i == 0) {
            print(A);
            emptycellnum(A);
            cout <<'\n'<< "Your turn: ";
            cin >> choice;
            if (A.obr((choice - 1) / 3, (choice - 1) % 3) == '_') {
                A.obr((choice - 1) / 3, (choice - 1) % 3) = 'O';
                i++;
            } 
            else {
                cout << "Try Again please" << endl;
            }
        } 
        else {
            cout << "Computer's turn..." << endl;
            A = best_board(A);
            i--;
        }
    }
    print(A);
    cout<<"THE WINNER IS "<<win(A);
    
}

int main(){
    Matrix doska(3,3);
    char  array[9]  = {'X','O','X',
		     'O','_','O',
		     '_','_','_'};

    gameWithComputer();
}

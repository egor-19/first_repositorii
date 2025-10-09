#include <iostream>
using namespace std;
#include <vector>
#include <cstdlib>
#include <ctime>


// Клетка игрового поля "Сапёр"
class Cell {
    private:
        bool is_mine; // 
        bool is_open;
        bool is_flag;
        
    
    public:

    Cell(){
        is_mine = false;
        is_open = false;
        is_flag = false;
        mines_near = 0;
    }

    int mines_near;

    void open (){
        is_open = true;
    }
    void make_flag(){
        is_flag = not(is_flag);
    }
    void set_mine(bool minaaa){
        is_mine = minaaa;
    }
    bool get_is_flag(){
        return is_flag;
    }
    bool get_is_open(){
        return is_open;
    }
    char get_symbol(){
        if (is_open){

            if (is_mine){
                //cout << "конец игры! бомба";
                    return '*';
            }

            if (mines_near == 0)
                return ' ';
            else if (mines_near>0)
                return  '0'+ mines_near;
        }
        else 
            if (is_flag == true)
                return 'F';
            else
                return '.';
        
        return ' ';
    }

    bool have_mine (){
        return is_mine;
    }
};



class Game {

    private:
        int size; // размер поля
        vector<vector<Cell>> pole;
        int flags_on_pole;
        

    public:

    int opened_cells;
    int mines_all; // всего мин
    bool game_is_going; // идёт ли игра 

    
        Game(){
            size = 5;
            mines_all = 8;
            game_is_going = true;
            pole.resize(size,  vector<Cell>(size));
            srand(time(NULL));
            opened_cells = 0;
            flags_on_pole = 0;
        }

        void put_flag(int y, int x){
            if ( y<0 || x<0 || x>=size || y>=size)
                    return ;
            else{
                if (pole[y][x].get_is_open() == false){
                    if (  flags_on_pole<mines_all){
                        pole[y][x].make_flag();
                        if (pole[y][x].get_is_flag())
                            flags_on_pole+=1;
                        else
                            flags_on_pole-=1;
    
                    }
                }
            }
            
        }

        void open_all(){
            for (int i = 0; i<size;i++){
                for (int j=0;j<size;j++)
                    pole[i][j].open();
            }
        }

        void print_pole(){
            cout<<"___________________________________\n"; //для визуализации игры
            for (int i = 0; i< size; i++){
                for (int j = 0; j <size;j++)
                    cout << pole[i][j].get_symbol()<<'\t';
                cout<<'\n';
            }
        }

        bool player_win() {
            bool res = false;

            // Вариант 1: Все не-минные клетки открыты
            if ( size * size - mines_all == opened_cells){
                res = true;
            }
                
            
            // Вариант 2: Все мины помечены флагами
            int rr = 0;
            for (int i = 0; i < size; i++){
                for (int j = 0; j < size;j++){
                    if (pole[i][j].get_is_flag() && pole[i][j].have_mine())
                        rr+=1;
                }
            }
            if (rr == mines_all)
                res = true;

            return res;
        }

        void calculate_mines(){
            int result;
            for (int i =0; i<size;i++){
                for ( int j = 0; j<size; j++){
                    result=0;
                    if ((pole[i][j]).have_mine() == true)
                        continue;
                    else{

                        if (   (i-1>=0 && (j+1)<size) &&  (pole[i-1][j+1]).have_mine() == true )
                            result+=1;
                        if (   (i-1>=0) && (pole[i-1][j]).have_mine() == true )
                            result+=1;
                        if ( (i-1>=0) && ((j-1)>=0 ) && (pole[i-1][j-1]).have_mine() == true )
                            result+=1;
                        }

                        if (   (j+1)<size && (pole[i][j+1]).have_mine() == true  )
                            result+=1;
                        if ( (j-1)>=0 && (pole[i][j-1]).have_mine() == true)
                            result+=1;

                        if ( (j+1)<size && (i+1)<size && (pole[i+1][j+1]).have_mine() == true )
                            result+=1;
                        if (  (i+1)<size && (pole[i+1][j]).have_mine() == true)
                            result+=1;
                        if ( (i+1)<size && (j-1)>=0 &&(pole[i+1][j-1]).have_mine() == true )
                            result+=1;

                        pole[i][j].mines_near = result;
                    }
                }
                
            }
        
        void put_mines(int y, int x){
            vector <int> numbers;
            for (int i = 0; i<size*size;i++)
                numbers.push_back(i);

                vector <int> bad_numbers;
                int dd = y*size+x; 
                for (int i = 0; i<size*size;i++){
                    if (i == dd+1 || i == dd-1 || i == dd+size || i == dd+size+1 || i == dd+size-1
                        || i == dd-size || i == dd-size+1 || i == dd-size-1 || i == dd)
                        bad_numbers.push_back(i);
                }
                
                vector <int> good_numbers;
                for (int i = 0; i<numbers.size(); i++){
                    int flag = 0;
                    for (int j = 0; j<bad_numbers.size();j++){
                        if (numbers[i] == bad_numbers[j]){
                            flag = 1;
                            break;
                        }
                    }
                    if (flag == 0)
                        good_numbers.push_back(numbers[i]) ;
                }
    
                for ( int i = 0; i< good_numbers.size();i++){
                    int index = rand() % good_numbers.size();
                    swap(good_numbers[i],good_numbers[index]);
                }
            

            for (int i = 0;i<mines_all;i++){
                int index = good_numbers[i];
                pole[index / size][index % size].set_mine(true);
                //cout << "Мина в: (" << index / size << "," << index % size << ")" << endl;
            }

            }


            void open_cells(int y, int x){
                if (y>=size || x>=size || x<0 || y<0)
                    cout<<" клетка неверна введена. размеры не соблюдены.\n";
                else if ( pole[y][x].get_is_open() == false ){

                    pole[y][x].open();

                   if (pole[y][x].have_mine() == true){
                        game_is_going = false;
                        //1cout<<"конец игрыыыыыыыыы. тут мина!!!\n";
                        open_all();
                        
                   }

                    opened_cells+=1;

                    if (pole[y][x].mines_near == 0){
                        
                        if (  (y-1>=0) && (x+1<size)  )
                            open_cells(y-1, x+1); 
                        if (   (y-1>=0)  )
                            open_cells(y-1, x); 
                        if ( (y-1>=0) && ((x-1)>=0 )  )
                            open_cells(y-1, x-1); 
                        if (   (y+1)<size )
                            open_cells(y+1, x); 
                        if ( (x-1)>=0 )
                            open_cells(y, x-1); 
                        if ( (x+1)<size && (y+1)<size  )
                            open_cells(y+1, x+1); 
                        if (  (y+1)<size )
                            open_cells(y+1, x); 
                        if ( (y+1)<size && (x-1)>=0  )
                            open_cells(y+1, x-1); 

                    } 
                }
            }

};

int main(){

    Game sapeeeeer;
    int y,x;

    //Обработка 1-ого хода

    sapeeeeer.print_pole();
    cout<<"введите координаты точек  (y,x): ";
    cin>>y>>x;
    y-=1;
    x-=1;
    sapeeeeer.put_mines(y,x);
    sapeeeeer.calculate_mines();
    sapeeeeer.open_cells(y,x);

    // Игорвой цикл сапёра
    while(true){
        sapeeeeer.print_pole();

        if (sapeeeeer.player_win()){
            cout << "ПОБЕДА!!! ПОЗДРАВЛЯЮ"<<'\n';
            break;
        }

        else if (!sapeeeeer.game_is_going){
            cout<<"Проигрыш. Ты нажал(а) на бомбу ((("<<"\n";
            break;
        }

        char symbol; //обрабатываем введённый знак
        cout<<"Введи команд у (o - открыть, f - флаг, ) : ";
        cin>> symbol;

        if (symbol == 'q')
            break;
        else if(symbol != 'o' && symbol != 'f'){
            cout<<"Введи команду заново. Введённой нет в списке\n";
            cin.ignore(100, '\n');
            continue;
        }
        else{
            int yy,xx;
            cout<<"Введи координаты (y,x): ";
            cin>>yy>>xx;
            yy-=1;
            xx-=1;

            if (symbol == 'o')
                sapeeeeer.open_cells(yy,xx);
            else if (symbol == 'f')
                sapeeeeer.put_flag(yy,xx);

    }

    }
    
    return 0;
}
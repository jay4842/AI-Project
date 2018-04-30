// base.cpp
#include <iostream>
#include <ctime>
#include <cstdlib>
using namespace std;

//Function Prototypes\\
|||||||||||||||||||||||
void generate_State();
void create_Board(int [], int);
void print_Board(int **, int);
void attack_pairs(int **, int);
void attack_pairs(int [], int);

// --main()--
int main()
{
    generate_State();
    
    return 0;
}// end main() lololololololol xD

// --generate_State()--
// generate randome states to pupulate the board
void generate_State()
{
    system("clear"); // clear screen

    int n;  // hold number of n queens
    
    cout << "Enter 'n' number of queens: ";
    cin >> n;
    
    // create an array of size n
    int space[n];
    
    srand(time(NULL));  // use time as seed
    
    // randomly populate the state
    for(int i = 0; i < n; i++)
        space[i] = (rand() % n - 1) + 1;
    
    for(int i = 0; i < n; i++)
        cout << space[i] << " ";
    
    cout << endl << endl;
    
    create_Board(space, n);
    attack_pairs(space, n);
}// end generate_State()

// --create_Board(int [], int)--
// create a board and place queens based on randomly generated
void create_Board(int space[], int n)
{
    // create 2d array for board of length n
    int **board;
    board = new int *[n];
    
    int *temp_ptr;
    temp_ptr = new int;
    
    
    for(int i = 0; i < n; i++)
        board[i] = new int[n];
    
    // initialize the board to an empty state
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
            board[i][j] = 0;
    }
    
    // randomly populate the board
    for(int i = 0; i < n; i++)
    {
        *temp_ptr = space[i];
        board[i][*temp_ptr] = 1;
    }
    
    delete temp_ptr;
    
    print_Board(board, n);
    attack_pairs(board, n);
}

void print_Board(int **board, int n)
{
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
            cout << board[j][i] << " ";
        
        cout << endl;
    }
}// end create_Board(int [], int)

// --attack_pairs(int **, int)--
// this function will find the number of attacking pairs
// on the board
void attack_pairs(int **board, int n)
{
    int *countR, *countC, *countD, *countTotal;
    countR = new int;
    countC = new int;
    countD = new int;
    countTotal = new int;
    
    //initialize all counts to empty state
    *countR = 0;
    *countC = 0;
    *countD = 0;
    *countTotal = 0;
    for(int i = 0; i < n; i++)
    {
        for(int j = 0; j < n; j++)
        {
            if(board[j][i] == 1)
                *countR += 1;
            if(board[i][j] == 1)
                *countC += 1;
        }
        if(*countR % 2 == 0)
            *countTotal += *countR/2;
        if(*countR % 2 != 0)
            *countTotal += *countR - 1;
        if(*countC % 2 == 0)
            *countTotal += *countC/2;
        if(*countC % 2 != 0)
            *countTotal += *countC - 1;
        
        // reset countR and countC
        *countR = 0;
        *countC = 0;
    }
    
    cout << "\n\nNumber of attacking pairs: " << *countTotal;
    
    delete countR;
    delete countC;
    delete countD;
    delete countTotal;
}// end attack_pairs(int **, int)

void attack_pairs(int state[], int n)
{
    int count = 0;

    for(int i = 0; i < n; i++)
    {
        for(int j = 1; j < n; j++)
        {
            if(i == (n - 1))
                break;
            else
            {
                if(state[i] == state[j])
                {
                    cout << endl << state[i] << " " << state[j] << endl;
                    count += 1;
                }
            }
        }
    }
    
    cout << endl << "count: " << count;
}

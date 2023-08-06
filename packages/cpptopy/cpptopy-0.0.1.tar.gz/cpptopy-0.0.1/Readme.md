# cpptopy

This is a project that helps you run C++ programs inside your python program. You can write your c++ code as is, inside a triple quoted
string and call the run function , it will run the c++ code and return the output.

In the backend , the module creates a cpp source code file(with the name win_cpptopy.cpp) with the code that you pass as argument and executes the source code through command promt USING G++ COMPILER(MAKE SURE IT IS DOWNLOADED AND ADDED TO PATH) and delets all the aditional files it creates after the execution of the code. MAKE SURE THERE ARE NO COMPILE ERRORS IN THE C++ CODE THAT YOU WRITE AND ALSO MAKE SURE THAT THE STRINGS INSIDE THE C++ CODE ARE PROPERLY QUOTED TO NOT MESS WITH THE PYTHON SYNTAX.

ALSO NOTE THAT YOU CANNOT INTERACT DIRECTLY WITH THE C++ CODE ONCE IT RUNS.. SO FINCTIONS LIKE cin WONT WORK. PLEASE TAKE YOUR INPUTS THROUGH
PYTHON.

Import the run_cpp object from the cpptopy module and create an instance as A. Then Call A.help() methord as it returns Further documentaion off each methord and best practices.


## INSTALLATION

1)Open Commmand promt

2) Check if pip is installed and added to path(write [pip --version] without brackets and if you get no errors then it's fine , otherwise
install pip and add it to PATH

3) In the command prompt type :

pip install cpptopy

and press ENTER.

## Usage

EXAMPLE:

from cpptopy import run_cpp

N = input("Enter number")

from cpptopy import run_cpp

A = run_cpp()

n = input("Enter a number")

a ='''
#include <iostream>

int main()
{
int x =''' + n + ''';


std::cout << "The number is" <<''' + n + ''';

}
    '''

ans  = A.run(a)

print(ans)

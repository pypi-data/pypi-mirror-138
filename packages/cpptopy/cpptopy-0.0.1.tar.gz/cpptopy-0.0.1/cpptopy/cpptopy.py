'''
 cpptopy module

 created by Ankan Halder, University Of Calcutta , Btech IT

 This module helps you run cpp code inside python. Make sure that Your Code Cpp code does not accept inputs. You can only interact With Your Cpp Code through Python

 First initialize: from  cpptopy import run_cpp

 then call : run_cpp.help() to get details on every function
 

 
'''




import subprocess

class run_cpp:



    def setup(self):
        out = subprocess.run(["g++" , "--version"], capture_output = True)
        ERR = out.stderr.decode()
        if (ERR != ''):
            return ERR + "/n /n Please Check if You have mingw and g++  installed and added to path "
        else:
 
            return ("Setup is successful. G++ is installed and added to path. You can Run This module")
    def run(self, cmd):
        with open('win_cpptopy.cpp', 'w') as f:

            f.write(cmd)
        out = subprocess.run(["g++" , "win_cpptopy.cpp" , '-o' , "win_cpptopy.exe"], stdout = subprocess.PIPE , stderr = subprocess.PIPE)
        if (out.stderr.decode() != '' ):
             return out.stderr.decode()
            
        out = subprocess.run("win_cpptopy.exe", stdout = subprocess.PIPE , stderr = subprocess.PIPE)
        rd = ['cmd', '/c', 'del', '/s', '/q',"win_cpptopy.cpp"]
        del_cmd = subprocess.run(rd)
        rd = ['cmd', '/c', 'del', '/s', '/q',"win_cpptopy.exe"]
        del_cmd = subprocess.run(rd)
        if (out.stderr.decode() != '' ):
             return out.stderr.decode()
        
        return out.stdout.decode()


    
    def help(self):
        a = '''
 cpptopy module

 created by Ankan Halder, University Of Calcutta , Btech IT

 This module helps you run cpp code inside python. Make sure that Your Code Cpp code does not accept inputs. You can only interact With Your Cpp Code through Python

 First initialize: from  cpptopy import run_cpp

 then call : run_cpp.help() to get details on every function


 MAKE SURE THAT YOU ONLY INTERACT WITH YOUR CPP CODE THROUGH PYTHON. THAT MEANS FUNCTIONS LIKE CIN WON'T WORK. ACCEPT INPUTS THROUGH PYTHON AND SEND THE INPUT IN YOUR TRIPPLE
 QUOTED Cpp COMMAND


 THIS MODULE ONLY WORKS WITH G++ COMPILER SO MAKE SURE YOU HAVE IT INSTALLED AND ADDED TO PATH(ENVIRONMENT VARIABLES)

 THE MODULE HAS 2 functions:

 1) setup() 

 eg:

 from cpptopy import run_cpp

 A = run_cpp()

 A.setup()


 THIS WILL SHOW YOU WETHER YOU HAVE g++ INSTALED AND ADDED TO PATH IN YOUR WORKSTATION THUS TELLING YOU WETHER YOU CAN RUN THE MODULE. IF IT RETURNS AN ERROR
 MAKE SURE YOU HAVE G++ COMPILER INSTALLED AND ADDED TO PATH


 2) run(<Str>)
 eg:
  from cpptopy import run_cpp

 A = run_cpp()
 cmd = <Your triple-quoted string>
 A.setup(cmd)

 

 
'''
        return a
          
        
        
        



            
    


 

            
            
            
  





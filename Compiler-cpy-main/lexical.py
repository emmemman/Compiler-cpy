import sys
import os

funcIDs = []
IDs=[]
##tokens = []
token = ''
line = 1
counter = 0

# cpy dictionary
keywords = ['main','def','#def','#int','global','if','elif','else','while','print', 'return', 'input', 'int' 'and','or','not']


####################
# Lexical Analyzer #
####################

def lexical_analyzer():
    state = 0
    global line
    lexeme = ''
    global tokens 
    
    while state != 9:
        c = f.read(1)
        if(state == 0):
            if(c.isspace()):
                if(c == '\n'):
                    line+=1
                state = 0
            elif(c.isalpha()):
                lexeme+=c
                state=1
            elif(c.isdigit()):
                lexeme+=c
                state = 2
            elif(c in "+-"):
                lexeme+=c
                ##tokens.append(('ADD_OP',lexeme))
                state = 9
            elif(c in "*%"):
                lexeme+=c
                ##tokens.append(('MULT_OP',lexeme))
                state = 9
            elif(c in '()'):
                lexeme+=c
                ##tokens.append(('GROUPING',lexeme))
                state = 9
            elif(c in ',:'):
                lexeme+=c
                ##tokens.append(('SEPERATOR',lexeme))
                state = 9
            elif(c=='/'):
                lexeme+=c
                state = 3
            elif(c=='='):
                lexeme+=c
                state = 4
            elif(c=='<'):
                lexeme+=c
                state = 5
            elif(c=='>'):
                lexeme+=c
                state = 6
            elif(c=='!'):
                lexeme+=c
                state = 7
            elif(c=='#'):
                lexeme+=c
                state = 8
            else:
                print("Error at line "+ str(line))
                exit()

        elif(state == 1):
            if(c.isalpha() or c.isdigit()):
                lexeme+=c
                
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
                    ##tokens.append(('IDENTIFIER',lexeme))
                ##elif(lexeme in keywords):
                    ##tokens.append(('KEYWORD',lexeme))
                state = 9
            else:
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
                    ##tokens.append(('IDENTIFIER',lexeme))
                ##elif(lexeme in keywords):
                    ##tokens.append(('KEYWORD',lexeme))
                f.seek(f.tell()-1)
                state = 9

        elif(state == 2):
            if(c.isdigit()):
                lexeme+=c

            elif(c.isalpha()):
                print("Error! Letter after digit in line "+str(line))
                exit()

            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                num =int(lexeme)
                if(num < - (2**32)-1 or num > (2**32)-1):
                    print("Error! Number out of range in line "+str(line))
                    exit()
                ##tokens.append(('LITERAL_INT',lexeme))
                state=9

            else:
                num = int(lexeme)

                if(num < - (2**32)-1 or num > (2**32)-1):
                    print("Error! Number out of range in line "+str(line))
                    exit()
                f.seek(f.tell()-1)
                ##tokens.append(('LITERAL_INT',lexeme))
                state = 9

        elif(state == 3):
            if(c=='/'):
                lexeme+=c
                ##tokens.append(('MULT_OP',lexeme))
                state = 9
            else:
                print("Error at line "+ str(line))
                exit()

        elif(state == 4):
            if(c=='='):
                lexeme+=c
                ##tokens.append(('LOGICAL',lexeme))
                state = 9
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                ##tokens.append(('ASSIGNMENT',lexeme))
                state=9
            else:
                f.seek(f.tell()-1)
                ##tokens.append(('ASSIGNMENT',lexeme))
                state = 9

        elif(state == 5):
            if(c=='='):
                lexeme+=c
                ##tokens.append(('LOGICAL',lexeme))
                state = 9
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                ##tokens.append(('LOGICAL',lexeme))
                state=9
            else:
                f.seek(f.tell()-1)
                ##tokens.append(('LOGICAL',lexeme))
                state = 9
        
        elif(state == 6):
            if(c=='='):
                lexeme+=c
                ##tokens.append(('LOGICAL',lexeme))
                state = 9
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                ##tokens.append(('LOGICAL',lexeme))
                state=9
            else:
                f.seek(f.tell()-1)
                ##tokens.append(('LOGICAL',lexeme))
                state = 9
        
        elif(state == 7):
            if(c=='='):
                lexeme+=c
                ##tokens.append(('LOGICAL',lexeme))
                state = 9
            else:
                print("Error at line "+ str(line))
                exit()

        elif(state == 8):
            if(c=='#'):
                lexeme = ''
                while c:
                    c = f.read(1)
                    if c == '#' and f.read(1)=='#':
                        state = 0
                        break
            elif(c=='{' or c=='}'):
                lexeme+=c
                ##tokens.append(('GROUPING',lexeme))
                state = 9
            elif(c.isalpha()):
                lexeme+=c
                state = 8
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                if(lexeme in keywords):
                    ##tokens.append(('KEYWORD',lexeme))
                    state=9
                else:
                    print("Error at line "+ str(line)+', '+lexeme+' not recognizable word')
                    exit()
            else:
                print("Error at line "+ str(line))
                exit()
            
    return lexeme


###################
# Syntax Analyzer #
###################


def program():
    notmain()    
    main()
    print("Syntax Analysis Successful! \n")

def notmain():
    global token
    token = lexical_analyzer()
    while(token == '#int'):
        globals_declare()
        print(str(token)+' wazzup')
    while(token == 'def'):
        function_def()
    print("notmain complete")

def globals_declare():
    global token
    token = lexical_analyzer()
    print('-----token+===='+str(token))
    if(token in IDs):
        ##declaration()
        print('Valid name nice!')
    else:
        print('Error not valid global var name on line'+str(line))
    token = lexical_analyzer()

def declarations():
    global token
    while(token == '#int'):
        print('declare that '+str(token))
        formal_pars()

def declaration():
    id_def()

def id_def():
    global token
    print('id that '+str(token))
    token = lexical_analyzer()
    funcIDs.append(token)

def functions():
     global token
     global counter  
     while(token == 'def'):
          print('i have become the function hahahahah '+str(token))
          counter+=1
          function_def()

def function_def():
     id_def()
     global token 
     token = lexical_analyzer()
     if(token == '('):
          formal_pars()
          if(token == ')'):
               token = lexical_analyzer()
               if(token == ':'):
                token = lexical_analyzer()
                if(token == '#{'):
                        token = lexical_analyzer()                        
                        declarations()
                        use_globals()
                        functions()
                        code_block()
                                                 
                        if(token == '#}'):
                            token = lexical_analyzer()
                        else:
                            print('Error! missing "#}" in line '+str(line))
                            exit()               
                else:
                    print('Errorr! missing "#{" in line '+str(line))
                    exit()
               else:
                print('Errorr! missing ":" in line '+str(line))
                exit()
          else:
              print('Errorr! missing ")" in line '+str(line))
              exit()
     else:
         print('Errorr! missing "(" in line '+str(line))
         exit()

def formal_pars():
    global token
    token = lexical_analyzer()
    if(token in IDs):
        id_def()
        while(token == ','):
            token = lexical_analyzer()
            if(token in IDs):
                id_def()		
            else:
                print("Syntax error in line: "+str(line))
                exit()

def use_globals():
    global token
    while(token == 'global'):
        print('globalize that '+str(token))
        formal_pars()

def code_block():
     global token
     while(token!='#}'):
        print('code block dissss '+str(token))
        if (token in IDs):
            assignment()
        elif(token == "if"):
            if_stat()
        elif(token == 'while'):
            while_stat()
        elif(token == "return"):
            return_stat()
        elif(token == 'print'):
            print_stat()
        elif(token == 'global' or token == '#int'):
            globals_declare()
        elif(token == 'elif'):
            break
        elif(token == 'else'):
            print('AAAAAA'+str(token))
            break
        else:
            print('Syntax error in line: '+str(line))
            exit()

def assignment():
     global token
     print('assignt that '+str(token))
     token = lexical_analyzer()
     if(token =='='):
          expression()
     else:
          print('Expected = at line'+str(line))
		
def if_stat():
        print('1-if starts')
        condition()
        global token
        
        if( token== ":" ):
            token = lexical_analyzer()
            code_block()
            print('BBCCCCCCCCCCCCCCCCCCCC'+str(token))
            while(token == "elif"):
                elif_choice()
            print('BBBBBBBBBBBB'+str(token))
            if(token == 'else'):
                else_choice()
        else:
            print("Error! Missing ':' in line: "+str(line))	
            exit()

def if_stat4():
     global token
     
     condition()
     token = lexical_analyzer()
     if( token== ":" ):
          token = lexical_analyzer()
          code_block()
     else:
          print("Error Missing ':' in line" + str(line)) 
          exit()
     if(token=="elif"):
          token = lexical_analyzer()
          if(token == ":"):
               token= lexical_analyzer()
               code_block()
          else:
               print("Error Missing ':' in line"+ str(line))
               exit()
     if(token== "else"):
          token = lexical_analyzer()
          if(token==":"):
               token= lexical_analyzer()
               code_block()
          else:
               print("Error Missingf ':' in line"+str(line))
               exit()

def elif_choice():
    global token
    print('mpika elif malaka me token '+str(token)) 
    condition()
    
    print('etsu jau den einai anwnfeawihjasdujifhujioghui'+str(token))
    if(token == ':'):
        token = lexical_analyzer()
        code_block()

def else_choice():
    global token
    print('------------mpika else malaka me token '+str(token)) 
    token = lexical_analyzer()
    if(token == ':'):
        token = lexical_analyzer()
        code_block()
    else:
        print("Error! Missing ':' in line: "+str(line))	
        exit()
    
def return_stat():
     global token
    
     expression()
     print('------------------------------------------------------------')


def print_stat():
     global token 
     token = lexical_analyzer()
     if(token == "("):
          token = lexical_analyzer() 
          expression()
          if(token == ")"):
               token= lexical_analyzer()
          else:
               print("Error Missing ')' in line " +str(line))
               exit()
     else:
          print("Error Missing '(' in line " +str(line))
          exit()

def while_stat():
        condition()
        global token
        token = lexical_analyzer()
        if(token == ':'):
            token = lexical_analyzer()
            if(token == '#'):
                token = lexical_analyzer()   
                if(token == '{'):
                    code_block()
                if(token == '#}'):
                    token = lexical_analyzer()

def expression():
    global token
    token = lexical_analyzer()
    if(token in funcIDs):
        print('gamw to spiti tou mannfiadnsisafidsinfadsjndfsjdfj')
    optional_sign()
    term()
    print('express diss '+str(token))
    while(token == '+' or token == '-'):
        ADD_OP()
        term()

def term():
    global token
    print('term disss '+str(token))
    factor()
    while(token == '*' or token == '//'):
        MUL_OP()
        factor()

def factor():
    global token
    ##token = lexical_analyzer()
    print('factorasdasdasdasdaDIS '+str(token))
    if(token.isdigit()):
        token = lexical_analyzer()
    elif(token in IDs): 
        print('factor DIS '+str(token))
        token = lexical_analyzer()
        idtail()
    elif(token=='('):
        
        expression()
        if(token ==')'):
            token = lexical_analyzer()
        else:	
            print("Error! Missing ')' in line "+str(line)) 
            exit()     
    else:
        print("Error! '(' or ID or number expected in line "+str(line))
        exit()

def condition():
    global token
    bool_term()
    while(token == 'or'):
        print('afto einai or '+str(token))
        
        bool_term()

def bool_term():
    global token
    print('3-bool term starts '+str(token))
    bool_factor()	
    while(token == 'and'):
        print('we have andd')
        
        bool_factor()

def bool_factor():
    global token
    print('4-bool factor starts '+str(token))
    if(token == 'not'):
        token = lexical_analyzer()
        condition()
    else:
        expression()
        REL_OP()
        expression()

def idtail():
    global token    
    if(token == '('):
        token = lexical_analyzer()
        actual_par_list()
        if(token == ')'):
            token = lexical_analyzer()
        else:
            print("Error! Missing ')' in line "+str(line))
            exit()	

def actual_par_list():
	global token
	expression()
	while(token==','):
		token = lexical_analyzer()
		expression()

def optional_sign():
	global token
	if(token=='+' or token=='-'):
		ADD_OP()

def ADD_OP():
    global token
    if(token == '+'):
        token = lexical_analyzer()
        addop = '+'
    elif(token == '-'):
        token = lexical_analyzer()
        addop = '-'
    return addop

def MUL_OP():
    global token
    if(token == '*'):
        token = lexical_analyzer()
        mulop = '*'
    elif(token == '//'):
        token = lexical_analyzer()
        mulop = '//'
    elif( token =='%'):
        token = lexical_analyzer()
        mulop = '%'
    return mulop

def REL_OP():
    global token
    print('is thie ssdfasdf '+str(token))
    if token == '==':
        #token = lexical_analyzer()
        relop = '=='
    elif token == '<=':
        #token = lexical_analyzer()
        relop = '<='
    elif token ==  '>=':
        #token = lexical_analyzer()
        relop = '>='
    elif token == '>':
        #token = lexical_analyzer()
        relop = '>'
    elif token == '<':
        #token = lexical_analyzer()
        relop = '<'
    elif token == '!=':
        #token = lexical_analyzer()  
        relop = '!='
    else:
        print("Error! Missing 'relational operator' in line "+str(line))
        exit()
    return relop

def main():
     global token
     token = lexical_analyzer
     if(token == 'main'):
          code_block()
     else:
          print('Error expected main at line' +str(line))	




f = open('test.cpy')
program()

    




#filename = sys.argv[1].replace('.ci','')
#print("Analysing file with name " + filename + ".ci \n")

#token=lexical_analyzer()

#program()

#intFile(filename)
#print("Outputed .int file in dir, with name " + filename + ".int \n")

#CFile(filename)
#print("Outputed .c file in dir, with name " + filename + ".c \n")

#outputSymbFile(filename)
#print("Outputed .symb file in dir, with name " + filename + ".symb \n")
#remScope()

#print("Outputed .asm file in dir, with name " + filename + ".asm \n")


#help(filename)



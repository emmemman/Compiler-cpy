#NIKOLAOS SKRETAS 4493
#EMMANOUIL EMMANOUILIDIS 4669

funcIDs = []
IDs=[]
token = ''
line = 1

# cpy keywords
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
                state = 9
            elif(c in "*%"):
                lexeme+=c
                state = 9
            elif(c in '()'):
                lexeme+=c
                state = 9
            elif(c == ','):
                lexeme+=c
                state = 9
            elif(c == ':'):
                lexeme+=c
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
                state = 9
            else:
                if(lexeme not in keywords):
                    if(lexeme not in IDs):
                        IDs.append(lexeme)
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
                state=9

            else:
                num = int(lexeme)

                if(num < - (2**32)-1 or num > (2**32)-1):
                    print("Error! Number out of range in line "+str(line))
                    exit()
                f.seek(f.tell()-1)
                state = 9

        elif(state == 3):
            if(c=='/'):
                lexeme+=c
                state = 9
            else:
                print("Error at line "+ str(line))
                exit()

        elif(state == 4):
            if(c=='='):
                lexeme+=c
                state = 9
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                state=9
            else:
                f.seek(f.tell()-1)
                state = 9

        elif(state == 5):
            if(c=='='):
                lexeme+=c
                state = 9
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                state=9
            else:
                f.seek(f.tell()-1)
                state = 9
        
        elif(state == 6):
            if(c=='='):
                lexeme+=c
                state = 9
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                state=9
            else:
                f.seek(f.tell()-1)
                state = 9
        
        elif(state == 7):
            if(c=='='):
                lexeme+=c
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
                state = 9
            elif(c.isalpha()):
                lexeme+=c
                state = 8
            elif(c.isspace()):
                if(c=='\n'):
                    line+=1
                if(lexeme in keywords):
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
    while(token == 'def'):
        function_def()

def globals_declare():
    global token
    token = lexical_analyzer()
    if(token not in IDs):
        print('Error not valid global var name on line'+str(line))
        exit()
    token = lexical_analyzer()

def declarations():
    global token
    while(token == '#int'):
        formal_pars()

def id_func():
    global token
    token = lexical_analyzer()
    funcIDs.append(token)

def id_def():
    global token
    token = lexical_analyzer()

def functions():
     global token
     global counter  
     while(token == 'def'):
          function_def()

def function_def():
     id_func()
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
        formal_pars()

def code_block():
     global token
     while(token!='#}'):
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
            break
        else:
            print('Syntax error in line: '+str(line))
            exit()

def code_block_main():
     global token
     while(token!=''):
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
            break
        else:
            print('Syntax error in line: '+str(line))
            exit()

def assignment():
     global token
     token = lexical_analyzer()
     if(token =='='):
          expression()
     else:
          print('Expected = at line '+str(line))
          exit()
		
def if_stat():
        condition()
        global token
        if( token== ":" ):
            token = lexical_analyzer()
            code_block()
            while(token == "elif"):
                elif_choice()
            if(token == 'else'):
                else_choice()
        else:
            print("Error! Missing ':' in line: "+str(line))	
            exit()

def elif_choice():
    global token
    condition()
    if(token == ':'):
        token = lexical_analyzer()
        code_block()
    else:
        print('Error expected ":" at line '+str(line))

def else_choice():
    global token 
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

def print_stat():
     global token 
     token = lexical_analyzer()
     if(token == "("):         
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
    if(token == ':'):
        token = lexical_analyzer()
        if(token == '#{'):
            token = lexical_analyzer()               
            code_block()
            if(token == '#}'):
                token = lexical_analyzer()
            else:
                 print("Error! '#}' expected in line "+str(line))
                 exit()
        else:
            print("Error! '#{' expected in line "+str(line))
            exit()
    else:
        print("Error! ':' expected in line "+str(line))
        exit()

def expression():
    global token
    token = lexical_analyzer()
    optional_sign()
    term()
    while(token == '+' or token == '-'):
        ADD_OP()
        term()

def term():
    global token
    factor()
    while(token == '*' or token == '//' or token == '%'):
        MUL_OP()
        factor()

def factor():
    global token
    if(token.isdigit()):
        token = lexical_analyzer()

    elif(token in funcIDs): 
        token = lexical_analyzer()

        if(token == '('):
    
            while(token!=')'):
                actual_par_list()
            token = lexical_analyzer()
        else:
            print("Error! '(' expected in line "+str(line))
            exit()

    elif(token=='('):     
        expression()
        if(token ==')'):
            token = lexical_analyzer()
        else:	
            print("Error! Missing ')' in line "+str(line)) 
            exit()   

    elif(token == 'int'):
        token = lexical_analyzer()
        if(token == '('):
            token = lexical_analyzer()
            if(token == 'input'):
                token = lexical_analyzer()
                if(token == '('):
                    token = lexical_analyzer()
                    if(token == ')'):
                        token=lexical_analyzer()
                        if(token == ')'):
                            token = lexical_analyzer()
                        else:
                            print("Error Missing ')' in line"+str(line))
                            exit()
                    else:
                        print("Error Missing ')' in line"+str(line))
                        exit()
                else:
                    print("Error Missing ')' in line "+ str(line))
                    exit()
            else:
                print("Error Missing 'input' in line" + str(line))
                exit()    
        else:
            print("Error Missing '(' in line"+str(line))
            exit()

    elif(token in IDs):
        token = lexical_analyzer()
        #idtail()

    else:
        print("Error! '(' or ID or number expected in line "+str(line))
        exit()

def condition():
    global token
    bool_term()
    while(token == 'or'):       
        bool_term()

def bool_term():
    global token
    bool_factor()	
    while(token == 'and'):  
        bool_factor()

def bool_factor():
    global token
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
    if token == '==':
        relop = '=='
    elif token == '<=':
        relop = '<='
    elif token ==  '>=':
        relop = '>='
    elif token == '>':
        relop = '>'
    elif token == '<':
        relop = '<'
    elif token == '!=':
        relop = '!='
    else:
        print("Error! Missing 'relational operator' in line "+str(line))
        exit()
    return relop

def main():
    global token
    if(token == '#def'):
            token = lexical_analyzer()
            if(token == 'main'):
                token = lexical_analyzer() 
                code_block_main()
            else:
                print('Error expected main at line ' +str(line))
                exit()          
    else:
        print('Error expected #def for main at line ' +str(line))	
        exit()


f = open('test.cpy')
program()
#NIKOLAOS SKRETAS 4493
#EMMANOUIL EMMANOUILIDIS 4669

funcIDs = []
IDs=[]
varIDs=[]
quadList = []
tempList = []
token = ''
buffer = ''
line = 1

scopes = []
scope = []

quadCounter = 1
tempCounter = 0

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

######################
# Endiamesos Kwdikas #
######################

def nextquad():
    global quadCounter
    return quadCounter

def genquad(op,x,y,z):
    global quadList, quadCounter
    count = nextquad()

    newquad = [count,op,x,y,z]
    quadList.append(newquad)

    quadCounter+=1

    return newquad

def newtemp():
    global tempCounter
    global tempList

    temp = 'T_'
    tempCounter +=1 
    temp += str(tempCounter)

    tempList += [temp]

    ent = Entity.Temp(temp, 'tmp', getOffset())
    newEntity(ent)

    return temp

def makeList(x):
    makeLst = [x]

    return makeLst

def merge(list1,list2):
    mergeLst = []
    mergeLst += list1 + list2

    return mergeLst

def backpatch(lists,z):
    global quadList

    for i in range(len(lists)):
        for j in range(len(quadList)):
            if lists[i] == quadList[j][0] and quadList[j][4] == '_':
                quadList[j][4] = z
                break

def intFile(file):
    global quadList,buffer

    buffer = ''
    F = open(file + '.int','w')
    for i in range(len(quadList)):
        buffer += str(quadList[i][0]) + ' ' + str(quadList[i][1]) + ' ' + str(quadList[i][2]) + ' ' + str(quadList[i][3]) + ' ' + str(quadList[i][4]) + '\n'

    F.write(buffer + '\n')
    F.close()

def CFile(file):
    global quadList,varIDs,buffer
    
    F = open(file + '.c','w')

    program_ = []
    program_.append('int main()\n{')

    buffer = '\n\tint '

    for variable in varIDs:
        buffer += str(variable) + ','

    program_.append(buffer[:-1] +';\n')

    program_.append('\tL_' + str(quadList[0][0]) + ':\n')

    for q in quadList[1:-1]:

        prog = '\n\tL_' + str(q[0]) + ': '

        if q[1] == ':=':
            prog += str(q[4]) + ' = ' + str(q[2]) + ';\n'
        
        elif q[1] == 'jump':
            prog += 'goto L_' + str(q[4]) + ';\n'
        
        elif q[1] == 'ret':
            prog += 'return(' + str(q[2]) + ');\n'

        elif q[1] == 'call':
            prog += '{};\n'

        elif q[1] == 'inp':
            prog += 'scanf("%d", &' + str(q[2]) + ');\n'

        elif q[1] == 'out':
            prog += 'printf("%d",' + str(q[2]) + ');\n'
        
        elif q[1] == '+' or q[1] == '-' or q[1] == '*' or q[1] == '/':
            prog += str(q[4]) + ' = ' + str(q[2]) + str(q[1]) + str(q[3]) + ';\n'
        
        elif q[1] == '<>' or q[1] == '=' or q[1] == '>' or q[1] == '<' or q[1] == '=>' or q[1] == '=<':
            relop = q[1]
            
            if relop == '<>':
                relop = '!='
            
            if relop == '=':
                relop = '=='

            prog += 'if (' + str(q[2]) + relop + str(q[3]) + ') goto L_' + str(q[4]) + ';\n'
        
        elif q[1] == 'halt':
            prog += '{};\n'
        
        program_.append(prog)
    program_.append('}')
    
    for i in program_:
        F.write(i)
    F.close()

################
# Symbol Table #
################

class Entity:

    def __init__(self, id, state):
        self.id = id
        self.state = state
        self.scope = -1

    @classmethod

    def Var(wrap, id, state, offset):

        variable = wrap(id, state)
        variable.offset = offset

        return variable

    @classmethod

    def Sub(wrap, id, state):
        
        sub = wrap(id, state)
        sub.squad = 0
        sub.args = []
        sub.length = 0

        return sub

    @classmethod

    def Par(wrap, id, state, mode, offset):

        parameter = wrap(id, state)
        parameter.mode = mode
        parameter.offset = offset

        return parameter

    @classmethod

    def Temp(wrap, id, state, offset):

        temp = wrap(id, state)
        temp.offset = offset

        return temp

def newEntity(entity):

    global scopes

    if scopes:
            scopes[-1][2].append(entity)
        
    print('New Entity: ')

def newScope(identifier):
    global scopes

    scopes.append([identifier,len(scopes),[]])
        
def remScope():

    global scopes

    if scopes: 
        del scopes[-1]
            
def newArg(argument):

    global scopes

    if scopes:
        if scopes[-1][2]:
            scopes[-1][2][-1].args.append(argument)

def newParams():

    global scopes

    if len(scopes) > 1:
        if scopes[-2][2]:
            for arg in scopes[-2][2][-1].args:
                parameter = Entity.Par(arg[0], 'prm', arg[2], getOffset())
                newEntity(parameter)
        
def getOffset():

    global scopes

    offset = 12

    if scopes:
        if scopes[-1][2]:
            for ent in scopes[-1][2]: 
                if ent.state == 'var' or ent.state == 'tmp' or ent.state == 'prm':
                    offset += 4

        return offset

def getLength():

    global scopes

    if len(scopes) > 1:
        if scopes[-2][2]:
            scopes[-2][2][-1].length = getOffset()

def getSQuad():

    global scopes

    if len(scopes) > 1:
        if scopes[-2][2]:
            scopes[-2][2][-1].squad = nextquad()

def outputSymbFile(file):

    global scopes, buffer

    buffer = ''
    F = open(file + '.symb', 'a')
    for scope in reversed(scopes):
        buffer += '\nScope ' + str(scope[1]) +'\n'
   
        for ent in scope[2]:
                
            if ent.state == 'var':
                buffer += '  Variable entity: ' + ent.id +', offset: ' + str(ent.offset) + '\n'

            elif ent.state == 'tmp':
                buffer += '  Temporary variable entity: ' + ent.id +', offset: ' + str(ent.offset) + '\n'

            elif ent.state == 'prm':
                buffer += '  Parameter entity: ' + ent.id + ', mode: ' + str(ent.mode) + ', offset: ' + str(ent.offset) + '\n'

            elif ent.state == 'func':
                buffer += '  Function entity: ' + ent.id + ', starting quad: ' + str(ent.squad) + ', length: ' + str(ent.length) + '\n'

            elif ent.state == 'proc':
                buffer += '  Procedure entity: ' + ent.id + ', starting quad: ' + str(ent.squad) + ', length: ' + str(ent.length) + '\n'

    F.write(buffer + '\n')
    F.close()

def search_id(id):

    global scopes

    if scopes:

        for scope in scopes[::-1]:

            for ent in scope[2]:
                if ent.id == id:
                    ent.scope = scope
                    return ent

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
        function()

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

#def id_func():
#    global token
#    token = lexical_analyzer()
#    funcIDs.append(token)

#def id_def():
#    global token
#    token = lexical_analyzer()

def functions():
     global token
     global counter  
     while(token == 'def'):
          function()

def function():
     global token
     token = lexical_analyzer()
     function_name = token
     

     newScope(function_name)
     newParams()

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
                        functions()
                        use_globals()

                        getSQuad()
                        genquad('begin_block',function_name,"_","_")

                        code_block()       

                        getLength()
                        genquad('end_block',function_name,"_","_")
                                          
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

        varIDs.append(token)

        ent = Entity.Var(token, 'var', getOffset())
        newEntity(ent)

        token = lexical_analyzer()

        while(token == ','):
            token = lexical_analyzer()
            if(token in IDs):
                varIDs.append(token)

                ent = Entity.Var(token, 'var', getOffset())
                newEntity(ent)

                token = lexical_analyzer()		
            else:
                print("Error! Needs a legitimate variable ID in line: "+str(line))
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
    global line

    assgnmnt_ID = token
    token = lexical_analyzer()
    if(token in IDs):
        if(token =='='):
            token = lexical_analyzer()
            if(token == 'int'):
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
                                    genquad(':=','input','_',assgnmnt_ID)
                                    token = lexical_analyzer()
                                else:
                                    print("Error Missing ')' in line"+str(line))
                                    exit()
                            else:
                                print("Error Missing ')' in line"+str(line))
                                exit()
                        else:
                            print("Error Missing '(' in line "+ str(line))
                            exit()
                    else:
                        print("Error Missing 'input' in line" + str(line))
                        exit()    
                else:
                    print("Error Missing '(' in line"+str(line))
                    exit()
            else:
                E = expression()
                genquad(':=',E,'_',assgnmnt_ID)
        else:
            print('Expected = at line '+str(line))
            exit()
    else:
        print('Error! Variable not fount in line '+str(line))
        exit()
		
def if_stat():
        global line 
        global token
        token = lexical_analyzer()

        B = condition()
        
        if( token== ":" ):
            token = lexical_analyzer()
            backpatch(B[0],nextquad())
            code_block()

            iflst = makeList(nextquad())
            genquad('jump','_','_','_')
            backpatch(B[1],nextquad())

            while(token == "elif"):
                elif_choice()
                
            if(token == 'else'):
                else_choice()
            
            backpatch(iflst,nextquad())
        else:
            print("Error! Missing ':' in line: "+str(line))	
            exit()

def elif_choice():
    global token
    token = lexical_analyzer()

    B = condition()

    if(token == ':'):
        token = lexical_analyzer()
        backpatch(B[0],nextquad())
        code_block()

        iflst = makeList(nextquad())
        genquad('jump','_','_','_')
        backpatch(B[1],nextquad())

        backpatch(iflst,nextquad())
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
     token = lexical_analyzer()   
     E = expression()
     genquad('ret',E,'_','_')

def print_stat():
     global token 
     token = lexical_analyzer()

     if(token == "("):
        token = lexical_analyzer()         
        E = expression()
        genquad('out',E,'_','_')

        if(token == ")"):
            token= lexical_analyzer()

        else:
            print("Error Missing ')' in line " +str(line))
            exit()
     else:
          print("Error Missing '(' in line " +str(line))
          exit()

def while_stat():
    global token
    global line

    token = lexical_analyzer()

    Bq = nextquad()
    B = condition()
    
    if(token == ':'):
        token = lexical_analyzer()
        if(token == '#{'):
            token = lexical_analyzer()      
            backpatch(B[0],nextquad())

            code_block()

            genquad('jump','_','_',Bq)
            backpatch(B[1],nextquad())

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

    op_s = optional_sign()
    T1 = term()

    if(op_s == '-'):
        temp = newtemp()
        genquad('-',0,T1,temp)
        T1 = temp
    
    while(token == '+' or token == '-'):
        addOp = ADD_OP()
        T2 = term()

        w = newtemp()
        genquad(addOp,T1,T2,w)
        T1 = w
    
    return T1

def term():
    global token
    F1 = factor()

    while(token == '*' or token == '//' or token == '%'):
        mulOp = MUL_OP()
        F2 = factor()

        w = newtemp()
        genquad(mulOp,F1,F2,w) 
        F1 = w

    return F1

def factor():
    global token
    if(token.isdigit()):
        F = token
        token = lexical_analyzer()
        return F
    
    elif(token in IDs):
        temp = token
        token=lexical_analyzer()
        F = idtail(temp)
        return F

    elif(token=='('):
        token = lexical_analyzer()     
        E = expression()

        if(token ==')'):
            token = lexical_analyzer()
            return E
        else:	
            print("Error! Missing ')' in line "+str(line)) 
            exit()   
    else:
        print("Error! '(' or ID or number expected in line "+str(line))
        exit()

def condition():
    global token

    Q1 = bool_term()

    conditionT = Q1[0]
    conditionF = Q1[1]

    while(token=="or"):
        backpatch(conditionF,nextquad())
        token=lexical_analyzer()
        
        Q2 = bool_term()

        conditionT = merge(conditionT,Q2[0])
        conditionF = Q2[1]

    return conditionT,conditionF

def bool_term():
    global token
    R1 = bool_factor()
    booltermT = R1[0]
    booltermF = R1[1]

    while(token == 'and'):  
        backpatch(booltermF,nextquad())

        token =  lexical_analyzer()

        R2 = bool_factor()
        booltermT = R2[0]
        booltermF = merge(booltermF,R2[1])

    return booltermT,booltermF

def bool_factor():
    global token
    global line

    if(token == 'not'):
        token = lexical_analyzer()
        B = condition()
        boolfactorT = B[1]
        boolfactorF = B[0]
        return (boolfactorF,boolfactorT)
    
    else:
        E1 = expression()
        rel_op = REL_OP()
        E2 = expression()

        Rtrue = makeList(nextquad())
        genquad(rel_op,E1,E2,'_')
        Rfalse = makeList(nextquad())
        genquad('jump','_','_','_')

    return Rtrue,Rfalse

def idtail(f_id):
    global token
    global line

    if(token == '('):
        token = lexical_analyzer()
        actual_par_list()

        w = newtemp()
        genquad('par', w, 'RET', '_')
        genquad('call', f_id, '_', '_')
        if(token == ')'):
            token = lexical_analyzer()
        else:
            print("Error! Missing ')' in line "+str(line))
            exit()

        return w
    
    return f_id	

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
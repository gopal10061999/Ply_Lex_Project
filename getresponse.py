import ply.lex as lex
import ply.yacc as yacc
import sys


str1 = ""
### DEFINING TOKENS###
tokens = ('BEGINTABLE', 'END','HEADING','START','START2','TITLE','GETDATA','ULE','ULS',
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN','CLOSESPAN', 
'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE','OPENPARA','CLOSEPARA')

def t_START(t):
    r'<h3[^>]*>'
    return t

def t_ULS(t):
    r'<ul[^>]*>'
    # return t
def t_ULE(t):
    r'</ul>'
    # return t

def t_HEADING(t):
    r'[0-9][0-9]?.(January|February|March|April|May|June|July|August|September|Octomber|November|December)'
    return t

def t_START2(t):
    r'</h3[^>]*>'
    return t

def t_END(t):
    r'<h(1|2|3|4|5)[^>]*>'


def t_OPENPARA(t):
    r'<p[^>]*>'
    # return t

def t_OPENHREF(t):
    r'<a[^>]*>'


def t_CLOSEHREF(t):
    r'</a[^>]*>'


def t_CLOSEPARA(t):
    r'</p[^>]*>'
    # return t

def t_OPENSTYLE(t):
    r'<style[^>]*>[^<]*</style>'

def t_CLOSESTYLE(t):
    r'</style[^>]>'


def t_WRONGDATA(t):
    r'&\#91;[0-9a-zA-Z]+&\#93; | &\#160;'

def t_OPENROW(t):
    r'<tr[^>]*>'

def t_CLOSEROW(t):
    r'</tr[^>]*>'

def t_CONTENT(t):
    r'[A-Za-z0-9,. ()\'–-]+'
    return t

def t_TITLE(t):
    r'</Title>'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)


############################################################# GRAMMAR RULES #############################################################

def p_start(p):
    '''start : table'''

def p_table(p):
    '''table : START HEADING data START2 data START
             | START2 data START'''
    global str1
    
    if(len(p)==7):
        str1 = str1 + '\n'+p[2]+": "+p[5]
    else:
        str1 = str1 + p[2]

# def p_par(p):
#     '''par : par OPENPARA data CLOSEPARA
#            | par ULS data ULE
#            | empty'''
#     if(len(p)==5):
#         print(p[3])
def p_data(p):
    '''data : CONTENT
            | data CONTENT'''
    if(len(p)==2):
        p[0]=p[1]
    else :
        p[0]=p[1]+p[2]
    # print(p[0])
def p_empty(p):
    '''empty :'''
    pass
flag=0
def p_error(p):
    global flag
    if flag==0:
        flag=1
        pass
    else:
        global str1
        try:
            str1 = str1 +'\n'+ p.value+": "
        except:

            pass
        pass


######### DRIVER FUNCTION#######

import sys
import ply.lex as lex
import ply.yacc as yacc

def main():
    try:
        file_obj = open('news.html', 'r', encoding="utf-8")
        data = file_obj.read()
        file_obj.close()

        parsed_data = parse_news_data(data)

        filename = sys.argv[1]
        write_parsed_data_to_file(parsed_data, filename)
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_news_data(data):
    lexer = lex.lex()
    lexer.input(data)
    parser = yacc.yacc()
    return parser.parse(data)

def write_parsed_data_to_file(parsed_data, filename):
    with open(filename, 'w') as file:
        file.write(parsed_data)

if __name__ == '__main__':
    main()


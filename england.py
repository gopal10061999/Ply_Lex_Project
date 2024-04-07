import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import sys
import re
name = ""
temp = ''
date = ""
player = 0
tokens = ('BEGIN', 'DATE', 'CLOSEROW', 'YES',
 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'PATTERN', 'OPENLIST', 'CLOSELIST',
'CONTENT', 'OPENDATA', 'CLOSEDATA', 'OPENSPAN', 'CLOSESPAN',
'OPENDIV', 'CLOSEDIV', 'GARBAGE')
t_ignore = '\t '


str1 = ""

###############Tokenizer Rules################
def t_DATE(t):
     r'(0?[1-9]|[12][0-9]|3[01])\s(?:January.–|February.–|February.-|March.–|April.–|May.–|June.–|July.–|August.–|September.–|October.–|November.–|December.–)'
    #  print("here")
     return t

def t_OPENLIST(t):
    r'<li>'
    return t

def t_CLOSELIST(t):
    r'</li>'
    return t

def t_WRONGDATA(t):
    r'&\#91;[0-9a-zA-Z]+&\#93; | &\#160;'

def t_CONTENT(t):
    r'[A-Za-z0-9,\(\)\-–\.:\'— ]+'
    return t

def t_GARBAGE(t):
    r'(<[^>]*>)'

def t_error(t):
    t.lexer.skip(1)

# def p_additionaldata(p):
#     '''
#     additionaldata : DATE content additionaldata
#                     | 
#     '''
#     if(len(p)==4):
#         p[0] = p[1]+p[2]+p[3]
#     else:
#         p[0] = ""
# def p_handlelist(p):
#     '''
#     handlelist : OPENLIST content CLOSELIST handlelist
#             | 
#     '''
#     global name
#     if(len(p)==5):
#         name = name + '\n'

def p_start(p):
    '''
    start : OPENLIST DATE content CLOSELIST
          | DATE content CLOSELIST
    '''
    global name
    global str1
    if(len(p)==5):
        pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        matches = re.findall(pattern, p[2])
        # print()
        # print(matches[0])
        # print()
        str1 = str1 + p[2].split(' –')[0]+':'+name +'\n'
        # print(p[2].split(' –')[0],':',name)
        name = ""
    elif(len(p)==4):
        pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        matches = re.findall(pattern, p[1])
        # print()
        # print(matches[0])
        # print()
        # global str1
        str1 = str1 + p[1].split(' –')[0]+':'+name+'\n'
        # print(p[1].split(' –')[0],':',name)
        name = ""

def p_content(p):
    '''
    content : CONTENT content
            | DATE content
            | OPENLIST content CLOSELIST content
            | 
    '''
    global name
    global temp
    if(len(p)==3):
        name = p[1]+name
        
    
    # if(len(p)== 5):
        # name = p[2] +'\n' + name
        # print(p[2])


def p_skipstart(p):
    '''
    skipstart : GARBAGE skipstart
              |  
    '''


# def p_skiptag(p):
#     '''
#     skiptag : OPENDATA skiptag
#             | CONTENT skiptag
#             | CLOSEDATA skiptag
#             | OPENHREF skiptag
#             | CLOSEHREF skiptag
#             | OPENSPAN skiptag
#             | CLOSESPAN skiptag
#             | OPENDIV skiptag
#             | CLOSEDIV skiptag
#             | PATTERN skiptag
#             | GARBAGE skiptag
#             | OPENI skiptag
#             | CLOSEI skiptag
#             | YES contract
#             | 

#     '''
    # print("skiptag")

# def p_contract(p):
#     '''
#     contract : skiptag
#     '''
#     # print("contract")
#     global player
#     player = 1

def p_error(p):
    pass
    # if p:
    #     print("Syntax error at '%s'" % p)
    # else:
    #     print("Syntax error at EOF")
    # return

def main():
    try:
        file_obj = open('countrynews.html', 'r', encoding="utf-8")
        data = file_obj.read()
        lexer = lex.lex()
        lexer.input(data)
        parser = yacc.yacc()
        parser.parse(data)
    except FileNotFoundError:
        print("Error: File 'countrynews.html' not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    def extract_date(line):
        parts = line.split(' ')
        try:
            date = int(parts[0])
            month = parts[1]
            return (date, month)
        except ValueError:
            return None

    filename = sys.argv[1] if len(sys.argv) > 1 else "output.txt"

    try:
        with open(filename, 'w') as file:
            global str1
            lines = str1.strip().split('\n')
            new_lines = [line for line in lines if extract_date(line)]
            sorted_lines = sorted(new_lines, key=extract_date)
            sorted_string = '\n'.join(sorted_lines)
            file.write(sorted_string)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

if __name__ == '__main__':
    main()
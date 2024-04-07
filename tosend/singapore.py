import ply.lex as lex
import ply.yacc as yacc
import sys
import re

# Global variables
name = ""
str1 = ""

# Token definitions
tokens = (
    'DATE', 'OPENLIST', 'CLOSELIST', 'CONTENT', 'GARBAGE'
)

# Ignore whitespace and tabs
t_ignore = ' \t'

# Token rules
def t_DATE(t):
    r'(0?[1-9]|[12][0-9]|3[01])\s(?:January:|February:|March:|April:|May:|June:|July:|August:|September:|October:|November:|December:)'
    return t

def t_OPENLIST(t):
    r'<li>'
    return t

def t_CLOSELIST(t):
    r'</li>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9,\(\)\-–\.:\'— ]+'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Grammar rules
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
        str1 = str1 + p[2].split(' –')[0] + name + '\n'
        name = ""
    elif(len(p)==4):
        pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        matches = re.findall(pattern, p[1])
        str1 = str1 + p[1].split(' –')[0] + name + '\n'
        name = ""

def p_content(p):
    '''
    content : CONTENT content
            | DATE content
            | OPENLIST content CLOSELIST content
            | 
    '''
    global name
    if(len(p) == 3):
        name = p[1] + name

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def main():
    try:
        file_obj = open('countrynews.html', 'r', encoding="utf-8")
        data = file_obj.read()
        file_obj.close()

        lexer = lex.lex()
        lexer.input(data)
        parser = yacc.yacc()
        parser.parse(data)

        filename = sys.argv[1]

        with open(filename, 'w') as file:
            global str1
            lines = str1.strip().split('\n')
            new_line=[]
            for line in lines:
                parts = line.split(' ')
                try:
                    date = int(parts[0])
                    new_line.append(line)
                except:
                    continue
            sorted_lines = sorted(new_line, key=lambda x: int(x.split(' ')[0]))
            sorted_string = '\n'.join(sorted_lines)

            file.write(sorted_string)

    except FileNotFoundError:
        print("Error: File not found")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    main()

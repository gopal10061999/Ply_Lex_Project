import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import re
name = ""
date = ""
player = 0
tokens = ('DATE','XAXIS', 'CLOSEDATA','BREAK','CATEGORY','OPENP', 'OPENCLOSETAG','CLOSEP', 'CLOSEL', 'CONTENT',  'PCONTENT', 'LCONTENT')
t_ignore = '\t '

###############Tokenizer Rules################
def t_DATE(t):
     r'((?:On|By|Also.on|Still.on|As.of|On.[a-z ]*|From)\s(0?[1-9]|[12][0-9]|3[01])(&\#160;\s|&\#160;|\s)(?:January|February|March|April|May|June|July|August|September|October|November|December))|On.the.same.day'
     return t

def t_OPENCLOSETAG(t):
    r'<img[^>]*>'
    return t

def t_LCONTENT(t):
    r'<li>(?!On\b|Also\b|From\b|Still\b|As\b|By\b)\w+'
    return t

def t_BREAK(t):
    r'<br[^>]*>'
    return t

def t_CATEGORY(t):
    r'categories:.\['
    return t

def t_PCONTENT(t):
    r'<p>(?!On\b|Also\b|From\b|Still\b|As\b|By\b)\w+'
    return t

def t_XAXIS(t):
    r'xAxis:.{'
    return t

def t_OPENP(t):
    r'<p>'
    return t

def t_WRONGDATA(t):
    r'&\#91;[0-9a-zA-Z]+&\#93; | &\#160;'

def t_CONTENT(t):
    r'[A-Za-z0-9, ]+'
    return t

def t_CLOSEL(t):
    r'</li>'
    return t

def t_CLOSEP(t):
    r'</p>'
    return t


def t_CLOSEDATA(t):
    r'\]'
    return t


def t_error(t):
    t.lexer.skip(1)


def p_start(p):
    '''
    start : startingdata additional start
          | 
          
    '''

def p_startingdata(p):
    '''
    startingdata : OPENP DATE content CLOSEP
                 | DATE content CLOSEP
    '''
    pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
    
    global name
    # print("starting")
    with open('Australia_(Jan-Jun 21).txt', 'a') as the_file:
        if(len(p)==5):
            p[2] = re.sub(r'&#160;', ' ', p[2])
            matches = re.findall(pattern, p[2])
            the_file.write(f'\n')
            if matches:
                the_file.write(matches[0]+":")
            the_file.write(p[2]+" "+name)
            name = ""
        elif(len(p)==4):
            p[1] = re.sub(r'&#160;', ' ', p[1])
            matches = re.findall(pattern, p[1])
            the_file.write(f'\n')
            if matches:
                the_file.write(matches[0]+":")
            the_file.write(p[1]+" "+name)
            name = ""
  
def p_additional(p):
    '''
    additional : additionaldata additional
               | 
    '''
    

def p_additionaldata(p):
    '''
    additionaldata : porlcontent CLOSEP  
                   | porlcontent CLOSEL
    '''
    global name
    with open('Australia_(Jan-Jun 21).txt', 'a') as the_file:
        the_file.write(f'\n')
        the_file.write(name)
        # print(name)
        name = ""

def p_porlcontent(p):
    '''
    porlcontent : PCONTENT content porlcontent
                | LCONTENT content porlcontent
            | 
    '''
    global name
    pattern = r'<p>|<li>'
    if(len(p)==4):
        p[1] = re.sub(pattern, '', p[1])
        name = p[1]+name
    

def p_content(p):
    '''
    content : CONTENT content
            | DATE content
            | 
    '''
    global name
    pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
    
    if(len(p)==3):
        name = p[1]+name

def p_error(p):
    pass
    # if p:
    #     print("Syntax error at '%s'" % p)
    # else:
    #     print("Syntax error at EOF")
    # return


def fetch_webpage(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        return webpage.decode("utf8")
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return None

def write_to_file(data, filename):
    try:
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(data)
        print("Webpage saved to file:", filename)
    except Exception as e:
        print(f"Error writing to file: {e}")

def read_from_file(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file_obj:
            return file_obj.read()
    except Exception as e:
        print(f"Error reading from file: {e}")
        return None

def lex_webpage(data):
    try:
        lexer = lex.lex()
        lexer.input(data)
        print("Lexing completed")
        return lexer
    except Exception as e:
        print(f"Error during lexing: {e}")
        return None

def parse_webpage(parser, data):
    try:
        parser.parse(data)
        print("Parsing completed")
    except Exception as e:
        print(f"Error during parsing: {e}")

def main():
    url = 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(January%E2%80%93June_2021)'
    filename = 'webpage.html'
    data = fetch_webpage(url)
    if data:
        write_to_file(data, filename)
        data = read_from_file(filename)
        if data:
            lexer = lex_webpage(data)
            if lexer:
                parser = yacc.yacc()
                parse_webpage(parser, data)

if __name__ == '__main__':
    main()
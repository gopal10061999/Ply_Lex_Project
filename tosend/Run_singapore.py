import os
import subprocess
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen

# Global variables
current_directory = os.path.dirname(os.path.abspath(__file__))
links = {}

# Token definitions
tokens = (
    'BEGINTABLE', 'ENDDATA', 'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
    'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'CONTENT', 'OPENDATA',
    'CLOSEDATA', 'OPENSPAN', 'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE',
    'CLOSESTYLE', 'GARBAGE', 'IGNOREDATA'
)

# Token rules
t_ignore = '\t'

def t_BEGINTABLE(t):
    r'<a.href="/wiki/Timeline_of_the_COVID-19_pandemic_in_Singapore"'
    return t

def t_ENDDATA(t):
    r'<a.href="/wiki/Timeline_of_the_COVID-19_pandemic_in_Thailand"'
    return t

def t_OPENTABLE(t):
    r'<tbody[^>]*>'
    return t

def t_CLOSETABLE(t):
    r'</tbody[^>]*>'
    return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    return t

def t_CLOSEROW(t):
    r'</tr[^>]*>'
    return t

def t_OPENHEADER(t):
    r'<th[^>]*>'
    return t

def t_CLOSEHEADER(t):
    r'</th[^>]*>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_OPENDIV(t):
    r'<div[^>]*>'
    return t

def t_CLOSEDIV(t):
    r'</div[^>]*>'
    return t

def t_OPENSTYLE(t):
    r'<style[^>]*>'
    return t

def t_CLOSESTYLE(t):
    r'</style[^>]*>'
    return t

def t_OPENSPAN(t):
    r'<span[^>]*>'
    return t

def t_CLOSESPAN(t):
    r'</span[^>]*>'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t

def t_IGNOREDATA(t):
    r'&nbsp; | (160;)'
    pass

def t_CONTENT(t):
    r'[A-Za-z0-9, ()–]+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Grammar rules
def p_start(p):
    '''start : table'''
    # p[0] = p[1]

def p_links(p):
    '''links : OPENHREF CONTENT links 
             | CONTENT links
             | '''
    if len(p) == 4:
        p[0] = p[1] + p[3]
        global links
        links[p[2]] = p[0]
    else: 
        p[0] = ''

def printoutput():
    links_dict = {}

    for key, value in links.items():
        link = "https://en.wikipedia.org" + value.split('"')[1]
        links_dict[key] = link

    for query in links_dict:
        req = Request(links_dict[query], headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        mydata = webpage.decode("utf8")
        f = open('countrynews.html', 'w', encoding="utf-8")
        f.write(mydata)
        f.close()
        subprocess.run(["python3", os.path.join(current_directory, "singapore.py"), f'{query}.txt'])
        
def p_table(p):
    '''table : BEGINTABLE  links ENDDATA'''

def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    pass

# Driver function
def main():
    url = f"https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic"

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = open('Timeline of the COVID-19 pandemic.html', 'w', encoding="utf-8")
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    f.write(mydata)
    f.close()

    file_obj = open('Timeline of the COVID-19 pandemic.html', 'r', encoding="utf-8")
    data = file_obj.read()
    lexer = lex.lex()
    lexer.input(data)
    parser = yacc.yacc()
    parser.parse(data)
    file_obj.close()
    printoutput()

if __name__ == '__main__':
    main()

import os
import subprocess
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen

# Global variables
links = {}

# Token definitions
tokens = (
    'BEGINTABLE', 'ENDDATA', 'OPENTABLE', 'CLOSETABLE',
    'OPENROW', 'CLOSEROW', 'OPENHEADER', 'CLOSEHEADER',
    'OPENHREF', 'CLOSEHREF', 'CONTENT', 'OPENDATA',
    'CLOSEDATA', 'OPENSPAN', 'CLOSESPAN', 'OPENDIV',
    'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE', 'GARBAGE',
    'IGNOREDATA'
)

# Ignored characters
t_ignore = '\t'

# Token rules
def t_BEGINTABLE(t):
    r'<a.href="/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia"'
    return t

def t_ENDDATA(t):
    r'<a.href="/wiki/Timeline_of_the_COVID-19_pandemic_in_Fiji"'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, ()–]+'
    return t

def t_IGNOREDATA(t):
    r'&nbsp; | (160;)'
    pass

def t_error(t):
    t.lexer.skip(1)

# Parser rules
def p_start(p):
    '''start : table'''

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

def p_table(p):
    '''table : BEGINTABLE links ENDDATA'''

def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    pass

# Function to print output and call subprocesses
def printoutput():
    links_dict = {}
    for key, value in links.items():
        link = "https://en.wikipedia.org" + value.split('"')[1]
        links_dict[key] = link

    subprocess.run(["python3", os.path.join(current_directory, "2022.py"), 'Australia (2022)'])
    subprocess.run(["python3", os.path.join(current_directory, "21_2.py"), 'Australia (July–December 2021)'])
    subprocess.run(["python3", os.path.join(current_directory, "21_1.py"), 'Australia (January–June 2021)'])
    subprocess.run(["python3", os.path.join(current_directory, "2020.py"), 'Australia (2020)'])

def main():
    url = "https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = open('Timeline of the COVID-19 pandemic.html', 'w', encoding="utf-8")
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    f.write(mydata)
    f.close()

    with open('Timeline of the COVID-19 pandemic.html', 'r', encoding="utf-8") as file_obj:
        data = file_obj.read()
        lexer = lex.lex()
        lexer.input(data)
        parser = yacc.yacc()
        parser.parse(data)

    printoutput()

if __name__ == '__main__':
    main()

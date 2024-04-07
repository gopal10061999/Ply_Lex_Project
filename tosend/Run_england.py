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
    r'<a.href="/wiki/Timeline_of_the_COVID-19_pandemic_in_the_United_Kingdom"'
    return t

def t_ENDDATA(t):
    r'<h3><span.class="mw-headline".id="Oceania">Oceania'
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
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, ()–]+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
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
        substring = "England"
        if p[2].find(substring) != -1:
            links[p[2]] = p[0]
    else: 
        p[0] = ''

def p_table(p):
    '''table : BEGINTABLE  links ENDDATA'''

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

    for query in links_dict:
        req = Request(links_dict[query], headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        mydata = webpage.decode("utf8")
        with open('countrynews.html', 'w', encoding="utf-8") as f:
            f.write(mydata)
        subprocess.run(["python3", os.path.join(current_directory, "england.py"), f'{query}.txt'])

def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    url = "https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with open('Timeline of the COVID-19 pandemic.html', 'w', encoding="utf-8") as f:
        webpage = urlopen(req).read()
        mydata = webpage.decode("utf8")
        f.write(mydata)

    with open('Timeline of the COVID-19 pandemic.html', 'r', encoding="utf-8") as file_obj:
        data = file_obj.read()
        lexer = lex.lex()
        lexer.input(data)
        parser = yacc.yacc()
        parser.parse(data)

    printoutput()

if __name__ == '__main__':
    main()

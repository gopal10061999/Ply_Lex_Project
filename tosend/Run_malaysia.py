import os
import subprocess
from urllib.request import Request, urlopen
import ply.lex as lex
import ply.yacc as yacc

# Global variables
current_directory = os.path.dirname(os.path.abspath(__file__))
links = {}

# Token definitions
tokens = ('BEGINTABLE', 'ENDDATA', 'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
          'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'CONTENT', 'OPENDATA',
          'CLOSEDATA', 'OPENSPAN', 'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE',
          'CLOSESTYLE', 'GARBAGE', 'IGNOREDATA')

# Token rules
def t_BEGINTABLE(t):
    r'<a.href="/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia"'
    return t

def t_ENDDATA(t):
    r'<li><span.class="flagicon"><span.typeof="mw:File"><span><img.alt="".src="'
    return t

def t_OPENTABLE(t):
    r'<tbody[^>]*>'

def t_CLOSETABLE(t):
    r'</tbody[^>]*>'

def t_OPENROW(t):
    r'<tr[^>]*>'

def t_CLOSEROW(t):
    r'</tr[^>]*>'

def t_OPENHEADER(t):
    r'<th[^>]*>'

def t_CLOSEHEADER(t):
    r'</th[^>]*>'

def t_OPENHREF(t):
    r'<a[^>]*>'
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

# Error handling for lexer
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Error handling for parser
def p_error(p):
    pass

# Grammar rules...
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Error handling for parser
def p_error(p):
    pass

# Grammar rules...
def p_start(p):
    '''start : table'''
    # p[0] = p[1]

def p_links(p):
    '''links : OPENHREF CONTENT links 
             | CONTENT links
             | '''
    if len(p) ==4:
        p[0] = p[1] + p[3]
        global links
        links[p[2]] = p[0]
    else: 
        p[0]=''

def p_table(p):
    '''table : BEGINTABLE  links ENDDATA'''

def parse_webpage(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            webpage = response.read().decode("utf8")
            return webpage
    except Exception as e:
        print(f"Error fetching webpage: {e}")
        return None

def write_to_file(filename, data):
    try:
        with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
            file.write(data)
    except Exception as e:
        print(f"Error writing to file: {e}")

def print_output(links_dict):
    for query in links_dict:
        try:
            req = Request(links_dict[query], headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req) as response:
                webpage = response.read().decode("utf8")
                with open('countrynews.html', 'w', encoding="utf-8") as f:
                    f.write(webpage)
                subprocess.run(["python3", os.path.join(current_directory, "malaysia.py"), f'{query}.txt'])
        except Exception as e:
            print(f"Error processing link: {e}")

def main():
    url = "https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic"

    webpage = parse_webpage(url)
    if webpage:
        try:
            with open('Timeline_of_the_COVID-19_pandemic.html', 'w', encoding="utf-8") as f:
                f.write(webpage)
        except Exception as e:
            print(f"Error writing to file: {e}")

        file_path = 'Timeline_of_the_COVID-19_pandemic.html'
        with open(file_path, 'r', encoding="utf-8") as file_obj:
            data = file_obj.read()
            lexer = lex.lex()
            lexer.input(data)
            parser = yacc.yacc()
            parser.parse(data)
            print_output(links)

if __name__ == '__main__':
    main()

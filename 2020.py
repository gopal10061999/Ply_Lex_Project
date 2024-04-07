import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import re
name = ""
date = ""
player = 0
tokens = ('DATE', 'OPENP','XAXIS','CATEGORY', 'CLOSEP', 'CLOSEDATA','CONTENT')
t_ignore = '\t '


def read_from_file(file_name):
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            data = f.read()
        return data
    except Exception as e:
        print(f"Error occurred while reading from file {file_name}: {e}")
        return None

###############Tokenizer Rules################
def t_DATE(t):
     r'(?:On|By|Also.on|Still.on|As.of|On.[a-z ]*|From)\s(0?[1-9]|[12][0-9]|3[01])\s(?:January|February|March|April|May|June|July|August|September|October|November|December)'
    #  print("here")
     return t


def t_CATEGORY(t):
    r'categories:.\['
    return t

def t_error(t):
    t.lexer.skip(1)

def t_OPENP(t):
    r'<p>'
    return t

def t_XAXIS(t):
    r'xAxis:.{'
    return t

def t_XAXIS(t):
    r'xAxis:.{'
    return t


def t_WRONGDATA(t):
    r'&\#91;[0-9a-zA-Z]+&\#93; | &\#160;'

def t_CLOSEDATA(t):
    r'\]'
    return t

def t_CLOSEP(t):
    r'</p>'
    return t



def t_CONTENT(t):
    r'[A-Za-z0-9,\(\)\-–\.:\'— ]+'
    return t


def p_start(p):
    '''
    start : OPENP DATE content CLOSEP
          | DATE content CLOSEP
    '''
    global name
    pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'

    try:
        with open('Australia_2020.txt', 'a') as the_file:
            if len(p) == 4:
                matches = re.findall(pattern, p[1])
                if matches:
                    the_file.write(f'\n')
                    the_file.write(matches[0] + ":")
                    the_file.write(p[1] + " " + name)
                    name = ""
            elif len(p) == 5:
                matches = re.findall(pattern, p[2])
                if matches:
                    the_file.write(f'\n')
                    the_file.write(matches[0] + ":")
                    the_file.write(p[2] + " " + name)
                    name = ""
    except Exception as e:
        print(f"Error occurred while writing to file: {e}")
def p_content(p):
    '''
    content : CONTENT content
            | DATE content
            | 
    '''
    global name
    if(len(p)==3):
        name = p[1]+name

def p_error(p):
    pass
    # if p:
    #     print("Syntax error at '%s'" % p)
    # else:
    #     print("Syntax error at EOF")
    # return
def parse_wikipedia_page(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf8")
        return webpage
    except Exception as e:
        print(f"Error occurred while fetching data from {url}: {e}")
        return None

def write_to_file(file_name, content):
    try:
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(content)
        print(f"Data written to file: {file_name}")
    except Exception as e:
        print(f"Error occurred while writing to file {file_name}: {e}")



def perform_lexical_analysis(data):
    try:
        lexer = lex.lex()
        lexer.input(data)
        print("Lexical analysis completed")
        return lexer
    except Exception as e:
        print(f"Error occurred during lexical analysis: {e}")
        return None

def perform_parsing(parser, data):
    try:
        parser.parse(data)
    except Exception as e:
        print(f"Error occurred during parsing: {e}")

def main():
    url = 'https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Australia_(2020)'
    
    # Fetch data from the Wikipedia page
    webpage = parse_wikipedia_page(url)
    if webpage is None:
        return

    # Write fetched data to a file
    write_to_file('webpage.html', webpage)

    # Read data from the file
    data = read_from_file('webpage.html')
    if data is None:
        return

    # Perform lexical analysis
    lexer = perform_lexical_analysis(data)
    if lexer is None:
        return

    # Parsing
    parser = yacc.yacc()
    perform_parsing(parser, data)

if __name__ == '__main__':
    main()
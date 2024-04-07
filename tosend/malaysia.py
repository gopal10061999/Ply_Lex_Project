import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import sys
import re

# Global variables
player_name = ""
output_data = ""

# Token definitions
tokens = (
    'DATE',
    'OPENP',
    'CLOSEP',
    'CONTENT',
    'GARBAGE'
)

# Ignored characters
t_ignore = ' \t'

# Token rules
def t_DATE(t):
    r'(?:On|By|As.of)\s(0?[1-9]|[12][0-9]|3[01])\s(?:January|February|March|April|May|June|July|August|September|October|November|December)'
    return t

def t_OPENP(t):
    r'<p>'
    return t

def t_CLOSEP(t):
    r'</p>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9,\(\)\-–\.:\'— ]+'
    return t

def t_GARBAGE(t):
    r'(<[^>]*>)'
    pass

def t_error(t):
    t.lexer.skip(1)

# Parsing rules
def p_start(p):
    '''
    start : OPENP DATE content CLOSEP
          | DATE content CLOSEP
    '''
    global output_data, player_name
    if len(p) == 5:
        pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        matches = re.findall(pattern, p[2])
        output_data = output_data + p[2].split(' –')[0] + ':' + player_name + '\n'
        player_name = ""
    elif len(p) == 4:
        pattern = r'\b\d{1,2}\s*(?:st|nd|rd|th)?\s+\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'
        matches = re.findall(pattern, p[1])
        output_data = output_data + p[1].split(' –')[0] + ':' + player_name + '\n'
        player_name = ""

def p_content(p):
    '''
    content : CONTENT content
            | DATE content
            | 
    '''
    global player_name
    if len(p) == 3:
        player_name = p[1] + player_name

def p_error(p):
    pass

# Main function
def main():
    # Fetch webpage data
    try:
        req = Request('https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2020)', headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        webpage_data = webpage.decode("utf8")
        with open('webpage.html', 'w', encoding="utf-8") as f:
            f.write(webpage_data)
    except Exception as e:
        print("Error fetching webpage data:", e)
        return
    
    # Read data from a local file
    try:
        with open('countrynews.html', 'r', encoding="utf-8") as file_obj:
            data = file_obj.read()
    except Exception as e:
        print("Error reading local file:", e)
        return

    # Lexical analysis
    lexer = lex.lex()
    lexer.input(data)

    # Syntax parsing
    parser = yacc.yacc()
    parser.parse(data)

    # Function to extract and sort dates
    def extract_and_sort_dates(line):
        parts = line.split(' ')
        date = int(parts[0])
        month = parts[2]
        return {date, month}

    # Writing sorted data to a file
    try:
        filename = sys.argv[1]
        with open(filename, 'w') as file:
            global output_data
            output_data = output_data.replace("On ", "")
            lines = output_data.strip().split('\n')
            new_lines = [line for line in lines if line.strip()]
            sorted_lines = sorted(new_lines, key=extract_and_sort_dates)
            sorted_string = '\n'.join(sorted_lines)
            file.write(sorted_string)
    except Exception as e:
        print("Error writing to file:", e)

if __name__ == '__main__':
    main()

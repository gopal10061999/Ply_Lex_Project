import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import re

td_count = 0
continent_count = 1

tokens = ('BEGIN', 'OPENROW', 'CLOSEROW', 'OPENHEADER', 'OPENTABLE', 'OPENHREF', 'CLOSEHREF',
          'CLOSEHEADER', 'PATTERN', 'CONTENT', 'OPENDATA', 'CLOSEDATA', 'THEADOPEN', 'THEADCLOSE', 'GARBAGE')
t_ignore = '\t '

def t_BEGIN(t):
    r'<table.id="main_table_countries_yesterday".class="table.table-bordered.table-hover.main_table_countries".style="width:100%;margin-top:.0px.!important;display:none;">'
    print("begin")
    return t

def t_OPENTABLE(t):
    r'<tbody>'
    return t

def t_THEADOPEN(t):
    r'<thead>'
    return t

def t_THEADCLOSE(t):
    r'</thead>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_PATTERN(t):
    r'(&\#160;)|(&amp;)|(&\#91;[0-9]&\#93;)|\#|(&[a-z]*;)'
    # return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9,+\(\)\-–\/\.:\' ]+'
    return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    return t

def t_CLOSEROW(t):
    r'</tr[^>]*>'
    return t
def t_GARBAGE(t):
    r'(<[^>]*>)|(<\/[^>]*>)|(<[^\/>]*\/>)|<![^>]>'
    return t

def t_OPENHEADER(t):
    r'<th[^>]*>'
    return t


def t_CLOSEHEADER(t):
    r'</th[^>]*>'
    return t


def t_error(t):
    t.lexer.skip(1)

def p_start(p):
    ''' 
    start : BEGIN THEADOPEN skiptag THEADCLOSE OPENTABLE getdata
    '''

def p_skiptag(p):
    '''
    skiptag : GARBAGE skiptag 
            | PATTERN skiptag
            | OPENHEADER skiptag
            | CLOSEHEADER skiptag
            | CONTENT skiptag
            | OPENDATA skiptag
            | CLOSEDATA skiptag
            | OPENROW skiptag
            | CLOSEROW skiptag

            |
    '''
def p_getdata(p):
    '''
    getdata : OPENROW handledata CLOSEROW getdata
            | 
    '''

def p_handledata(p):
    '''
    handledata : onlydata handledata
               | 
    '''
def p_comment(p):
    '''
    comment : GARBAGE
            | 
    '''
def p_onlydata(p):
    '''
    onlydata : OPENDATA CLOSEDATA comment 
             | OPENDATA CONTENT CLOSEDATA comment 
             | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA comment
             | OPENDATA OPENHREF CONTENT CONTENT CLOSEHREF CLOSEDATA comment
             | OPENDATA GARBAGE GARBAGE CLOSEDATA comment
            | OPENDATA GARBAGE CONTENT GARBAGE CLOSEDATA comment
    '''
    if(len(p) == 8):
        # print("here")
        p[3] = p[3]+p[4]
    global td_count,continent_count
    td_count = td_count+1
    if p.slice[2].type == 'CONTENT':
        p[2] = p[2].split()[0]

    if continent_count != 7 and continent_count <= 8:
        with open('countries.txt', 'a') as the_file:
            if td_count == 2:
                the_file.write(f'{p[2].replace(" ", "_")} ' if p.slice[3].type != 'CONTENT' else f'{p[3].replace(" ", "_")} ')
            elif td_count in [3, 4, 5, 6, 7, 8, 9, 12, 13, 14]:
                the_file.write(f'{p[2]} ' if p.slice[2].type == 'CONTENT' else 'N/A ')
            
            if td_count == 22:
                the_file.write("\n")
                continent_count += 1
                td_count = 0

    elif continent_count==7:
        if td_count == 22:
            continent_count = continent_count+1
            td_count = 0
    else:
        with open('countries.txt', 'a') as the_file:
            if td_count == 2:
                content = p[3] if p.slice[3].type == 'CONTENT' else p[2].replace(" ", "_")
                content = content if content != "S. Korea" else "S._Korea"
                the_file.write(f'{content} ')
            elif td_count in [3, 4, 5, 6, 7, 8, 9, 12, 13, 14]:
                content = p[2] if p.slice[2].type == 'CONTENT' else "N/A"
                the_file.write(f'{content} ')
            if td_count == 22:
                the_file.write("\n")
                continent_count += 1
                td_count = 0


def p_error(p):
    
    if p:
        print("Syntax error at '%s'" % p)
    else:
        print("Syntax error at EOF")
    pass

def parse_webpage(data):
    try:
        lexer = lex.lex()
        lexer.input(data)
        print("Lex completed")
        parser = yacc.yacc()
        parser.parse(data)
    except Exception as e:
        print(f"An error occurred during parsing: {e}")

def main():
    try:
        # Open countries.txt for writing and close it immediately to clear its contents
        with open('countries.txt', 'w', encoding="utf-8"):
            pass

        # Fetch webpage and save it to a file
        req = Request('https://www.worldometers.info/coronavirus/', headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode("utf8")
        with open('webpage.html', 'w', encoding="utf-8") as f:
            f.write(webpage)

        # Read data from webpage.html
        with open('webpage.html', 'r', encoding="utf-8") as file_obj:
            data = file_obj.read()

        # Parse the webpage data
        parse_webpage(data)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
import ply.lex as lex
import ply.yacc as yacc
from urllib.request import Request, urlopen
import sys
import re
name = ""
temp = ''
date = ""
player = 0
tokens = ('BEGIN', 'DATE', 'BEGINTABLE', 'ENDTABLE',
'OPENHEADER', 'CLOSEHEADER','CLOSEANCHOR','OPENDIV','OPENPARA','CLOSEPARA','OPENLIST','CLOSELIST',
'CONTENT',  'OPENSPAN','CLOSEDIV','CLOSESPAN','GARBAGE','EXTRA','FIGUREO','FIGUREC','OPENANCHOR','CLOSEROW', 'YES',
 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF', 'PATTERN', 'OPENLIST', 'CLOSELIST',
'CONTENT', 'OPENDATA', 'CLOSEDATA', 'OPENSPAN', 'CLOSESPAN',
'OPENDIV', 'CLOSEDIV', 'GARBAGE')
t_ignore = '\t '


str1 =""
###############Tokenizer Rules################
def t_DATE(t):
     r'(0?[1-9]|[12][0-9]|3[01])\s(?:January:|February:|March:|April:|May:|June:|July:|August:|September:|October:|November:|December:)'
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

def t_BEGINTABLE(t):
    r'Pandemic.chronology</span>'
    return t

def t_OPENANCHOR(t):
    r'<aa[^>]*>'

def t_CLOSEANCHOR(t):
    r'</aa[^>]*>'

def t_OPENDIV(t):
    r'<di[^>]*>'

def t_CLOSEDIV(t):
    r'</di[^>]*>'

def t_HREF(t):
    r'href\s*=\s*\"[^\"]*\"'

def t_ENDTABLE(t):
    r'Summary</span>'
    return t

def t_FIGUREO(t):
    r'<figure[^>]*>'
    return t

def t_FIGUREC(t):
     r'</figure[^>]*>'
     return t

def t_OPENSPAN(t):
    r'<span[^>]*>'

def t_CLOSESPAN(t):
    r'</span[^>]*>'


def t_OPENHEADER(t):
    r'<h[^>]*>'
    return t 

def t_CLOSEHEADER(t):
    r'</h[^>]*>'
    return t

def t_OPENPARA(t):
    r'<p[^>]*>'
  

def t_CLOSEPARA(t):
    r'</p[^>]*>'
def t_OPENLIST(t):
    r'<li[^>]*>'
    # return t
  
def t_CLOSELIST(t):
    r'</li[^>]*>'
    # return t



def p_start(p):

    '''
    start : OPENLIST DATE content CLOSELIST
          | DATE content CLOSELIST
          | OPENDIV CONTENT CLOSEDIV
          | OPENHEADER CONTENT CLOSEHEADER
    '''
    global name
    global str1 
    if len(p) == 5:
        pattern = r'\b(\d{1,2}\s*(?:st|nd|rd|th)?)\s+(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b)\s+\d{4}'
        matches = re.findall(pattern, p[2])
        
        # Simulating additional processing based on matches
        if matches:
            name = "Matched"
        else:
            name = "Not Matched"

        str1 += f"{p[2].split(' –')[0]} {name}\n"
        name = ""

    elif len(p)==3:
        patterns = r'\b(\d{1,2}\s*(?:st|nd|rd|th)?)\s+(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b)\s+\d{4}'
        matchess = re.findall(pattern, p[2])
        if matchess:
            names = "Matched"
        else:
            names = "Not Matched"

        str1 += f"{p[2].split(' –')[0]} {names}\n"
        names=""

    elif len(p) == 4:
        pattern = r'\b(\d{1,2}\s*(?:st|nd|rd|th)?)\s+(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b)\s+\d{4}'
        matches = re.findall(pattern, p[1])
        
        # Simulating additional processing based on matches
        if matches:
            name = "Matched"
        else:
            name = "Not Matched"

        str1 += f"{p[1].split(' –')[0]} {name}\n"
        name = ""
    else:
        patterns = r'\b(\d{1,2}\s*(?:st|nd|rd|th)?)\s+(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b)\s+\d{4}'
        matchess = re.findall(pattern, p[1])
        
        # Simulating additional processing based on matches
        if matchess:
            names = "Matched"
        else:
            names = "Not Matched"

        str1 += f"{p[1].split(' –')[0]} {names}\n"
        names = ""


def p_content(p):
    '''
    content : CONTENT content
            | DATE content
            | OPENLIST content CLOSELIST content
            | OPENDIV CONTENT CLOSEDIV 
            | OPENHEADER CONTENT 
            | 
    '''
    global name
    global temp
    if(len(p)==3):
        name = p[1]+name
        
    elif(len(p)== 6):
        name = p[2] +'\n' + name
        print(p[2])


def p_skipstart(p):
    '''
    skipstart : GARBAGE skipstart
              |  
    '''

r = 1

def p_error(p):
    pass
   

def main():
    req = Request('https://en.wikipedia.org/wiki/Timeline_of_the_COVID-19_pandemic_in_Malaysia_(2020)',headers ={'User-Agent':'Mozilla/5.0'})
    webpage = urlopen(req).read()
    mydata = webpage.decode("utf8")
    f=open('webpage.html','w',encoding="utf-8")
    f.write(mydata)
    f.close
    file_obj = open('countrynews.html','r',encoding="utf-8")
    data = file_obj.read()
    lexer = lex.lex()
    lexer.input(data)
    # print("lex completed")
    for tok in lexer:
        tok=tok
        # print(tok)
    parser = yacc.yacc()
    parser.parse(data)

    def extract_date(line):
        parts = line.split(' ')
        date = int(parts[0])
        month = parts[1]
        return {date,month}

    filename = sys.argv[1]

    with open(filename, 'w') as file:
        global str1
        lines = str1.strip().split('\n')
        new_line=[]
        for line in lines:
            parts = line.split(' ')
            try :
                date = int(parts[0])
                new_line.append(line)
            except:
                continue
        sorted_lines = sorted(new_line, key=extract_date)
        sorted_string = '\n'.join(sorted_lines)

        file.write(sorted_string)



if __name__ == '__main__':
    main()
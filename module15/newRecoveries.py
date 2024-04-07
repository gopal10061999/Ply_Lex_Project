import ply.lex as lex
import ply.yacc as yacc

class WebPageParser:
    def __init__(self):
        self.env = {}
        self.dates = []
        self.new_recoveries = []

    # Token definitions
    tokens = (
        'OPENTITLE', 'TITLE', 'XAXIS', 'CATEGORY', 'CLOSETITLE', 'START', 'NAME', 'OPENDATA', 'CLOSEDATA', 'STYLE',
        'CONTENT'
    )
    t_ignore = r' \t\n '

    # Token rules
    def t_OPENTITLE(self, t):
        r'(title|itle):.{'
        return t

    def t_TITLE(self, t):
        r'(text|ext):.\'(New.Cases.vs\..New.Recoveries|Daily.New.Cases)\''
        return t

    def t_NAME(self, t):
        r'(name|ame):.\'New.Recoveries\','
        return t

    def t_STYLE(self, t):
        r'[A-Za-z0-9]+:.[^,]+,'
        return t

    def t_CONTENT(self, t):
        r'[^<>\n\t\[\]]+'
        return t
    
    def t_CLOSETITLE(self, t):
        r'},'
        return t

    def t_XAXIS(self, t):
        r'xAxis:.{'
        return t

    def t_CATEGORY(self, t):
        r'categories:.\['
        return t

    def t_START(self, t):
        r'series:.\[{'
        return t
    def t_OPENDATA(self, t):
        r'data:.\['
        return t

    def t_CLOSEDATA(self, t):
        r'\]'
        return t

    def t_error(self, t):
        t.lexer.skip(1)

    # Parser rules
    def p_start_d(self, p):
        '''start_d : OPENTITLE TITLE CLOSETITLE skiptag'''

    def p_skiptag(self, p):
        '''skiptag : STYLE skiptag
                   | CONTENT skiptag
                   | XAXIS CATEGORY getdate'''

    def p_getdate(self, p):
        '''getdate : CONTENT CLOSEDATA CLOSETITLE skiptag1'''
        self.env['date'] = p[1]

    def p_skiptag1(self, p):
        '''skiptag1 : STYLE skiptag1
                    | CONTENT skiptag1
                    | OPENDATA skiptag1
                    | CLOSEDATA skiptag1
                    | CLOSETITLE skiptag1
                    | start'''

    def p_start(self, p):
        '''start : START NAME getdata'''

    def p_getdata(self, p):
        '''getdata : STYLE getdata
                   | OPENDATA getcontent'''

    def p_getcontent(self, p):
        '''getcontent : CONTENT CLOSEDATA'''
        self.env['data'] = p[1]

    def p_error(self, p):
        pass

    def get_new_recoveries(self):
        file_obj = open('webpage.html', 'r', encoding="utf-8")
        data = file_obj.read()
        lexer = lex.lex(module=self)
        lexer.input(data)
        parser = yacc.yacc(module=self)
        try:
            parser.parse(data)
            dates = self.env['date'].split('"')
            self.dates = [i for i in dates if i != '' and i != ',']
            self.new_recoveries = self.env['data'].split(',')
            del self.env['data']
            del self.env['date']
        except Exception as e:
            print("Error:", e)
            self.new_recoveries = 'N/A'
            self.dates = 'N/A'
        return self.dates, self.new_recoveries


if __name__ == '__main__':
    parser = WebPageParser()
    dates, new_recoveries = parser.get_new_recoveries()
    for i in range(len(dates)):
        print(f'{dates[i]}\t{new_recoveries[i]}')

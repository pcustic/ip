from tip import Parser, Token, AST, Tokenizer, vrsta
import enum

class Ar(enum.Enum):
    PRAZNO, KRAJ, GREŠKA = range(3)
    BROJ = 3

    PLUS = '+'
    MINUS = '-'
    PUTA = '*'
    POT = '^'
    OTVORENA = '('
    ZATVORENA = ')'


def aritm_lex(kod):
    lex = Tokenizer(kod)
    while True:
        znak = lex.pogledaj()
        vr = vrsta(znak)
        if vr == 'kraj': yield Token(Ar.KRAJ, ''); return
        elif vr == 'praznina': Token(Ar.PRAZNO, lex.praznine())
        elif vr == 'znamenka': yield Token(Ar.BROJ, lex.broj())
        elif znak == '-': yield Token(Ar.BROJ, lex.čitaj() + lex.broj())
        elif znak in '+*^()': yield Token(Ar(znak), lex.čitaj())
        else:
            yield Token(Ar.GREŠKA, lex.čitaj())

class AritmParser(Parser):
    def izraz(self):
        



        

def aritm_parse(niz_znakova):
    parser = AritmParser(aritm_lex(niz_znakova))
    rezultat = parser.izraz()
    parser.pročitaj(Ar.KRAJ)
    return rezultat
    
if __name__ == '__main__':
    print(*aritm_lex('1+43*3+4^5'), sep='\n')

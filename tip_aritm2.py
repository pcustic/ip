# Tokenizer i parser za aritmeticke izraze sa zbrajanjem, mnozenjem i potenciranjem

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
        č1 = self.član()
        sljedeće = self.granaj(Ar.KRAJ, Ar.PLUS, Ar.ZATVORENA)
        if sljedeće == Ar.PLUS:
            self.pročitaj(Ar.PLUS)
            č2 = self.izraz()
            return AST(stablo='zbroj', lijevo=č1, desno=č2)
        else:
            return č1

    def član(self):
        f1 = self.faktor()
        sljedeće = self.granaj(Ar.KRAJ, Ar.PUTA, Ar.PLUS, Ar.ZATVORENA)
        if sljedeće == Ar.PUTA:
            self.pročitaj(Ar.PUTA)
            f2 = self.član()
            return AST(stablo='umnožak', lijevo=f1, desno=f2)
        else:
            return f1

    def faktor(self):
        p1 = self.potencija()
        sljedeće = self.granaj(Ar.KRAJ, Ar.POT, Ar.PUTA, Ar.PLUS, Ar.ZATVORENA)
        if sljedeće == Ar.POT:
            self.pročitaj(Ar.POT)
            p2 = self.faktor()
            return AST(stablo='potencija', lijevo=p1, desno=p2)
        else:
            return p1

    def potencija(self):
        if self.granaj(Ar.BROJ, Ar.OTVORENA) == Ar.BROJ:
            return self.pročitaj(Ar.BROJ)
        else:
            self.pročitaj(Ar.OTVORENA)
            u_zagradi = self.izraz()
            self.pročitaj(Ar.ZATVORENA)
            return u_zagradi


def vrijednost(fragment):
    if isinstance(fragment, Token):
        return int(fragment.sadržaj)
    else:
        l = vrijednost(fragment.lijevo)
        d = vrijednost(fragment.desno)
        if fragment.stablo == 'zbroj': return l + d
        elif fragment.stablo == 'umnožak': return l * d
        elif fragment.stablo == 'potencija': return l ** d


def testiraj(izraz):
    mi = vrijednost(aritm_parse(izraz))
    python_izraz = izraz.replace('^', '**') #pythonu je ^ bitovni xor pa to prebacimo u **
    Python = eval(python_izraz)
    if mi == Python:
        print(izraz, '==', mi, 'OK')
    else:
        print(izraz, 'mi:', mi, 'Python:', Python)


def aritm_parse(niz_znakova):
    parser = AritmParser(aritm_lex(niz_znakova))
    rezultat = parser.izraz()
    parser.pročitaj(Ar.KRAJ)
    return rezultat

    
if __name__ == '__main__':
    print(*aritm_lex('1+43*(3+4^5)'), sep='\n')
    print (aritm_parse('1+43*(3+4^5)'))
    testiraj('1+43*(3+4^5)')
    testiraj('(2+3)^4+1')
    testiraj('(2*23+4)^(1+2)*(2+3)')
    testiraj('-2+3*4*(-2+3)^5+34')
    testiraj('2^3^4')
    

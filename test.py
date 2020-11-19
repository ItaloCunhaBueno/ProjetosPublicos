from spellchecker import SpellChecker

spell = SpellChecker('pt')  # loads default word frequency list
spell.word_frequency.load_text_file(r'C:\Users\Italo\Desktop\palavras.txt')

palavra = "Meu nome é Italo e eu tenho apitidao para screver python".split(" ")
misspelled = spell.unknown(palavra)

for word in misspelled:
    print("{0} =====> {1}".format(word, spell.correction(word)))

    print("Candidatos: {0}".format(spell.candidates(word)))
    print()
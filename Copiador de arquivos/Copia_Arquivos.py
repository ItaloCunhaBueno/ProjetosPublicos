from glob import glob
from shutil import copyfile
from os.path import basename, isdir, join
from os import walk
import fnmatch


PASTA_PA = r''
PASTA_SAIDA = r''
EXT = r'ods'


error = 0
if not isdir(PASTA_PA):
    error +=1
    print u"Campo 'ARQUIVOS' não é um caminho válido."
if not isdir(PASTA_SAIDA):
    error +=1
    print u"Campo 'SAÍDA' não é um caminho válido."
if EXT == None or EXT == "" or EXT == " ":
    error +=1
    print u"É necessario indicar uma extensão no campo 'EXTENSÃO'."
if error == 0:
    files = []
    for root, dirnames, filenames in walk(PASTA_PA):
        for filename in fnmatch.filter(filenames, '*.{0}'.format(EXT)):
            files.append(join(root, filename))
    
    print u"Iniciando cópia...\n"
    totalfiles = len(files)
    copiados = 0
    erros = 0
    for f in files:
        name = basename(f)
        dst = "{0}\\{1}".format(PASTA_SAIDA, name)
        try:
            copyfile(f, dst)
            copiados += 1
            print u"'{0}' copiado com sucesso.".format(f)
        except:
            erros += 1
            print u"não foi possivel copiar '{0}'\n".format(f)
    print u"\nPROCESSO CONCLUÍDO\n"
    print u"-----------------------------------------------------------------\n"
    print u"Total de arquivos processados: {0}".format(totalfiles)
    print u"Arquivos copiados: {0}".format(copiados)
    print u"Erros: {0}".format(erros)
    print u"\n"
from os.path import dirname, join
from os import walk
from tqdm import tqdm
from time import time

COMECO = time()
PASTA = r'\\10.0.0.21\maverick'

PATHS = []
FILES = [join(root, f) for root, dirs, files in walk(PASTA) for f in files if 'Ladybug_Panoramic' in root and f.endswith('.jpg')]
for F in tqdm(FILES, desc="ANALISANDO ARQUIVOS...", colour='green'):
    CAMINHO = dirname(F)
    if dirname(F) not in PATHS:
        PATHS.append(dirname(F))

for P in PATHS:
    print(P)

print("")
print("Quantidade de arquivos: {0}".format(len(FILES)))
print("TEMPO: {0}".format(time()-COMECO))
import csv
from os import listdir

IMAGENS = r"\\10.0.0.21\sao_vicente\LEV_MAVERICK_SV_31_01_21\sv31_01_01\Missions\M01\Images\Ladybug_CameraNo0"
CSV = r"C:\Users\Italo\Desktop\sv-faltantes.csv"
DADOS = csv.DictReader(open(CSV), delimiter=";")
DICTNAMES = {}
for x in DADOS:
    ORIG = x["origem"].replace("-", "_")
    if ORIG not in DICTNAMES:
        DICTNAMES[ORIG] = {}
    if x["camera_id"] not in DICTNAMES[ORIG]:
        DICTNAMES[ORIG][x["camera_id"]] = []
    if x["image_id"] not in DICTNAMES[ORIG][x["camera_id"]]:
        DICTNAMES[ORIG][x["camera_id"]].append([x["image_id"], x["event_id"]])

print([X for X in DICTNAMES])

ARQUIVOS = ["{0}\{1}".format(IMAGENS, FILE) for FILE in listdir(IMAGENS)]
for MISS in DICTNAMES["31_01_01"]["Ladybug_CameraNo0"]:
    IMGID = "{0}.jpg".format(MISS[0])
    EVNTID = "{0}.jpg".format(MISS[1])
    CAMINHOFOTO = ""
    for PATH in ARQUIVOS:
        if IMGID in PATH:
            CAMINHOFOTO = PATH
            break
    if CAMINHOFOTO:
        print(IMGID, CAMINHOFOTO)

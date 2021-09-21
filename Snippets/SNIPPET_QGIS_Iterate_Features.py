#
#   DEVE SER EXECUTADO DENTRO DO QGIS
#

from qgis.core import QgsProject

# NOME DO LAYER
LAYER = ""

# CRIA O OBJETO LAYER
LAYEROBJ = QgsProject.instance().mapLayersByName(LAYER)[0]

# INICIA A EDIÇÃO NO LAYER
LAYEROBJ.startEditing()

# ITERA AS FEICOES DENTRO DO LAYER
for L in LAYEROBJ.getFeatures():

    LAYEROBJ.updateFeature(L)
    pass

# FAZ O COMMIT DAS EDICOES NO LAYER
LAYEROBJ.commitChanges()

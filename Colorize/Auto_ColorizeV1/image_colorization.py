import numpy as np
import cv2 as cv
import PySimpleGUIQt as sg
import sys, os, io, errno, stat, shutil
from PIL import Image

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise

def resource_path(relative_path):

    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


prototext = resource_path("colorization_deploy_v2.prototxt")
caffemodel = resource_path("colorization_release_v2.caffemodel")
npyfile = resource_path("pts_in_hull.npy")


sg.ChangeLookAndFeel('Reddit')
sg.set_options(button_color=("0079d3", "0079d3"), button_element_size=(10, 1), text_justification="center")

col1 = [[sg.T("IMAGEM:", size=(44, 1)), sg.I(size=(0, 0), visible=False, key="img", enable_events=True), sg.FileBrowse("SELECIONAR", file_types=(("Imagem", "*.png; *.jpg; *.jpeg"),), target="img")],
        [sg.Image(filename=resource_path("placeholder.png"), key="img_display")]]
col2 = [[sg.T('RESULTADO:', size=(44, 1)), sg.I(size=(0, 0), visible=False, key="savefile", enable_events=True), sg.B("COLORIR", key="processar")],
        [sg.Image(filename=resource_path("placeholder.png"), key="img_display2", )]]

tab1_layout = [[sg.Column(col1), sg.Column(col2)],
               [sg.Exit(key="EXIT"), sg.FileSaveAs("SALVAR", file_types=(("Imagem", "*.jpg"),), target='savefile', key="savefilebrowse", disabled=True, button_color=("black","grey"))]]

tab2_layout = [[sg.T('PASTA:'), sg.I(key="pasta", size=(98,1)), sg.FolderBrowse()],
               [sg.B("COLORIR")],
               [sg.Exit(key="Exit")]]

layout = [[sg.T("\t\t\t\t\tCOLORIZADOR DE FOTOS EM PRETO E BRANCO", font=("Arial 12 bold"))],
          [sg.TabGroup([[sg.Tab('COLORIR ARQUIVO ÚNICO', tab1_layout), sg.Tab('COLORIR LOTE', tab2_layout)]])]]

window = sg.Window('Monografia do vértice genérica', layout, size=(1000, 700), auto_size_text=True, auto_size_buttons=False, resizable=False)

FileIMG = None

while True:
    event, values = window.read()
    if event is None or event == 'Exit' or event == 'EXIT':
        if os.path.isdir("./temp/"):
            shutil.rmtree("./temp/", ignore_errors=False, onerror=handleRemoveReadonly)
        break
    if event == 'img':
        if window['img'].Get():
            file = window['img'].Get()
            size = 530, 530
            im = Image.open(file)
            im.thumbnail(size, Image.ANTIALIAS)
            imgByteArr = io.BytesIO()
            im.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            window['img_display'].Update(data=imgByteArr)

    if event == "processar":
        if window['img'].Get():
            name = os.path.basename(window['img'].Get())[0:-4]
            ext = os.path.basename(window['img'].Get())[-3:]
            frame = cv.imread(window['img'].Get())
            numpy_file = np.load(npyfile)
            Caffe_net = cv.dnn.readNetFromCaffe(prototext, caffemodel)
            numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)
            Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [numpy_file.astype(np.float32)]
            Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

            input_width = 224
            input_height = 224
            rgb_img = (frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
            lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
            l_channel = lab_img[:,:,0]
            l_channel_resize = cv.resize(l_channel, (input_width, input_height))
            l_channel_resize -= 50

            Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
            ab_channel = Caffe_net.forward()[0,:,:,:].transpose((1,2,0))
            (original_height,original_width) = rgb_img.shape[:2]
            ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
            lab_output = np.concatenate((l_channel[:,:,np.newaxis],ab_channel_us),axis=2)
            bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)
            if not os.path.isdir("./temp/"):
                os.mkdir("./temp/")
            cv.imwrite("./temp/result.jpg", (bgr_output*255).astype(np.uint8))
            FileIMG = "./temp/result.jpg"
            size = 530, 530
            im2 = Image.open("./temp/result.{0}".format(ext))
            im2.thumbnail(size, Image.ANTIALIAS)
            imgByteArr = io.BytesIO()
            im2.save(imgByteArr, format='PNG')
            imgByteArr = imgByteArr.getvalue()
            window['img_display2'].Update(data=imgByteArr, visible=True)
            window['savefilebrowse'].Update(disabled=False, button_color=("0079d3", "0079d3"))
        else:
            sg.PopupOK("Selecione um arquivo antes.", keep_on_top=True, non_blocking=False)

    if event == "savefile":
        if window['savefile'].Get():
            if FileIMG:
                if os.path.isfile(FileIMG):
                    if not os.path.isfile(window['savefile'].Get()):
                        os.rename(FileIMG, window['savefile'].Get())
                        window['img_display2'].Update(filename=resource_path("placeholder.png"))
                        window['savefilebrowse'].Update(disabled=True, button_color=("black","grey"))
                        window.Refresh()
                    else:
                        os.remove(window['savefile'].Get())
                        os.rename(FileIMG, window['savefile'].Get())
                        window['img_display2'].Update(filename=resource_path("placeholder.png"))
                        window['savefilebrowse'].Update(disabled=True, button_color=("black","grey"))
                        window.Refresh()
                    sg.PopupOK("Arquivo salvo com sucesso.", keep_on_top=True, non_blocking=False)
                else:
                    sg.PopupOK("Processe um arquivo antes.", keep_on_top=True, non_blocking=False)
            else:
                sg.PopupOK("Processe um arquivo antes.", keep_on_top=True, non_blocking=False)

    if event == "COLORIR":
        if os.path.isdir(window['pasta'].Get()):
            Pasta = window['pasta'].Get()
            print("PROCESSANDO:")
            print("")
            print("="*50)
            window.Refresh()
            fnum = 0
            filenum = len(os.listdir(Pasta))
            for file in os.listdir(Pasta):
                if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(".PNG") or file.endswith(".Jpg") or file.endswith(".Png") or file.endswith(".jpeg") or file.endswith(".JPEG") or file.endswith(".Jpeg"):
                    filepath = os.path.join(Pasta, file)
                    name = file[0:-4]
                    ext = os.path.basename(window['img'].Get())[-3:]
                    frame = cv.imread(filepath)
                    numpy_file = np.load(npyfile)
                    Caffe_net = cv.dnn.readNetFromCaffe(prototext, caffemodel)
                    numpy_file = numpy_file.transpose().reshape(2, 313, 1, 1)
                    Caffe_net.getLayer(Caffe_net.getLayerId('class8_ab')).blobs = [numpy_file.astype(np.float32)]
                    Caffe_net.getLayer(Caffe_net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

                    input_width = 224
                    input_height = 224
                    rgb_img = (frame[:,:,[2, 1, 0]] * 1.0 / 255).astype(np.float32)
                    lab_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2Lab)
                    l_channel = lab_img[:,:,0]
                    l_channel_resize = cv.resize(l_channel, (input_width, input_height))
                    l_channel_resize -= 50

                    Caffe_net.setInput(cv.dnn.blobFromImage(l_channel_resize))
                    ab_channel = Caffe_net.forward()[0,:,:,:].transpose((1,2,0))
                    (original_height,original_width) = rgb_img.shape[:2]
                    ab_channel_us = cv.resize(ab_channel, (original_width, original_height))
                    lab_output = np.concatenate((l_channel[:,:,np.newaxis],ab_channel_us),axis=2)
                    bgr_output = np.clip(cv.cvtColor(lab_output, cv.COLOR_Lab2BGR), 0, 1)
                    cv.imwrite("{0}/Result_{1}.jpg".format(Pasta, name), (bgr_output*255).astype(np.uint8))
                    fnum += 1
                    print("CONCLUÍDO: {0}".format(filepath))
                    window.Refresh()
            print("=" * 50)
            print("")
            print("PROCESSO CONCLUÍDO")
            print("")
            print("Arquivos na pasta: {0}".format(filenum))
            print("Arquivos processados: {0}".format(fnum))
            window.Refresh()
        else:
            sg.PopupOK("Selecione uma pasta antes.", keep_on_top=True, non_blocking=False)
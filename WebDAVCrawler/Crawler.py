import requests as rq
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from os.path import join, isdir
from os import mkdir

# =====================================================PARAMETERS=====================================================
INPUTLINK = r""
OUTPUTFOLDER = r""

# =======================================================SCRIPT=======================================================

# FUNCTION TO DEFINE IF ADDRESS IS FOLDER OF FILE
def isDirectory(url):

    try:
        NAME = url.split("/")[-1]
        if NAME == "" or NAME.startswith(".") or not "." in NAME:
            return True
        else:
            return False
    except AttributeError:
        return False


# FUNCTION TO ITERATE EVERY LINK IN A PAGE AND DOWNLOAD IT AS A FILE
def file_download(URLlink, folder):

    """
    link: url to the webdav page with all the links to the files
    folder: folder where the files will be saved
    """

    # CREATE THE OUTPUT FOLDER IF DOES NOT EXIST
    if not isdir(folder):
        mkdir(folder)

    # CREATE THE REQUESTS SESSION
    SESSION = rq.Session()

    # GET THE PAGE
    REQ = SESSION.get(URLlink)

    # PARSE THE PAGE
    SOUP = bs(REQ.content, "html.parser")

    # NAME OF CURRENT FOLDER
    FOLDERNAME = URLlink.split("/")[-1]

    # ITERATE OVER THE FILE LINKS
    for link in tqdm(SOUP.find_all("a"), desc=f"Downloading {FOLDERNAME}...", leave=False, dynamic_ncols=True):

        # GET THE FILE LINK
        URL = link.get("href")

        # PROCEED IF THE RESULT IS A VALID LINK
        if URL:
            if URL.startswith("http"):

                # CHECK IF ITS FOLDER
                if isDirectory(URL):
                    file_download(URL, join(folder, URL.split("/")[-1]))

                else:

                    # DEFINE OUTPUT FILE NAME
                    OUTFILE = join(folder, URL.split("/")[-1])

                    # GRAB THE FILE
                    FILEREQ = SESSION.get(URL, stream=True)

                    # WRITE THE FILE TO DISK
                    with open(OUTFILE, "wb") as f:
                        for CHUNK in FILEREQ.iter_content(chunk_size=1024):
                            if CHUNK:
                                f.write(CHUNK)


# EXECUTE THE SCRIPT
if __name__ == "__main__":
    print("Starting...")
    file_download(INPUTLINK, OUTPUTFOLDER)
    print("Done!")

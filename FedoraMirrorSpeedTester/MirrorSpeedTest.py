#
#   SCRIPT FOR TESTING THE DOWNLOAD SPEED OF FEDORA'S MIRRORS SO YOU CAN CHOOSE THE BEST ONE
#

# ======================================== IMPORTS ==========================================

import dnf
import xmltodict
import requests
from pathlib import Path
import time
from os import remove
import concurrent.futures
import enlighten

# ======================================== SETTINGS =========================================

# NAME (WITH EXTENSION) OF THE PACKAGE TO BE DOWNLOADED SEVERAL TIMES, CHOOSE ONE NOT TOO BIG AND NOT TOO SMALL
PACKAGE = "kernel-doc-5.14.10-300.fc35.noarch.rpm"

# DOWNLOAD TIME BEFORE THE PROGRAM SKIPS TO NEXT MIRROR
TIMEOUT = 10

# NUMBER OF CONCURRENT DOWNLOADS
CONCURRENT = 5

# SAVE LOCATION FOR THE PACKAGES AND 'Results.txt', LEAVE BLANK FOR DOWNLOADS FOLDER (DEFAULT)
SAVE_LOCATION = ''

# ======================================= FUNCTIONS =========================================


# GET THE METALINK FILE FOR THE FEDORA RELEASE AND ARCHITECTURE AND PARSE IT TO OBTAIN
# EVERY MIRROR LINK, RETURNS A LIST OF MIRRORS
def GetURLs(package):
    """
    This function gets the URLs of the Fedora mirrors from the Fedora metalink.
    """
    print("Getting the URLs of the Fedora mirrors...")

    # DEFINE THE RELEASE VERSION AND BASE ARCHITECTURE
    db = dnf.dnf.Base()
    VER_ARCH = db.conf.substitutions

    # METALINK WITH THE LIST OF MIRRORS
    METALINK = f"https://mirrors.fedoraproject.org/metalink?repo=fedora-{VER_ARCH['releasever']}&arch={VER_ARCH['basearch']}"

    # KEEP URL OF THE MIRRORS AS A LIST
    URLS = []

    # PARSE THE METALINK AND GET THE URLS OF THE MIRRORS
    XML = xmltodict.parse(requests.get(METALINK).text)
    for LINK in XML["metalink"]["files"]["file"]["resources"]["url"]:
        URL = LINK["#text"]

        # GET ONLY LINKS THAT START WITH "http" OR "https" AND MAKE THE PACKAGE LINK OUT OF IT
        if URL.startswith("http"):
            PART1 = URL.replace("repodata/repomd.xml", "")
            PART2 = f"{PART1}/Packages/{package[0]}/{package}"
            URLS.append(PART2)

    # RETURNS THE LIST OF MIRRORS
    return URLS


# DOES THE DOWNLOAD OF THE PACKAGE PRESENTING A NICE PROGRESS BAR AND RETURNS THE SPEED AND URL
def Download(url, package, timeout, count, total, manager, save_location):
    """
    This function downloads the package from the given URL and save it to the Downloads folder.

    url: The URL of the mirror.
    package: Name of the package to be downloaded.
    timeout: Timeout (in seconds) for the download.
    count: ID of the URL in the list of URLs.
    total: Total number of URLs in the list.
    manager: Manager class of the enlighten lib used to create the progress bar.

    """

    # DEFINE SAVE PATH TO THE DOWNLOADED PACKAGE
    if save_location == '':
        SAVE_PATH = Path(Path().home(), "Downloads", package)
    else:
        SAVE_PATH = Path(save_location, package)

    # HOLDS THE DOWNLOAD SPEED VARIABLE
    SPEED = 0

    # SAVES THE PACKAGE
    with open(SAVE_PATH, "wb") as F:

        # TRY TO DOWNLOAD THE PACKAGE, IF IT FAILS, SKIP TO THE NEXT MIRROR
        try:

            # START TIME SO WE CAN CALCULATE THE DOWNLOAD SPEED
            START = time.perf_counter()

            # REQUEST THE PACKAGE IN STREAM MODE AND GET THE TOTAL SIZE OF PACKAGE
            RESPONSE = requests.get(url, stream=True, timeout=timeout)
            TOTAL_LENGTH = RESPONSE.headers.get("content-length")

            # IF THE RESPONSE DOES NOT CONTAIN THE CONTENT-LENGTH HEADER, PRINTS A MESSAGE AND SKIP TO THE NEXT MIRROR
            if TOTAL_LENGTH is None:
                print(
                    "WARNING: The response does not contain the content-length header, skipping to the next mirror...")

            # ELSE PRESENT THE PROGRESS BAR
            else:

                # CONVERT THE SIZE TO INTEGER
                TOTAL_LENGTH = int(TOTAL_LENGTH)

                # IF THE PACKAGE IS BIGGER THAN 1024 BYTES AND SMALLER THAN 1048576 BYTES, PRESENT THE SIZE IN KB
                if TOTAL_LENGTH >= 1024 and TOTAL_LENGTH < 1048576:
                    UNIDADE = "KiB"
                    FACTOR = 1024
                    TOTALN = round(TOTAL_LENGTH / FACTOR, 2)

                # IF THE PACKAGE IS BIGGER THAN 1048576 BYTES AND SMALLER THAN 1073741824 BYTES, PRESENT THE SIZE IN MB
                elif TOTAL_LENGTH >= 1048576 and TOTAL_LENGTH < 1073741824:
                    UNIDADE = "MiB"
                    FACTOR = 1048576
                    TOTALN = round(TOTAL_LENGTH / FACTOR, 2)

                # IF THE PACKAGE IS BIGGER THAN 1073741824 BYTES, PRESENT THE SIZE IN GB
                elif TOTAL_LENGTH >= 1073741824:
                    UNIDADE = "GiB"
                    FACTOR = 1073741824
                    TOTALN = round(TOTAL_LENGTH / FACTOR, 2)

                # FORMAT THE PROGRESS BAR IN THE FOLLOWING MANER:
                # Description: 100%|=========================| XX.XX KB/ YY.YY KB @ ZZ.ZZ KB/s
                BAR_FORMAT = "{desc}{desc_pad}{percentage:3.0f}%|{bar}|{desc_pad}{count:.2f} {unit}/{total} {unit} @ {rate:.2f}{unit}/s"

                # CREATE A PROGRESS BAR
                PROGRESSBAR = manager.counter(
                    total=TOTALN, desc=f"({count}/{total})", unit=UNIDADE, leave=False, bar_format=BAR_FORMAT)

                # HOLDS HOW MANY BYTES WE HAVE DOWNLOADED
                DL = 0

                # ITERATE THE CHUNKS OF THE RESPONSE, SAVE IT, UPDATE THE PROGRESS BAR AND CALCULATE THE SPEED
                for data in RESPONSE.iter_content(chunk_size=4096):

                    # IF THE DOWNLOAD TIME EXCEEDS THE TIMEOUT, PRINT A MESSAGE AND SKIP TO THE NEXT MIRROR
                    if (time.perf_counter() - START) > timeout + 1:
                        print("INFO: Timeout reached, skipping to next mirror.")
                        break

                    # SUM THE BYTES DOWNLOADED
                    DL += len(data)

                    # WRITE DATA TO DISK
                    F.write(data)

                    # UPDATE THE PROGRESS BAR
                    PROGRESSBAR.update(len(data) / FACTOR)

                    # UPDATE THE DOWNLOAD SPEED
                    SPEED = int((DL // (time.perf_counter() - START)) / 1024)

                # ENDS THE PROGRESS BAR WHEN FINISHED
                PROGRESSBAR.close()

        # CATCH CONNECTION TIMEOUT EXCEPTIONS, PRINT A MESSAGE AND SKIP TO NEXT MIRROR
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            print("INFO: Timeout reached, skipping to next mirror.")

    # RETURNS THE DOWNLOAD SPEED AND THE URL
    return (SPEED, url)


# PRINTS A BUNCH O MESSAGES TO THE USER
def PrintMessages(package, timeout, concurrent):
    """
    This function prints the messages to the user.

    package: Name of the package to be downloaded.
    timeout: Timeout (in seconds) for the download.
    concurrent: Number of concurrent downloads.

    """

    # PRINT THE MESSAGE TO THE USER
    MESSAGE = """
    ################################################################################
    #
    # FEDORA MIRROR TESTER
    # This program will download a package from the Fedora mirrors, test
    # the download speed and save a TestResults.txt to the Downloads folder.
    # 
    ################################################################################
    """
    print(MESSAGE)
    print("")
    print("SETTINGS:")
    print(f"Package: {package}")
    print(f"Timeout: {timeout}")
    print(f"Concurrent: {concurrent}")
    print("")


# INITIATE THE PROCESS AND RETURN THE RESULTS
def Process(package, links, timeout, nconcurrent, save_location):
    """
    This function initiates the process and returns the results.
    """

    # PRINT MESSAGE
    print(f"Downloading {package}...")

    # HOLDS THE RESULTS
    RESULTS = {}

    # INITIALIZE THE PROGRESS BARS MANAGER
    with enlighten.get_manager(no_resize=True) as MANAGER:

        # DRAW A HEADER TO THE PROGRESS BARS SECTION
        MANAGER.status_bar(status_format="{fill}Testing Mirrors...{fill}{elapsed}",
                           color="bold_underline_bright_white_on_lightslategray", justify=enlighten.Justify.CENTER, autorefresh=True, min_delta=0.5)

        # DOES THE CONCURRENCY
        with concurrent.futures.ThreadPoolExecutor(max_workers=nconcurrent) as executor:

            # HOLDS THE PROCESSES
            futures = []

            # ITERATE THE LINKS AND START THE PROCESS IN EACH LINK
            for ID, LINK in enumerate(links, start=1):
                futures.append(executor.submit(
                    Download, LINK, package, timeout, ID, len(links), MANAGER, save_location))

    # ITERATE THE FINISHED PROCESSES AND RETURN THE RESULTS
    for future in concurrent.futures.as_completed(futures):

        # HOLDS THE RESULT
        SP = future.result()

        # APPEND THE RESULT TO THE RESULTS DICTIONARY USING THE DOWNLOAD SPEED AS KEY SO WE CAN SORT IT LATTER
        if SP[0] not in RESULTS:
            RESULTS[SP[0]] = [SP[1]]

        # IF THE DOWNLOAD SPPED IS ALREADY IN THE DICTIONARY, APPEND THE URL TO THE LIST
        else:
            RESULTS[SP[0]].append(SP[1])

    # RETURN THE RESULTS
    print("")
    return RESULTS


# SAVE THE RESULTS FILE AND PRINT IT TO THE USER
def SaveResults(results, package, save_location):
    """
    This function saves the results file and prints it to the user.
    """

    # PATH TO THE TEST RESULTS FILE
    if save_location == "":
        RESULTS_PATH = Path(Path().home(), "Downloads", "Results.txt")
    else:
        RESULTS_PATH = Path(save_location, "Results.txt")

    # PRINT MESSAGE
    print(f"Saving results to {RESULTS_PATH}...")

    # CREATE THE TEST RESULTS FILE
    with open(RESULTS_PATH, "w+") as r:

        # WRITE THE HEADER
        r.write(f"{package} download speed test results (from Best to Worst):\n")
        r.write("\n")

        # ITERATE THE RESULTS AND WRITE THE DOWNLOAD SPEED AND THE URL
        for DLDSPEED in sorted(results.keys(), reverse=True):
            for URI in results[DLDSPEED]:
                r.write(
                    f"{DLDSPEED} Kbps: {URI.replace(f'/Packages/{package[0]}/{package}', '')}\n")

    # ITERATE THE RESULTS AND PRINT IT TO THE USER
    print("RESULTS:")
    for DLSPEED in sorted(results.keys()):
        for URLFINAL in results[DLSPEED]:
            print(
                f"{DLSPEED} Kbps: {URLFINAL.replace(f'/Packages/{package[0]}/{package}', '')}")


# MAIN FUNCTION
def main(package, timeout, concurrent, save_location):

    # PRINT FIRST MESSAGES TO THE USER
    PrintMessages(package, timeout, concurrent)

    # GET THE PACKAGE URL FOR EACH MIRROR
    LINKS = GetURLs(package)

    # PROCESS THE LINKS AND RETURN THE RESULTS
    FINALRESULTS = Process(package, LINKS, timeout, concurrent, save_location)

    # SAVE THE RESULTS FILE
    SaveResults(FINALRESULTS, package, save_location)

    # DELETE THE DOWNLOADED PACKAGE IF IT EXISTS
    if save_location == "":
        FILE = Path(Path().home(), "Downloads", package)
    else:
        FILE = Path(save_location, package)

    if FILE.exists():
        remove(FILE)

    # PRINT THE END MESSAGE TO THE USER
    print("")
    print("################################################################################")


# ======================================= MAIN =========================================
if "__main__" == __name__:
    main(PACKAGE, TIMEOUT, CONCURRENT, SAVE_LOCATION)

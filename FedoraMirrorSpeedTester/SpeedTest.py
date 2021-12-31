#
#   SCRIPT FOR TESTING THE DOWNLOAD SPEED OF FEDORA'S MIRRORS SO YOU CAN CHOOSE THE BEST ONE
#

import dnf
import xmltodict
import requests
from pathlib import Path
import time
from os import remove
import concurrent.futures
import enlighten

# NAME (WITH EXTENSION) OF THE PACKAGE TO BE DOWNLOADED SEVERAL TIMES, CHOOSE ONE NOT TOO BIG AND NOT TOO SMALL
PACKAGE = "kernel-doc-5.14.10-300.fc35.noarch.rpm"

# DOWNLOAD TIME BEFORE THE PROGRAM SKIPS TO NEXT MIRROR
TIMEOUT = 10

# NUMBER OF CONCURRENT DOWNLOADS
CONCURRENT = 20


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
        if URL.startswith("http"):
            PART1 = URL.replace("repodata/repomd.xml", "")
            PART2 = f"{PART1}/Packages/{package[0]}/{package}"
            URLS.append(PART2)

    # RETURNS THE LIST OF MIRRORS
    return URLS


def Download(url, package, timeout, count, total, manager):
    """
    This function downloads the package from the given URL and save it to the Downloads folder.
    """

    # DEFINE SAVE PATH TO THE DOWNLOADED PACKAGE
    SAVE_PATH = Path(Path().home(), "Downloads", package)
    SPEED = 0

    # SAVES THE PACKAGE
    with open(SAVE_PATH, "wb") as F:
        try:
            START = time.perf_counter()

            # REQUEST THE PACKAGE IN STREAM MODE
            RESPONSE = requests.get(url, stream=True, timeout=timeout)
            TOTAL_LENGTH = RESPONSE.headers.get("content-length")

            # IF THE RESPONSE DOES NOT CONTAIN THE CONTENT-LENGTH HEADER, DOWNLOAD ANYWAY
            if TOTAL_LENGTH is None:
                F.write(RESPONSE.content)

            # ELSE PRESENT THE PROGRESS BAR
            else:

                TOTAL_LENGTH = int(TOTAL_LENGTH)

                if TOTAL_LENGTH >= 1024 and TOTAL_LENGTH < 1048576:
                    UNIDADE = "KiB"
                    FACTOR = 1024
                    TOTALN = round(TOTAL_LENGTH / FACTOR, 2)

                elif TOTAL_LENGTH >= 1048576 and TOTAL_LENGTH < 1073741824:
                    UNIDADE = "MiB"
                    FACTOR = 1048576
                    TOTALN = round(TOTAL_LENGTH / FACTOR, 2)

                elif TOTAL_LENGTH >= 1073741824:
                    UNIDADE = "GiB"
                    FACTOR = 1073741824
                    TOTALN = round(TOTAL_LENGTH / FACTOR, 2)

                BAR_FORMAT = "{desc}{desc_pad}{percentage:3.0f}%|{bar}|{desc_pad}{count:.2f} {unit}/{total} {unit} @ {rate:.2f}{unit}/s"
                PROGRESSBAR = manager.counter(
                    total=TOTALN,
                    desc=f"({count}/{total})",
                    unit=UNIDADE,
                    leave=False,
                    bar_format=BAR_FORMAT,
                )

                DL = 0
                for data in RESPONSE.iter_content(chunk_size=4096):
                    if (time.perf_counter() - START) > timeout + 1:
                        print("INFO: Timeout reached, skipping to next mirror.")
                        break
                    DL += len(data)
                    F.write(data)
                    PROGRESSBAR.update(len(data) / FACTOR)
                    SPEED = int((DL // (time.perf_counter() - START)) / 1024)
                PROGRESSBAR.close()
        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ChunkedEncodingError,
        ) as e:
            print("INFO: Timeout reached, skipping to next mirror.")
    return (SPEED, url)


if "__main__" == __name__:
    MESSAGE = """################################################################################
#
# FEDORA MIRROR TESTER
# This program will download a package from the Fedora mirrors, test
# the download speed and save a TestResults.txt to the Downloads folder.
# 
################################################################################"""
    print(MESSAGE)
    print("")
    print("SETTINGS:")
    print(f"Package: {PACKAGE}")
    print(f"Timeout: {TIMEOUT}")
    print(f"Concurrent: {CONCURRENT}")
    print("")

    LINKS = GetURLs(PACKAGE)

    print(f"Downloading {PACKAGE}...")

    RESULTS = {}
    with enlighten.get_manager(no_resize=True) as MANAGER:
        MANAGER.status_bar(
            status_format="{fill}Testing Mirrors...{fill}{elapsed}",
            color="bold_underline_bright_white_on_lightslategray",
            justify=enlighten.Justify.CENTER,
            autorefresh=True,
            min_delta=0.5,
        )
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT) as executor:
            futures = []
            for ID, LINK in enumerate(LINKS, start=1):
                futures.append(
                    executor.submit(
                        Download, LINK, PACKAGE, TIMEOUT, ID, len(LINKS), MANAGER
                    )
                )
    for future in concurrent.futures.as_completed(futures):
        SP = future.result()
        if SP[0] not in RESULTS:
            RESULTS[SP[0]] = [SP[1]]
        else:
            RESULTS[SP[0]].append(SP[1])

    print("")

    RESULTS_PATH = Path(Path().home(), "Downloads", "TestResults.txt")

    print(f"Saving results to {RESULTS_PATH}...")

    with open(RESULTS_PATH, "w+") as r:
        r.write(f"{PACKAGE} download speed test results (from Best to Worst):\n")
        r.write("\n")
        for DLDSPEED in sorted(RESULTS.keys(), reverse=True):
            for URI in RESULTS[DLDSPEED]:
                r.write(
                    f"{DLDSPEED} Kbps: {URI.replace(f'/Packages/{PACKAGE[0]}/{PACKAGE}', '')}\n"
                )

    print("RESULTS:")

    for DLSPEED in sorted(RESULTS.keys()):
        for URLFINAL in RESULTS[DLSPEED]:
            print(
                f"{DLSPEED} Kbps: {URLFINAL.replace(f'/Packages/{PACKAGE[0]}/{PACKAGE}', '')}"
            )

    FILE = Path(Path().home(), "Downloads", PACKAGE)
    if FILE.exists():
        remove(FILE)

    print("")
    print(
        "################################################################################"
    )

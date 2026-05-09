import os
import zipfile
import requests
import ffmpeg
from requests.exceptions import HTTPError
from tqdm import tqdm
from natsort import natsorted
import xml.etree.ElementTree as ET


def create_session(username, password, lms) -> requests.session:

    s = requests.session()
    url = f"https://lms{lms}.sku.ac.ir/system/login?domain=lms{lms}.sku.ac.ir&next=/admin?domain=lms{lms}.sku.ac.ir&set-lang=en"

    data = {
        "login": username,
        "password": password,
        "feature=fGhJT-PGEiFYwFBGg3k43A__": "Login",
    }
    try:
        r = s.post(url, data, timeout=20)
        r.raise_for_status()
        if "Invalid credentials." in r.text:
            print("[-] Failed: Invalid credentials")
            is_login = False
        else:
            is_login = True
            print("[+] Success: Authentication completed")
    except HTTPError as e:
        print(f"[-] Failed: Request failed => {e}")

    return s, is_login


def download_class_files(s, url, filename):

    run = True
    if os.path.exists(filename):
        answ = input("[!] Warning: Already exists. Do you want to rewrite it ? ([Y/n])")
        if answ.lower() in ["n", "no"]:
            run = False

    if run:
        try:
            r = s.get(url, stream=True)
            r.raise_for_status()

            file_size = int(r.headers.get("content-length"))

            with open("class.zip", "wb") as file:
                with tqdm(
                    total=file_size, unit="B", unit_scale=True, desc="Downloading"
                ) as pbar:
                    for data in r.iter_content(chunk_size=1024):
                        file.write(data)
                        pbar.update(len(data))
            print("[+] Success: ZIP file downloaded successfully")

            # Extract ZIP
            os.makedirs(filename, exist_ok=True)
            os.makedirs(f"{filename}/videos", exist_ok=True)
            os.makedirs(f"{filename}/chats", exist_ok=True)
            os.makedirs(f"{filename}/xml", exist_ok=True)

            is_chat_exist = False

            with zipfile.ZipFile("class.zip", "r") as zipf:
                for file in zipf.infolist():
                    if ".flv" in file.filename:
                        zipf.extract(file.filename, f"./{filename}/videos")
                    elif "sco_metadata" in file.filename:
                        zipf.extract(file.filename, f"./{filename}/chats")
                        is_chat_exist = True
                    else:
                        zipf.extract(file.filename, f"./{filename}/xml")

            print("[+] Success: ZIP file extracted successfully")

            os.remove("class.zip")

        except HTTPError as e:
            print(f"[-] Failed: Download request failed => {e}")

        # main path
        path = os.getcwd()
        if is_chat_exist:
            extract_chat(filename)

        os.chdir(path)
        convert(filename)


def extract_chat(filename):

    os.chdir(f"{filename}/chats")
    tree = ET.parse("sco_metadata.xml")
    root = tree.getroot()

    content_texts = []
    for content in root.iter("content"):
        if content.text:
            content_texts.append(content.text.strip())
    with open("chats.txt", "w") as c:
        for message in content_texts:
            if not ("sendMessage6" in message):
                c.write(f"- {message}\n")

    if os.path.exists("sco_metadata.xml"):
        os.remove("sco_metadata.xml")


def convert(dir_name):

    os.chdir(f"{dir_name}/videos")
    vid_list = natsorted(os.listdir())
    share_list = []

    # check if screen share exist
    share_is_exist = False

    with open("vidlist.txt", "w") as l:
        for vid in vid_list:

            if "screenshare" in vid:
                share_is_exist = True
                share_list.append(vid)
                continue

            if (".flv" in vid) and has_content(vid):
                l.write(f"file '{vid}'\n")

    if share_is_exist:
        with open("screenlist.txt", "w") as l:
            for share in natsorted(share_list):
                if (".flv" in share) and has_content(share):
                    l.write(f"file '{share}'\n")

    # ffmpeg convert
    run = True

    if run:
        try:
            ffmpeg.input("vidlist.txt", f="concat", safe="0").output(
                f"{dir_name}.flv",
                vcodec="copy",
                af="aresample=async=1",
                acodec="aac",
                audio_bitrate="192k",
            ).run(overwrite_output=True)
        except Exception as e:
            print(f"[-] Failed: Couldn't convert the file => {e}")

        if share_is_exist:
            try:
                ffmpeg.input("screenlist.txt", f="concat", safe="0").output(
                    f"{dir_name}_screen.flv",
                    vcodec="copy",
                    af="aresample=async=1",
                    acodec="aac",
                    audio_bitrate="192k",
                ).run(overwrite_output=True)
            except Exception as e:
                print(f"[-] Failed: Couldn't convert the file => {e}")

        for vid in vid_list:
            os.remove(vid)

    if os.path.exists("vidlist.txt"):
        os.remove("vidlist.txt")

    if os.path.exists("screenlist.txt"):
        os.remove("screenlist.txt")


def has_content(filepath):

    try:
        size_bytes = os.path.getsize(filepath)

        # 100KB
        if size_bytes < 100 * 1024:
            return False

        probe = ffmpeg.probe(filepath)
        duration = float(probe["format"]["duration"])

        bitrate = (size_bytes * 8) / duration if duration > 0 else 0

        if bitrate < 10000:
            return False

        return True
    except:
        return False


def main(url=None, st_id=None, nat_id=None):
    if url is None:
        download_url = input(
            "Enter URL (EXAMPLE = https://lms1.sku.ac.ir/xxxxxxxxxxxx): "
        ).rstrip("/")
    else:
        download_url = url.rstrip("/")

    download_url = download_url + "/output/class.zip?download=zip"
    class_code = download_url[23:35]

    if st_id is None:
        username = "k" + input("Enter ID (EXAMPLE = 4041406xxx): ")
    else:
        username = "k" + st_id

    if nat_id is None:
        national_id = int(input("Enter National-ID: "))
    else:
        national_id = int(nat_id)

    print("***********************************************************")

    lms_server = 1
    if "lms2" in download_url:
        lms_server = 2

    user_session, is_login = create_session(username, national_id, lms_server)

    if is_login:
        download_class_files(user_session, download_url, class_code)
    else:
        print("[-] Failed: Please login to your account")


if __name__ == "__main__":
    main()

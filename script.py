import os
import zipfile
import requests
import ffmpeg
from requests.exceptions import HTTPError
from tqdm import tqdm


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
            os.makedirs(f"{filename}/xml", exist_ok=True)

            with zipfile.ZipFile("class.zip", "r") as zipf:
                for file in zipf.infolist():
                    if ".flv" in file.filename:
                        zipf.extract(file.filename, f"./{filename}/videos")
                    else:
                        zipf.extract(file.filename, f"./{filename}/xml")

            print("[+] Success: ZIP file extracted successfully")

            os.remove("class.zip")

        except HTTPError as e:
            print(f"[-] Failed: Download request failed => {e}")

        convert(filename)


def convert(dir_name):

    os.chdir(f"{dir_name}/videos")
    vid_list = sorted(os.listdir())
    with open("vidlist.txt", "w") as l:
        for vid in vid_list:
            if ".flv" in vid:
                l.write(f"file '{vid}'\n")

    # ffmpeg convert
    run = True

    if os.path.exists(f"{dir_name}.flv"):
        answ = input("[!] Warning: Already exists. Do you want to rewrite it ? ([Y/n])")
        if answ.lower() in ["n", "no"]:
            run = False

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

        for vid in vid_list:
            os.remove(vid)

    if os.path.exists("vidlist.txt"):
        os.remove("vidlist.txt")


def main():
    download_url = (
        input("Enter URL (EXAMPLE = https://lms1.sku.ac.ir/xxxxxxxxxxxx): ").rstrip("/")
        + "/output/class.zip?download=zip"
    )

    # dir name
    class_code = download_url[23:35]

    username = "k" + input("Enter ID (EXAMPLE = 4041406xxx): ")
    national_id = int(input("Enter National-ID: "))
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

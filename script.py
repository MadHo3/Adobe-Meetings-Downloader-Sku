import os
import zipfile
import requests
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
            isLogin = False
        else:
            isLogin = True
            print("[+] Success: Authentication completed")
    except HTTPError as e:
        print(f"[-] Failed: Request failed => {e}")

    return s, isLogin


def download_class_files(s, url):
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
        class_code = url[23:35]
        os.makedirs(class_code)

        with zipfile.ZipFile("class.zip", "r") as zipf:
            zipf.extractall(f"./{class_code}")

        print("[+] Success: ZIP file extracted successfully")

        os.remove("class.zip")

    except HTTPError as e:
        print(f"[-] Failed: Download request failed => {e}")


def main():
    download_url = (
        input("Enter URL (EXAMPLE = https://lms1.sku.ac.ir/xxxxxxxxxxxx): ").rstrip("/")
        + "/output/class.zip?download=zip"
    )
    username = "k" + input("Enter ID (EXAMPLE = 4041406xxx): ")
    national_id = int(input("Enter National-ID : "))
    print("***********************************************************")

    lms_server = 1
    if "lms2" in download_url:
        lms_server = 2

    user_session, isLogin = create_session(username, national_id, lms_server)

    if isLogin:
        download_class_files(user_session, download_url)
    else:
        print("[-] Failed: Please login to your account")


if __name__ == "__main__":
    main()

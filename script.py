import os
import zipfile
import requests
from requests.exceptions import HTTPError


def creat_session(username, password, lms) -> requests.session:

    s = requests.session()
    url = f"https://lms{lms}.sku.ac.ir/system/login?domain=lms{lms}.sku.ac.ir&next=/admin?domain=lms{lms}.sku.ac.ir&set-lang=en"

    data = {"login": username, "password": password}
    try:
        r = s.post(url, data, timeout=20)
        r.raise_for_status()
        if "Invalid credentials." in r.text:
            print("Login Failed")
        else:
            print("Login Successful")
    except HTTPError as e:
        print(f"Request failed => {e}")

    return s


def download_class_files(s, url):
    try:
        r = s.get(url, stream=True)
        r.raise_for_status()
        with open("class.zip", "wb") as file:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print("**************************************")
        print("ZIP file downloaded successfully")

        # Extract ZIP
        with zipfile.ZipFile("class.zip", "r") as zipf:
            zipf.extractall(".")

        os.remove("class.zip")

    except HTTPError as e:
        print(f"download failed => {e}")


def main():
    download_url = (
        input("Enter URL (EXAMPLE = https://lms1.sku.ac.ir/xxxxxxxxxxxx): ").rstrip("/")
        + "/output/class.zip?download=zip"
    )
    username = "k" + input("Enter ID (EXAMPLE = 4041406xxx): ")
    national_id = int(input("Enter National-ID : "))

    lms_server = 1
    if "lms2" in download_url:
        lms_server = 2

    user_session = creat_session(username, national_id, lms_server)

    download_class_files(user_session, download_url)


if __name__ == "__main__":
    main()

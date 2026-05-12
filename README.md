# Adobe Meetings Downloader SKU

---

## فارسی

### درباره پروژه
این ابزار برای دانلود و تبدیل خودکار جلسات ضبط‌ شده **Adobe Connect** از سامانهٔ آموزش مجازی دانشگاه شهرکرد (SKU) طراحی شده است.  
با وارد کردن لینک کلاس، شماره دانشجویی و کد ملی، اسکریپت وارد حساب کاربری شما می‌شود، فایل ZIP کلاس را دانلود کرده، ویدیوهای FLV را استخراج و به ترتیب صحیح به هم می‌چسباند، همچنین گفتگوی متنی کلاس (چت) را جدا کرده و در فایل متنی ذخیره می‌کند.  
اگر در جلسه اشتراک‌گذاری صفحه وجود داشته باشد، آن را نیز به صورت جداگانه پردازش می‌کند.  
به دلیل محدودیت‌های ذاتی **Adobe Connect** ممکن است در برخی موارد ترکیب کامل جلسه ممکن نباشد.

### پیش‌نیازها
- **Python 3.6** یا بالاتر
- **pip**
- **ffmpeg**

### نصب و راه‌اندازی

#### لینوکس
```bash
# Debian / Ubuntu
sudo apt update && sudo apt install ffmpeg -y
git clone https://github.com/MadHo3/Adobe-Meetings-Downloader-Sku.git
cd Adobe-Meetings-Downloader-Sku
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 script.py
# GUI version
python3 gui.py

# Arch
sudo pacman -S ffmpeg
git clone https://github.com/MadHo3/Adobe-Meetings-Downloader-Sku.git
cd Adobe-Meetings-Downloader-Sku
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 script.py
# GUI version
python3 gui.py
```
#### ویندوز

فایل zip را استخراج کنید => [Download](https://scorpian.ir/proxy/asset/MadHo3/Adobe-Meetings-Downloader-Sku/418623577)

فایل install.bat را اجرا کنید سپس فایل AdobeDownloaderSku.exe را اجرا کنید.


#### نکات :

کد ملی به عنوان رمز عبور استفاده می‌شود.

پس از ورود موفق، اسکریپت به صورت خودکار :

-- فایل ZIP کلاس را دانلود می‌کند.

-- ویدیوها را استخراج کرده.

-- فایل نهایی ترکیب‌شده با نام .flv در پوشه /videos/ ذخیره می‌شود.

-- در صورت وجود اشتراک‌گذاری صفحه، فایل جداگانه screen.flv ایجاد می‌کند.

-- فایل گفتگوها در /chats/chats.txt ذخیره می‌شود.

#### ویدیوی آموزشی (ویندوز)

[Video tutorial](https://uplod.ir/mza1m6i9wi47/Amoozesh.mp4.htm)

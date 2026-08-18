from pathlib import Path
import re


# =========================================================
# MANAVOĞLU VERA - OTOMATİK GÖRSEL LİSTELEYİCİ
# =========================================================

IMAGES_DIR = Path("images/vera")

OUTPUT_FILE = Path("data/vera-gallery.js")


# =========================================================
# DOSYA ADINI KATEGORİYE ÇEVİR
# =========================================================

def classify(filename):

    name = filename.lower()

    # RENDER
    if "render" in name:
        return "renders"

    # PLAN BOYAMA
    if "planboyama" in name:

        if "zemin" in name:
            return "zemin"

        if "bodrum" in name:
            return "bodrum"

        if "1kat" in name or "1-kat" in name:
            return "1kat"

        if "2kat" in name or "2-kat" in name:
            return "2kat"

        if "3kat" in name or "3-kat" in name:
            return "3kat"

        if "cati" in name or "çatı" in name:
            return "cati"

        return "planlar"

    # İÇ MEKAN
    if "icmekan" in name or "içmekan" in name:
        return "icmekan"

    # GÖRÜNÜŞ
    if "gorunus" in name or "görünüş" in name:
        return "gorunus"

    return None


# =========================================================
# GÖRSELLERİ BUL
# =========================================================

def scan_images():

    gallery = {
        "renders": [],
        "plans": {
            "bodrum": [],
            "zemin": [],
            "1kat": [],
            "2kat": [],
            "3kat": [],
            "cati": [],
            "planlar": []
        },
        "icmekan": [],
        "gorunus": []
    }

    if not IMAGES_DIR.exists():
        print("images/vera klasörü bulunamadı.")
        return gallery

    for file in sorted(IMAGES_DIR.rglob("*")):

        if not file.is_file():
            continue

        if file.suffix.lower() not in [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        ]:
            continue

        category = classify(file.name)

        if category is None:
            continue

        path = "../" + file.as_posix()

        if category == "renders":

            gallery["renders"].append(path)

        elif category in gallery["plans"]:

            gallery["plans"][category].append(path)

        elif category == "icmekan":

            gallery["icmekan"].append(path)

        elif category == "gorunus":

            gallery["gorunus"].append(path)

    return gallery


# =========================================================
# JAVASCRIPT DOSYASI OLUŞTUR
# =========================================================

gallery = scan_images()

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

javascript = f"""
window.VERA_GALLERY = {repr(gallery)};
"""

OUTPUT_FILE.write_text(
    javascript,
    encoding="utf-8"
)

print("====================================")
print("MANAVOĞLU VERA GALERİ TARAMASI")
print("====================================")

print(
    "Render:",
    len(gallery["renders"])
)

print(
    "Zemin:",
    len(gallery["plans"]["zemin"])
)

print(
    "1. Kat:",
    len(gallery["plans"]["1kat"])
)

print(
    "2. Kat:",
    len(gallery["plans"]["2kat"])
)

print(
    "3. Kat:",
    len(gallery["plans"]["3kat"])
)

print(
    "İç Mekan:",
    len(gallery["icmekan"])
)

print(
    "Görünüş:",
    len(gallery["gorunus"])
)

print("====================================")

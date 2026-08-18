from pathlib import Path
import re
import html


# =========================================================
# AYARLAR
# =========================================================

PROJECT_NAME = "Manavoğlu Vera"

IMAGES_DIR = Path("images/vera")

OUTPUT_FILE = Path("projeler/manavoglu-vera.html")


# =========================================================
# DOSYA ADINDAN KATEGORİ BELİRLEME
# =========================================================

def classify_image(filename):

    name = filename.lower()

    # -----------------------------------------
    # RENDER
    # -----------------------------------------

    if "render" in name:

        return {
            "category": "renders",
            "title": "Render"
        }


    # -----------------------------------------
    # PLAN BOYAMA
    # -----------------------------------------

    if "planboyama" in name:

        if "zemin" in name:
            title = "ZEMİN KAT"

        elif "bodrum" in name:
            title = "BODRUM KAT"

        elif "1kat" in name or "1-kat" in name:
            title = "1. KAT"

        elif "2kat" in name or "2-kat" in name:
            title = "2. KAT"

        elif "3kat" in name or "3-kat" in name:
            title = "3. KAT"

        elif "cati" in name or "çatı" in name:
            title = "ÇATI KATI"

        else:
            title = "PLAN"


        return {
            "category": "plans",
            "title": title
        }


    # -----------------------------------------
    # İÇ MEKAN
    # -----------------------------------------

    if "icmekan" in name or "içmekan" in name:

        if "salon" in name:
            title = "SALON"

        elif "mutfak" in name:
            title = "MUTFAK"

        elif "yatak" in name:
            title = "YATAK ODASI"

        elif "banyo" in name:
            title = "BANYO"

        else:
            title = "İÇ MEKAN"


        return {
            "category": "interior",
            "title": title
        }


    # -----------------------------------------
    # GÖRÜNÜŞ
    # -----------------------------------------

    if "gorunus" in name or "görünüş" in name:

        if "kuzey" in name:
            title = "KUZEY"

        elif "guney" in name or "güney" in name:
            title = "GÜNEY"

        elif "dogu" in name or "doğu" in name:
            title = "DOĞU"

        elif "bati" in name or "batı" in name:
            title = "BATI"

        else:
            title = "GÖRÜNÜŞ"


        return {
            "category": "elevations",
            "title": title
        }


    return None


# =========================================================
# GÖRSELLERİ BUL
# =========================================================

def get_images():

    categories = {
        "plans": [],
        "renders": [],
        "interior": [],
        "elevations": []
    }


    if not IMAGES_DIR.exists():

        print("images/vera klasörü bulunamadı.")

        return categories


    for file in IMAGES_DIR.rglob("*"):

        if not file.is_file():
            continue


        if file.suffix.lower() not in [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        ]:
            continue


        result = classify_image(file.name)


        if result is None:
            continue


        relative_path = file.as_posix()


        categories[
            result["category"]
        ].append({

            "path": "../" + relative_path,

            "title": result["title"],

            "filename": file.name

        })


    return categories


# =========================================================
# HTML GÖRSEL OLUŞTURUCULARI
# =========================================================

def build_plan_cards(items):

    output = ""


    for index, item in enumerate(items, 1):

        output += f"""
        <div class="plan-card">

            <img
                src="{html.escape(item['path'])}"
                alt="{html.escape(item['title'])}"
            >

            <div class="plan-label">

                <span>
                    {index:02d}
                </span>

                <strong>
                    {html.escape(item['title'])}
                </strong>

            </div>

        </div>
        """


    return output


def build_render_cards(items):

    output = ""


    for index, item in enumerate(items):

        size_class = "large" if index == 0 else ""


        output += f"""
        <div class="render-card {size_class}">

            <img
                src="{html.escape(item['path'])}"
                alt="Manavoğlu Vera Render {index + 1}"
            >

        </div>
        """


    return output


def build_interior_cards(items):

    output = ""


    for item in items:

        output += f"""
        <div class="interior-card">

            <img
                src="{html.escape(item['path'])}"
                alt="{html.escape(item['title'])}"
            >

            <div>
                {html.escape(item['title'])}
            </div>

        </div>
        """


    return output


def build_elevation_cards(items):

    output = ""


    for item in items:

        output += f"""
        <div class="elevation-card">

            <img
                src="{html.escape(item['path'])}"
                alt="{html.escape(item['title'])}"
            >

            <span>
                {html.escape(item['title'])}
            </span>

        </div>
        """


    return output


# =========================================================
# TAB OLUŞTUR
# =========================================================

def build_tab_content(data):

    plans = build_plan_cards(data["plans"])

    renders = build_render_cards(data["renders"])

    interiors = build_interior_cards(data["interior"])

    elevations = build_elevation_cards(data["elevations"])


    return f"""

<section class="vera-gallery">

    <div class="gallery-header">

        <p class="section-small">
            PROJE DETAYLARI
        </p>

        <h2>
            Projeyi keşfedin.
        </h2>

    </div>


    <div class="gallery-tabs">

        <button
            class="tab-button active"
            onclick="openTab(event, 'plans')">

            PLAN BOYAMALARI

        </button>


        <button
            class="tab-button"
            onclick="openTab(event, 'renders')">

            RENDERLAR

        </button>


        <button
            class="tab-button"
            onclick="openTab(event, 'interior')">

            İÇ MEKAN

        </button>


        <button
            class="tab-button"
            onclick="openTab(event, 'elevations')">

            GÖRÜNÜŞLER

        </button>

    </div>


    <div
        id="plans"
        class="tab-content active">

        <div class="gallery-title">

            <span>01</span>

            <h3>
                Plan Boyamaları
            </h3>

        </div>

        <div class="plan-grid">

            {plans}

        </div>

    </div>


    <div
        id="renders"
        class="tab-content">

        <div class="gallery-title">

            <span>02</span>

            <h3>
                Mimari Renderlar
            </h3>

        </div>

        <div class="render-grid">

            {renders}

        </div>

    </div>


    <div
        id="interior"
        class="tab-content">

        <div class="gallery-title">

            <span>03</span>

            <h3>
                İç Mekan
            </h3>

        </div>

        <div class="interior-grid">

            {interiors}

        </div>

    </div>


    <div
        id="elevations"
        class="tab-content">

        <div class="gallery-title">

            <span>04</span>

            <h3>
                Mimari Görünüşler
            </h3>

        </div>

        <div class="elevation-grid">

            {elevations}

        </div>

    </div>

</section>

"""


# =========================================================
# ANA HTML
# =========================================================

def build_page(data):

    gallery = build_tab_content(data)


    return f"""<!DOCTYPE html>

<html lang="tr">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>
        {PROJECT_NAME} | Manavoğlu İnşaat
    </title>

    <link
        rel="stylesheet"
        href="../css/style.css"
    >

</head>


<body>


<header class="navbar">

    <div class="logo">

        MANAVOĞLU

        <span>
            İNŞAAT
        </span>

    </div>


    <nav class="menu">

        <a href="../index.html">
            ANA SAYFA
        </a>

        <a href="#">
            KURUMSAL
        </a>

        <a href="../index.html#projects">
            PROJELER
        </a>

        <a href="#">
            HİZMETLER
        </a>

        <a href="#">
            İLETİŞİM
        </a>

    </nav>

</header>



<main>


<section class="project-hero">

    <img
        src="../images/manavoglu-vera.png"
        alt="Manavoğlu Vera"
    >

    <div class="project-hero-overlay"></div>


    <div class="project-hero-content">

        <p>
            MANAVOĞLU İNŞAAT
        </p>

        <h1>
            MANAVOĞLU<br>
            VERA
        </h1>

        <span>
            KONUT PROJESİ
        </span>

    </div>

</section>



<section class="project-intro">

    <div class="project-intro-title">

        <p class="section-small">
            PROJE HAKKINDA
        </p>

        <h2>
            Modern yaşam için
            tasarlanan yeni nesil
            yaşam alanı.
        </h2>

    </div>


    <div class="project-description">

        <p>
            Manavoğlu Vera, çağdaş mimari anlayışı,
            nitelikli malzeme kullanımı ve kullanıcı
            odaklı tasarım yaklaşımıyla ele alınan
            bir konut projesidir.
        </p>

        <p>
            Projenin tasarımında estetik, işlevsellik
            ve uzun ömürlü kullanım bir arada
            değerlendirilmiştir.
        </p>

    </div>

</section>



<section class="project-details">

    <div class="detail-item">

        <span>
            PROJE
        </span>

        <strong>
            MANAVOĞLU VERA
        </strong>

    </div>


    <div class="detail-item">

        <span>
            PROJE TÜRÜ
        </span>

        <strong>
            KONUT
        </strong>

    </div>


    <div class="detail-item">

        <span>
            KONUM
        </span>

        <strong>
            ANTALYA
        </strong>

    </div>


    <div class="detail-item">

        <span>
            TASARIM
        </span>

        <strong>
            MANAVOĞLU İNŞAAT
        </strong>

    </div>

</section>



{gallery}



<section class="project-contact">

    <p>
        MANAVOĞLU İNŞAAT
    </p>

    <h2>
        Projeniz hakkında
        konuşalım.
    </h2>

    <a href="#">
        İLETİŞİME GEÇ →
    </a>

</section>


</main>



<script>

function openTab(event, tabName) {{

    const contents =
        document.querySelectorAll(".tab-content");


    const buttons =
        document.querySelectorAll(".tab-button");


    contents.forEach(function(content) {{

        content.classList.remove("active");

    }});


    buttons.forEach(function(button) {{

        button.classList.remove("active");

    }});


    document
        .getElementById(tabName)
        .classList.add("active");


    event.currentTarget
        .classList.add("active");

}}

</script>


</body>

</html>
"""


# =========================================================
# ÇALIŞTIR
# =========================================================

data = get_images()

page = build_page(data)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE.write_text(
    page,
    encoding="utf-8"
)


print("Manavoglu Vera galerisi oluşturuldu.")

print(
    f"Planlar: {len(data['plans'])}"
)

print(
    f"Renderlar: {len(data['renders'])}"
)

print(
    f"İç mekan: {len(data['interior'])}"
)

print(
    f"Görünüşler: {len(data['elevations'])}"
)

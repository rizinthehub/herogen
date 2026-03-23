from fpdf import FPDF
import requests
import tempfile
import os
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


def _download_image(url):
    """Handle both local file paths and URLs."""
    if not url:
        return None

    # If it's already a local file, return it directly
    if os.path.exists(url):
        return url

    # Otherwise treat it as a URL and download it
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.write(response.content)
        tmp.close()
        return tmp.name
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def _create_coloring_image(image_path):
    """Convert a color image into a black-and-white coloring page."""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path)
        img = img.resize((800, 800))
        gray = img.convert("L")
        edges = gray.filter(ImageFilter.CONTOUR)
        edges = ImageOps.autocontrast(edges, cutoff=2)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        edges.save(tmp.name)
        tmp.close()
        return tmp.name
    except Exception as e:
        print(f"Error creating coloring image: {e}")
        return None


def _safe_text(text):
    """Clean text for PDF compatibility."""
    if not text:
        return ""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def create_full_pdf(story_data, image_urls):
    """Create the complete Edu-Pack PDF with story, coloring pages, and edu sheet."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    title = _safe_text(story_data.get("title", "My Story"))

    # ---- COVER PAGE ----
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 36)
    pdf.ln(30)
    pdf.multi_cell(0, 18, title, align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 16)
    pdf.cell(0, 10, "A Personalized Story by HeroGen", align="C")

    if image_urls and image_urls[0]:
        img_path = _download_image(image_urls[0])
        if img_path:
            try:
                pdf.image(img_path, x=30, y=90, w=150)
            except:
                pass
            # Only delete if it was a downloaded temp file
            if not os.path.exists(image_urls[0]):
                os.unlink(img_path)

    # ---- STORY PAGES ----
    for i, page in enumerate(story_data.get("pages", [])):
        pdf.add_page()

        # Page header
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, f"Page {page.get('page_num', i+1)}", align="C")
        pdf.ln(5)
        pdf.set_text_color(0, 0, 0)

        # Image
        if i < len(image_urls) and image_urls[i]:
            img_path = _download_image(image_urls[i])
            if img_path:
                try:
                    pdf.image(img_path, x=25, y=25, w=160)
                    pdf.set_y(140)
                except:
                    pdf.set_y(25)
                if not os.path.exists(image_urls[i]):
                    os.unlink(img_path)
            else:
                pdf.set_y(25)
        else:
            pdf.set_y(25)

        # Story text
        pdf.set_font("Helvetica", "", 14)
        pdf.multi_cell(0, 8, _safe_text(page.get("text", "")))

    # ---- COLORING PAGES ----
    for i, url in enumerate(image_urls or []):
        if url:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 22)
            pdf.cell(0, 12, f"Color Me! - Page {i+1}", align="C")
            pdf.ln(8)
            img_path = _download_image(url)
            if img_path:
                coloring_path = _create_coloring_image(img_path)
                if coloring_path:
                    try:
                        pdf.image(coloring_path, x=25, y=35, w=160)
                    except:
                        pass
                    os.unlink(coloring_path)
                if not os.path.exists(url):
                    os.unlink(img_path)

    # ---- EDU SHEET ----
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 15, "Teacher's Guide", align="C")
    pdf.ln(20)

    edu = story_data.get("edu_sheet", {})

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Vocabulary Words:")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    for word in edu.get("vocab", []):
        pdf.multi_cell(0, 8, f" * {_safe_text(word)}")
        pdf.ln(2)

    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Discussion Questions:")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    for q in edu.get("discussion", []):
        pdf.multi_cell(0, 8, f" * {_safe_text(q)}")
        pdf.ln(4)

    return bytes(pdf.output())


def create_coloring_pdf(image_urls):
    """Create PDF with only coloring pages."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 30)
    pdf.ln(40)
    pdf.cell(0, 15, "My Coloring Book", align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 14)
    pdf.cell(0, 10, "by HeroGen", align="C")

    for i, url in enumerate(image_urls or []):
        if url:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 22)
            pdf.cell(0, 12, f"Color Me! - Page {i+1}", align="C")
            img_path = _download_image(url)
            if img_path:
                coloring_path = _create_coloring_image(img_path)
                if coloring_path:
                    try:
                        pdf.image(coloring_path, x=20, y=30, w=170)
                    except:
                        pass
                    os.unlink(coloring_path)
                if not os.path.exists(url):
                    os.unlink(img_path)

    return bytes(pdf.output())


def create_edu_pdf(story_data):
    """Create PDF with only the teacher's edu sheet."""
    pdf = FPDF()
    pdf.add_page()

    title = _safe_text(story_data.get("title", "Story"))
    edu = story_data.get("edu_sheet", {})

    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 15, "Teacher's Guide", align="C")
    pdf.ln(15)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Story: {title}")
    pdf.ln(15)

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Vocabulary Words:")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    for word in edu.get("vocab", []):
        pdf.multi_cell(0, 8, f" * {_safe_text(word)}")
        pdf.ln(3)

    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Discussion Questions:")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 14)
    for q in edu.get("discussion", []):
        pdf.multi_cell(0, 8, f" * {_safe_text(q)}")
        pdf.ln(4)

    return bytes(pdf.output())
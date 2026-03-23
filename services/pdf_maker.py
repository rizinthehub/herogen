from fpdf import FPDF
import requests
import tempfile
import os
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


# ── HELPERS ───────────────────────────────────────────────────

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
    """Convert a color image into a clean black-and-white coloring page."""
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((800, 800), Image.LANCZOS)
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


def _cleanup_temp(path, original_url):
    """Only delete file if it was a downloaded temp file, not original."""
    if path and original_url and not os.path.exists(original_url):
        try:
            os.unlink(path)
        except:
            pass


def _add_cover_page(pdf, title, image_urls, child_name, moral):
    """Add a professional cover page to the PDF."""
    pdf.add_page()

    # Background header bar
    pdf.set_fill_color(255, 107, 107)  # Warm red
    pdf.rect(0, 0, 210, 50, "F")

    # HeroGen branding
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(10)
    pdf.cell(0, 10, "HeroGen - Personalized Storybooks", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, "Powered by AI, Made with Love", align="C")

    # Cover image
    if image_urls and image_urls[0]:
        img_path = _download_image(image_urls[0])
        if img_path:
            try:
                pdf.image(img_path, x=30, y=55, w=150, h=120)
            except:
                pass
            _cleanup_temp(img_path, image_urls[0])

    # Story title
    pdf.set_y(182)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 12, _safe_text(title), align="C")

    # Subtitle
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 13)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(
        0, 8,
        _safe_text(f"A story about {moral} starring {child_name}"),
        align="C"
    )

    # Footer bar
    pdf.set_fill_color(78, 205, 196)  # Teal
    pdf.rect(0, 270, 210, 27, "F")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(277)
    pdf.cell(0, 8, "A Personalized Story by HeroGen", align="C")


def _add_story_pages(pdf, pages, image_urls):
    """Add all story pages with image and rich paragraph text."""
    for i, page in enumerate(pages):
        pdf.add_page()

        # ── Page number header ──
        pdf.set_fill_color(248, 249, 250)
        pdf.rect(0, 0, 210, 12, "F")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.set_y(3)
        pdf.cell(0, 6, f"Page {page.get('page_num', i+1)} of {len(pages)}", align="C")

        # ── Story image ──
        if i < len(image_urls) and image_urls[i]:
            img_path = _download_image(image_urls[i])
            if img_path:
                try:
                    pdf.image(img_path, x=15, y=15, w=180, h=120)
                except:
                    pass
                _cleanup_temp(img_path, image_urls[i])

        # ── Decorative divider ──
        pdf.set_draw_color(255, 107, 107)
        pdf.set_line_width(0.8)
        pdf.line(15, 140, 195, 140)

        # ── Story text ──
        pdf.set_y(145)
        pdf.set_font("Helvetica", "", 12)
        pdf.set_text_color(40, 40, 40)
        pdf.set_left_margin(15)
        pdf.set_right_margin(15)

        # Line height 7 gives comfortable reading spacing
        pdf.multi_cell(0, 7, _safe_text(page.get("text", "")))

        # ── Quiz section ──
        pdf.ln(5)
        pdf.set_fill_color(255, 249, 230)  # Soft yellow
        pdf.set_draw_color(255, 200, 100)
        pdf.set_line_width(0.5)

        # Quiz box
        current_y = pdf.get_y()
        pdf.rect(15, current_y, 180, 28, "FD")

        pdf.set_y(current_y + 3)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(180, 100, 0)
        pdf.cell(0, 6, "Think About It:", align="C")
        pdf.ln(5)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(80, 60, 0)
        pdf.multi_cell(0, 5, _safe_text(page.get("quiz", "")), align="C")

        # Reset margins
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)


def _add_coloring_pages(pdf, image_urls):
    """Add black and white coloring pages."""
    pdf.add_page()

    # Section header
    pdf.set_fill_color(78, 205, 196)
    pdf.rect(0, 0, 210, 35, "F")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(8)
    pdf.cell(0, 12, "Coloring Pages", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, "Color the story your way!", align="C")

    for i, url in enumerate(image_urls or []):
        if url:
            pdf.add_page()

            # Page title
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(100, 100, 100)
            pdf.set_y(8)
            pdf.cell(0, 10, f"Scene {i+1} - Color Me!", align="C")
            pdf.ln(3)

            # Coloring image
            img_path = _download_image(url)
            if img_path:
                coloring_path = _create_coloring_image(img_path)
                if coloring_path:
                    try:
                        pdf.image(coloring_path, x=15, y=25, w=180, h=180)
                    except:
                        pass
                    os.unlink(coloring_path)
                _cleanup_temp(img_path, url)

            # Fun instruction
            pdf.set_y(210)
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 8, "Use your favorite colors to bring this scene to life!", align="C")


def _add_edu_sheet(pdf, story_data):
    """Add a professional teacher's guide and edu sheet."""
    pdf.add_page()

    # Header
    pdf.set_fill_color(107, 107, 255)  # Purple
    pdf.rect(0, 0, 210, 35, "F")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(8)
    pdf.cell(0, 12, "Teacher's Guide & Edu Sheet", align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, f"Story: {_safe_text(story_data.get('title', ''))}", align="C")

    edu = story_data.get("edu_sheet", {})
    pdf.set_text_color(40, 40, 40)

    # ── Vocabulary Section ──
    pdf.set_y(45)
    pdf.set_fill_color(230, 240, 255)
    pdf.rect(10, pdf.get_y(), 190, 10, "F")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(50, 50, 150)
    pdf.cell(0, 10, "  Vocabulary Words", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    for word in edu.get("vocab", []):
        pdf.set_x(15)
        pdf.cell(5, 7, "-")
        pdf.multi_cell(0, 7, _safe_text(word))
        pdf.ln(1)

    # ── Discussion Questions Section ──
    pdf.ln(5)
    pdf.set_fill_color(230, 255, 240)
    pdf.rect(10, pdf.get_y(), 190, 10, "F")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(50, 150, 80)
    pdf.cell(0, 10, "  Discussion Questions", ln=True)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(40, 40, 40)
    for idx, q in enumerate(edu.get("discussion", []), 1):
        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(8, 7, f"Q{idx}.")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, _safe_text(q))
        pdf.ln(3)

    # ── Moral Summary ──
    pdf.ln(5)
    pdf.set_fill_color(255, 240, 230)
    current_y = pdf.get_y()
    pdf.rect(10, current_y, 190, 10, "F")
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(200, 100, 50)
    pdf.cell(0, 10, "  The Moral of This Story", ln=True)
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.set_x(15)
    pdf.multi_cell(
        0, 7,
        _safe_text(
            f"Through this story, {story_data.get('title', 'our hero')} teaches us "
            f"that doing the right thing, even when it is hard, "
            f"always makes the world a better place."
        )
    )


# ── PUBLIC FUNCTIONS ──────────────────────────────────────────

def create_full_pdf(story_data, image_urls):
    """Create the complete professional Edu-Pack PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    child_name = story_data.get("child_name", "Hero")
    moral = story_data.get("moral", "kindness")
    title = story_data.get("title", "My Story")

    _add_cover_page(pdf, title, image_urls, child_name, moral)
    _add_story_pages(pdf, story_data.get("pages", []), image_urls)
    _add_coloring_pages(pdf, image_urls)
    _add_edu_sheet(pdf, story_data)

    return bytes(pdf.output())


def create_coloring_pdf(image_urls):
    """Create PDF with only coloring pages."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cover
    pdf.add_page()
    pdf.set_fill_color(78, 205, 196)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(100)
    pdf.cell(0, 15, "My Coloring Book", align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 16)
    pdf.cell(0, 10, "by HeroGen", align="C")

    for i, url in enumerate(image_urls or []):
        if url:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(100, 100, 100)
            pdf.set_y(8)
            pdf.cell(0, 10, f"Scene {i+1} - Color Me!", align="C")

            img_path = _download_image(url)
            if img_path:
                coloring_path = _create_coloring_image(img_path)
                if coloring_path:
                    try:
                        pdf.image(coloring_path, x=15, y=25, w=180, h=180)
                    except:
                        pass
                    os.unlink(coloring_path)
                _cleanup_temp(img_path, url)

    return bytes(pdf.output())


def create_edu_pdf(story_data):
    """Create PDF with only the teacher's edu sheet."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    _add_edu_sheet(pdf, story_data)
    return bytes(pdf.output())
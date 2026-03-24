from fpdf import FPDF
import requests
import tempfile
import os
from PIL import Image, ImageFilter, ImageOps


def _download_image(url):
    if not url:
        return None
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
    if not text:
        return ""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _download_all_images(image_urls):
    paths = []
    for url in (image_urls or []):
        paths.append(_download_image(url))
    return paths


def _cleanup_paths(paths):
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except Exception:
                pass


def create_full_pdf(story_data, image_urls):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    title = _safe_text(story_data.get("title", "My Story"))
    image_paths = _download_all_images(image_urls)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 32)
    pdf.ln(20)
    pdf.multi_cell(0, 16, title, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 14)
    pdf.cell(0, 10, "A Personalized Story by HeroGen", align="C")
    if image_paths and image_paths[0]:
        try:
            pdf.image(image_paths[0], x=30, y=80, w=150)
        except Exception:
            pass

    for i, page in enumerate(story_data.get("pages", [])):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, f"Page {page.get('page_num', i+1)}", align="C")
        pdf.set_text_color(0, 0, 0)

        if i < len(image_paths) and image_paths[i]:
            try:
                pdf.image(image_paths[i], x=35, y=18, w=140)
            except Exception:
                pass

        pdf.set_y(155)
        pdf.set_draw_color(255, 200, 150)
        pdf.set_line_width(0.8)
        pdf.line(20, 153, 190, 153)
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 15)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(170, 9, _safe_text(page.get("text", "")), align="L")

    for i, img_path in enumerate(image_paths):
        if img_path:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 24)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 15, f"Color Me! - Page {i+1}", align="C")
            pdf.ln(10)
            coloring_path = _create_coloring_image(img_path)
            if coloring_path:
                try:
                    pdf.image(coloring_path, x=15, y=35, w=180)
                except Exception:
                    pass
                os.unlink(coloring_path)

    pdf.add_page()
    pdf.set_fill_color(78, 205, 196)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(5)
    pdf.cell(0, 12, "Teacher's Guide", align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, f"Story: {title}", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(40)

    edu = story_data.get("edu_sheet", {})

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(78, 205, 196)
    pdf.cell(0, 10, "Story Summary")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    pages_data = story_data.get("pages", [])
    if pages_data:
        pdf.multi_cell(170, 7, _safe_text(pages_data[0].get("text", "")))
        if len(pages_data) > 1:
            pdf.ln(2)
            last_text = _safe_text(pages_data[-1].get("text", ""))
            pdf.multi_cell(170, 7, "The story concludes: " + last_text)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 107, 107)
    pdf.cell(0, 10, "Vocabulary Words")
    pdf.ln(10)
    pdf.set_text_color(60, 60, 60)
    for idx, word in enumerate(edu.get("vocab", []), 1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(10, 8, f"{idx}.")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(160, 7, f" {_safe_text(word)}")
        pdf.ln(4)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(78, 205, 196)
    pdf.cell(0, 10, "Discussion Questions")
    pdf.ln(10)
    pdf.set_text_color(60, 60, 60)
    for idx, q in enumerate(edu.get("discussion", []), 1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(10, 8, f"Q{idx}.")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(160, 7, f" {_safe_text(q)}")
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(180, 180, 180)
        pdf.cell(10, 6, "")
        pdf.cell(0, 6, "Answer: _______________________________________________")
        pdf.ln(6)
        pdf.set_text_color(60, 60, 60)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 107, 107)
    pdf.cell(0, 10, "Classroom Activities")
    pdf.ln(10)
    pdf.set_text_color(60, 60, 60)
    activities = [
        "Ask children to draw their own version of the moral lesson.",
        "Role-play: Act out scenes from the story.",
        "Writing prompt: Write about a time you showed this value.",
        "Group discussion: What makes this value important?",
        "Art project: Create a poster showing the moral.",
    ]
    for idx, act in enumerate(activities, 1):
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(10, 7, f"{idx}.")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(160, 7, f" {act}")
        pdf.ln(3)

    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(78, 205, 196)
    pdf.cell(0, 10, "Learning Objectives")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(60, 60, 60)
    objectives = [
        "Identify and understand the moral theme.",
        "Expand vocabulary through context clues.",
        "Develop empathy by discussing character emotions.",
        "Practice reading comprehension.",
        "Express creativity through coloring and drawing.",
    ]
    for obj in objectives:
        pdf.cell(8, 7, "")
        pdf.cell(170, 7, "- " + obj)
        pdf.ln(6)

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 8, "Generated by HeroGen", align="C")

    _cleanup_paths(image_paths)
    return bytes(pdf.output())


def create_coloring_pdf(image_urls):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 30)
    pdf.ln(40)
    pdf.cell(0, 15, "My Coloring Book", align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 14)
    pdf.cell(0, 10, "by HeroGen", align="C")
    image_paths = _download_all_images(image_urls)
    for i, img_path in enumerate(image_paths):
        if img_path:
            pdf.add_page()
            pdf.set_font("Helvetica", "B", 22)
            pdf.cell(0, 12, f"Color Me! - Page {i+1}", align="C")
            coloring_path = _create_coloring_image(img_path)
            if coloring_path:
                try:
                    pdf.image(coloring_path, x=15, y=30, w=180)
                except Exception:
                    pass
                os.unlink(coloring_path)
    _cleanup_paths(image_paths)
    return bytes(pdf.output())


def create_edu_pdf(story_data):
    pdf = FPDF()
    pdf.add_page()
    title = _safe_text(story_data.get("title", "Story"))
    edu = story_data.get("edu_sheet", {})

    pdf.set_fill_color(78, 205, 196)
    pdf.rect(0, 0, 210, 30, "F")
    pdf.set_font("Helvetica", "B", 26)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(5)
    pdf.cell(0, 12, "Teacher's Guide", align="C")
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, f"Story: {title}", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(40)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 107, 107)
    pdf.cell(0, 10, "Vocabulary Words")
    pdf.ln(12)
    pdf.set_text_color(60, 60, 60)
    for idx, word in enumerate(edu.get("vocab", []), 1):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(10, 8, f"{idx}.")
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(160, 8, f" {_safe_text(word)}")
        pdf.ln(5)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(78, 205, 196)
    pdf.cell(0, 10, "Discussion Questions")
    pdf.ln(12)
    pdf.set_text_color(60, 60, 60)
    for idx, q in enumerate(edu.get("discussion", []), 1):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(10, 8, f"Q{idx}.")
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(160, 8, f" {_safe_text(q)}")
        pdf.ln(2)
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(180, 180, 180)
        pdf.cell(10, 6, "")
        pdf.cell(0, 6, "Answer: _______________________________________________")
        pdf.ln(8)
        pdf.set_text_color(60, 60, 60)
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 107, 107)
    pdf.cell(0, 10, "Suggested Activities")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    activities = [
        "Draw your favorite scene from the story.",
        "Retell the story in your own words.",
        "Create a poster about the moral.",
        "Write a letter to the main character.",
        "Act out the story as a classroom play.",
    ]
    for idx, act in enumerate(activities, 1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(10, 8, f"{idx}.")
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(160, 8, f" {act}")
        pdf.ln(4)

    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 8, "Generated by HeroGen", align="C")
    return bytes(pdf.output())
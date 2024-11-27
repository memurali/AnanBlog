import os
from django.conf import settings
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import traceback
from bs4 import BeautifulSoup

def remove_inline_styles(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(style=True):
        del tag['style']

    return str(soup)


def inline_image_mapper(img_src: str):
    if img_src.startswith('/media'):
        return os.path.join(settings.BASE_DIR, img_src.lstrip('/'))
    return img_src


def resize_images(html_content, width):
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'):
        img['width'] = width
        if 'height' in img.attrs:
            del img['height']

    return str(soup)


class BlogPDF(FPDF):
    def __init__(self):
        print("Initializing BlogPDF")
        super().__init__()
        font_dir = os.path.join(settings.BASE_DIR, 'staticfiles', 'fonts')
        print(f"Font directory: {font_dir}")
        try:
            self.add_font("DejaVu", style="", fname=os.path.join(font_dir, 'DejaVuSans.ttf'), uni=True)
            self.add_font("DejaVu", style="B", fname=os.path.join(font_dir, 'DejaVuSans-Bold.ttf'), uni=True)
            self.add_font("DejaVu", style="I", fname=os.path.join(font_dir, 'DejaVuSans-Oblique.ttf'), uni=True)
            print("Fonts added successfully")
        except Exception as e:
            print(f"Error adding fonts: {str(e)}")
            print(traceback.format_exc())

    def header(self):
        print("Generating PDF header")
        self.set_font("DejaVu", style="I", size=8)
        self.cell(30, 10, 'Rendered from Anang Tawiah\'s Blog', 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.ln()

    def footer(self):
        print("Generating PDF footer")
        self.set_y(-15)
        self.set_font("DejaVu", style="I", size=8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf(title, shortDescription, highLights, content, image):
    try:
        print("Starting PDF generation")
        pdf = BlogPDF()
        pdf.add_page()

        print("Adding title")
        pdf.set_font("DejaVu", style="B", size=16)
        pdf.multi_cell(0, 10, title)
        pdf.ln(10)

        print("Adding short description")
        pdf.set_font("DejaVu", style="", size=12)
        pdf.multi_cell(0, 10, shortDescription)
        pdf.ln(10)

        try:
            print(f"Adding image from path: {image}")
            pdf.image(image, w=pdf.epw)
            pdf.ln(10)
        except:
            print("No image path provided, skipping image")

        if highLights:
            print("Adding highlights")
            pdf.set_font("DejaVu", style="B", size=14)
            pdf.cell(0, 10, "Highlights", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("DejaVu", style="", size=12)
            pdf.write_html(remove_inline_styles(highLights))
            pdf.ln(10)

        print("Adding content")
        pdf.set_font("DejaVu", style="B", size=14)
        pdf.cell(0, 10, "Content", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("DejaVu", style="", size=12)
        content = remove_inline_styles(content)
        content = resize_images(content, int(pdf.epw))
        pdf.write_html(remove_inline_styles(content), image_map=inline_image_mapper)

        print("Generating PDF output")
        output = pdf.output()
        print("PDF generation complete")
        return output
    except Exception as e:
        print(f"Error in PDF generation: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return None

"""
Convert markdown documentation files to a Word document.
"""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import re

# Define the 13 documentation files in order
DOC_FILES = [
    "01_Overview.md",
    "02_Getting_Started.md",
    "03_Configuration.md",
    "04_Data_Pipeline.md",
    "05_Feature_Engineering.md",
    "06_Models.md",
    "07_Training_Pipeline.md",
    "08_Ensembling_and_Conformal.md",
    "09_API_and_Service.md",
    "10_Dashboard.md",
    "11_Deployment_and_CI.md",
    "12_Testing_and_Quality.md",
    "13_Troubleshooting_and_Examples.md",
]

def parse_markdown_content(md_text):
    """Parse markdown into structured sections."""
    sections = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Heading
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            sections.append(('heading', level, text))
        # Code block
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            lang = line[3:].strip() if len(line) > 3 else ''
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            sections.append(('code', '\n'.join(code_lines), lang))
        # Bullet list
        elif line.strip().startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(lines[i].strip()[2:])
                i += 1
            sections.append(('list', items))
            continue
        # Paragraph
        elif line.strip():
            sections.append(('paragraph', line.strip()))
        
        i += 1
    
    return sections

def add_markdown_to_docx(doc, md_file_path):
    """Add markdown file content to Word document."""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = parse_markdown_content(content)
    
    for section in sections:
        if section[0] == 'heading':
            _, level, text = section
            style = f'Heading {min(level, 9)}'
            doc.add_paragraph(text, style=style)
        
        elif section[0] == 'code':
            _, code_text, lang = section
            p = doc.add_paragraph()
            p.style = 'Normal'
            run = p.add_run(code_text.strip())
            run.font.name = 'Courier New'
            run.font.size = Pt(9)
        
        elif section[0] == 'list':
            _, items = section
            for item in items:
                doc.add_paragraph(item, style='List Bullet')
        
        elif section[0] == 'paragraph':
            _, text = section
            # Simple markdown formatting
            text = text.replace('**', '')
            text = text.replace('`', '')
            text = text.replace('_', '')
            doc.add_paragraph(text)

def main():
    """Main conversion function."""
    docs_dir = Path(__file__).parent
    output_file = docs_dir / "Sales_Forecast_Pro_Documentation.docx"
    
    # Create Word document
    doc = Document()
    
    # Add title
    title = doc.add_heading('Sales Forecast Pro — Complete Documentation', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Add table of contents placeholder
    doc.add_heading('Table of Contents', 1)
    for i, fname in enumerate(DOC_FILES, 1):
        title = fname.replace('_', ' ').replace('.md', '')
        doc.add_paragraph(title, style='List Bullet')
    
    doc.add_page_break()
    
    # Add each markdown file
    for md_file in DOC_FILES:
        md_path = docs_dir / md_file
        
        if md_path.exists():
            print(f"Adding {md_file}...")
            add_markdown_to_docx(doc, md_path)
            doc.add_page_break()
        else:
            print(f"Warning: {md_file} not found")
    
    # Save the document
    doc.save(output_file)
    print(f"\n✓ Word document created: {output_file}")
    print(f"  Size: {output_file.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()

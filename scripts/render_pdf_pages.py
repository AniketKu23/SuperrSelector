import fitz  # PyMuPDF
import os

def render_pages():
    os.makedirs('report_screenshots', exist_ok=True)
    doc = fitz.open('SupeRR_Selector_Season_2_Methodology_Report.pdf')
    print(f"Total pages in PDF: {len(doc)}")
    
    saved_paths = []
    for i, page in enumerate(doc):
        # Render page at 2x resolution (144 dpi) for crisp inspection
        pix = page.get_pixmap(dpi=150)
        img_path = f"report_screenshots/page_{i+1}.png"
        pix.save(img_path)
        saved_paths.append(img_path)
        print(f"Rendered Page {i+1} to {img_path} ({pix.width}x{pix.height})")
        
    return saved_paths

if __name__ == '__main__':
    render_pages()

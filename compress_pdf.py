import fitz  # PyMuPDF
import sys
import os

input_file = "health risk ai certificate.pdf"
output_file = "completion_report.pdf"

try:
    doc = fitz.open(input_file)
    
    # Create a new empty PDF
    new_doc = fitz.open()
    
    # We only need the first page (the completion report)
    # The second page is usually the transcript which takes up space
    page = doc.load_page(0)
    
    # Render the page to an image (dpi 150 to keep size small but readable)
    pix = page.get_pixmap(dpi=150)
    
    # Create a new page in the new pdf with the same dimensions
    new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
    
    # Insert the image into the new page
    new_page.insert_image(page.rect, pixmap=pix)
    
    # Save the new document
    new_doc.save(output_file, deflate=True)
    new_doc.close()
    doc.close()
    
    print(f"New compressed size: {os.path.getsize(output_file) / 1024:.2f} KB")
except Exception as e:
    print(f"Error: {e}")

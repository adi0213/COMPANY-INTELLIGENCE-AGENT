"""
PDF Exporter Module

Requires `wkhtmltopdf` to be installed on the system path for Windows.
If it fails, it gracefully falls back to just providing the Markdown.
"""

import os
import logging
import markdown
import pdfkit

logger = logging.getLogger(__name__)

class PDFExporter:
    def __init__(self, output_dir: str = "data/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export(self, company_name: str, md_content: str) -> str:
        """
        Converts Markdown to HTML, then HTML to PDF.
        """
        file_name = f"{company_name.lower().replace(' ', '_')}_report.pdf"
        file_path = os.path.join(self.output_dir, file_name)
        
        html_content = markdown.markdown(md_content)
        
        # Add basic styling to HTML
        styled_html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                    h1 {{ color: #2C3E50; border-bottom: 2px solid #2C3E50; padding-bottom: 10px; }}
                    h2 {{ color: #34495E; margin-top: 30px; }}
                    h3 {{ color: #7F8C8D; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """
        
        try:
            pdfkit.from_string(styled_html, file_path)
            logger.info(f"Report exported to PDF: {file_path}")
            return file_path
        except Exception as e:
            logger.warning(f"Failed to generate PDF (wkhtmltopdf might be missing): {e}")
            logger.warning("Falling back to Markdown only.")
            return None

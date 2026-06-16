"""
Markdown Exporter Module
"""

import os
import logging
import markdown

logger = logging.getLogger(__name__)

class MarkdownExporter:
    def __init__(self, output_dir: str = "data/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def export(self, company_name: str, md_content: str) -> str:
        """
        Saves the markdown file.
        """
        file_name = f"{company_name.lower().replace(' ', '_')}_report.md"
        file_path = os.path.join(self.output_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        logger.info(f"Report exported to Markdown: {file_path}")
        return file_path

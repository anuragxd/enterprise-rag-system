"""
Document loader module for extracting text from PDFs
"""
import PyPDF2
from pathlib import Path
from loguru import logger

class DocumentLoader:
    """Handles loading and extracting text from PDF documents"""
    
    def __init__(self):
        logger.info("DocumentLoader initialized")
    
    def load_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"Loading PDF: {pdf_path} ({num_pages} pages)")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                if not text.strip():
                    logger.warning(f"No text extracted from {pdf_path}")
                    return ""
                
                logger.info(f"Successfully extracted {len(text)} characters from {pdf_path}")
                return text
                
        except PyPDF2.errors.PdfReadError as e:
            logger.error(f"PDF read error for {pdf_path}: {e}")
            return ""
        except Exception as e:
            logger.error(f"Error loading PDF {pdf_path}: {e}")
            return ""
    
    def load_multiple_pdfs(self, pdf_dir: str) -> dict:
        """
        Load multiple PDFs from a directory
        
        Args:
            pdf_dir: Directory containing PDF files
            
        Returns:
            Dictionary mapping filenames to extracted text
        """
        pdf_path = Path(pdf_dir)
        results = {}
        
        if not pdf_path.exists():
            logger.error(f"Directory not found: {pdf_dir}")
            return results
        
        pdf_files = list(pdf_path.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files in {pdf_dir}")
        
        for pdf_file in pdf_files:
            text = self.load_pdf(str(pdf_file))
            if text:
                results[pdf_file.name] = text
        
        return results

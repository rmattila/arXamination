import os
import requests
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

from urllib.parse import urlparse, unquote

from arxamination.utils import ensure_directory_exists

ARXIV_BASE_URL = "https://arxiv.org/pdf/{}.pdf"


class DownloadError(Exception):
    """Raised when there is an issue downloading the PDF."""

    pass


class PDFExtractionError(Exception):
    """Raised when there is an issue extracting text from a PDF."""

    pass


def fetch_pdf_from_url(url: str, download_dir: str = "documents") -> str:
    """
    Fetch an article from an arbitrary URL.

    First checks if the paper has already been downloaded, otherwise proceeds
    to download it.

    Args:
        url (str): URL to the article.
        download_dir (str): The directory to download and save PDF files.

    Returns:
        str: The local file path to the downloaded article.
    """
    # Parse out the filename from the URL
    parsed_url = urlparse(url)
    filename = unquote(os.path.basename(parsed_url.path))

    # Ensure download_dir exists
    ensure_directory_exists(download_dir)

    # Construct the full local file path
    local_file_path = os.path.join(download_dir, filename)

    # Check if the file already exists
    if not os.path.exists(local_file_path):
        # Download the file
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(local_file_path, "wb") as f:
                f.write(response.content)
            print(f"Downloaded '{filename}' to '{download_dir}'")
        except requests.RequestException as e:
            raise DownloadError(f"Error downloading file: {e}")
    else:
        print(f"File '{filename}' already exists in '{download_dir}'")

    return local_file_path


def fetch_pdf_from_arxiv(arxiv_id: str, download_dir: str = "documents") -> str:
    """
    Fetch an arXiv article.

    First checks if paper has already been downloaded, otherwise proceeds
    to download it.

    Args:
        arxiv_id (str): The arXiv article ID (e.g., '1706.037620').
        download_dir (str): The directory to download and save PDF files.

    Returns:
        str: The local file path to the downloaded article.
    """
    # Ensure download_dir exists
    ensure_directory_exists(download_dir)

    # Construct the full local file path
    pdf_file_path = os.path.join(download_dir, f"{arxiv_id}.pdf")

    # URL to arXiv paper
    pdf_url = ARXIV_BASE_URL.format(arxiv_id)

    # Check if article has already been downloaded
    if os.path.exists(pdf_file_path):
        print(f"PDF file for {arxiv_id} already exists in {pdf_file_path}")
    else:
        try:
            # download PDF if it doesn't exist
            print(f"Downloading from {pdf_url}")
            response = requests.get(pdf_url)
            response.raise_for_status()

            # save the PDF to the download directory
            with open(pdf_file_path, "wb") as pdf_file:
                pdf_file.write(response.content)
                print(f"arXiv article downloaded to {pdf_file_path}")
        except requests.exceptions.HTTPError as e:
            raise DownloadError(f"Error downloading arXiv article: {e}")

    return pdf_file_path


def process_pdf(pdf_file_path) -> str:
    """
    Extracts the text from a pdf file.

    Args:
        pdf_file_path (str): Local file path to the PDF.

    Returns:
        str: The extracted text from the PDF.
    """
    try:
        # Extract text from the pdf
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_text = extract_text(pdf_file)
    except (PDFSyntaxError, IOError):
        raise PDFExtractionError(f"Error extracting text from {pdf_file_path}: {e}")

    if not pdf_text:
        raise PDFExtractionError(
            f"No text could be extracted from the PDF file '{pdf_file_path}'"
        )

    return pdf_text

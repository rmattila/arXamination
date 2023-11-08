import os
import requests
from pdfminer.high_level import extract_text


def process_arxiv(arxiv_id: str, download_dir: str = "documents") -> str:
    """
    Fetch and process an arXiv article.

    Args:
        arxiv_id (str): The arXiv article ID (e.g., '1706.037620').
        download_dir (str): The directory to download and save PDF files.

    Returns:
        str: The extracted text from the PDF, or None if an error occurs.
    """
    # create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    # paths
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    pdf_file_path = os.path.join(download_dir, f"{arxiv_id}.pdf")

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
                print(f"Paper downloaded to {pdf_file_path}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            return None

    # extract text from the pdf
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_text = extract_text(pdf_file)

    return pdf_text

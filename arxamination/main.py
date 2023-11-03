import argparse

from . import arxiv_parser


def main():
    parser = argparse.ArgumentParser(description="Fetch and analyze arXiv articles.")
    parser.add_argument("arxiv_id", help="The arXiv article ID (e.g., '1706.03762')")
    args = parser.parse_args()
    arxiv_id = args.arxiv_id

    pdf_text = arxiv_parser.process_arxiv(arxiv_id)
    if pdf_text:
        # sample text to see what we loaded
        print(pdf_text[0:500])
    else:
        print(f"Failed to load text of {arxiv_id}")


if __name__ == "__main__":
    main()

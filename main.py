import argparse
import sys
import random
from typing import Dict, Tuple
from tqdm import tqdm
import toml

from arxamination.pdf_parser import (
    fetch_pdf_from_arxiv,
    fetch_pdf_from_url,
    process_pdf,
)
from arxamination.llm_interaction import BaseLLM, llm_factory
from arxamination.utils import is_arxiv_id, is_file, is_url, make_bold


def parse_arguments() -> argparse.Namespace:
    """Parse and return command line arguments."""

    parser = argparse.ArgumentParser(description="Fetch and analyze research papers")

    file_source_group = parser.add_mutually_exclusive_group(required=False)
    file_source_group.add_argument(
        "--id", help="Specify an Arxiv ID (e.g., '1706.03762')"
    )
    file_source_group.add_argument("--file", help="Specify a local file path")
    file_source_group.add_argument("--url", help="Specify a URL")

    parser.add_argument("input", nargs="?", help="Arxiv ID, URL, or file path")
    parser.add_argument(
        "--num_questions",
        "-n",
        type=int,
        default=None,
        help="Number of questions to sample",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Increase output verbosity"
    )
    parser.add_argument(
        "--model",
        "-m",
        help="Specify the language model to use",
        choices=["local", "openai"],
        default="local",
    )

    # Check if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def determine_source(args: argparse.Namespace) -> Tuple[str, str]:
    """Determine where to load PDF from.

    Returns:
        Tuple[str, str]: A tuple containing source type and value."""

    source = None
    if args.id:
        source = ("id", args.id)
    elif args.file:
        source = ("file", args.file)
    elif args.url:
        source = ("url", args.url)
    elif args.input:
        if is_arxiv_id(args.input):
            source = ("id", args.input)
        elif is_url(args.input):
            source = ("url", args.input)
        elif is_file(args.input):
            source = ("file", args.input)
        else:
            raise ValueError(
                "Input does not match expected patterns for Arxiv ID, URL, or file path."
            )

    if not source:
        raise ValueError("No valid source specified.")
    return source


def fetch_pdf(source_type: str, source_value: str) -> str:
    """Fetch the PDF from various sources."""
    if source_type == "id":
        # Fetch PDF from arXiv
        pdf_file_path = fetch_pdf_from_arxiv(source_value)
    elif source_type == "url":
        # Fetch PDF from the given URL
        pdf_file_path = fetch_pdf_from_url(source_value)
    elif source_type == "file":
        # Path to the local file (already provided)
        pdf_file_path = source_value

    return pdf_file_path


def initialize_llm(model_type: str, config: Dict, verbose: bool) -> BaseLLM:
    """Initialize and return LLM instance"""
    return llm_factory(model_type, config, verbose)


def main():
    args = parse_arguments()
    source_type, source_value = determine_source(args)

    pdf_file_path = fetch_pdf(source_type, source_value)

    # Extract text from PDF
    pdf_text = process_pdf(pdf_file_path)

    # Load config
    try:
        config = toml.load("config.toml")
    except (FileNotFoundError, toml.TomlDecodeError) as e:
        print(f"Error loading config file: {e}")
        return

    # Create an LLM based on user's choice
    language_model = initialize_llm(args.model, config, args.verbose)

    # If num_questions has not been set, go through all questions; otherwise, sample num_questions
    num_questions = args.num_questions
    if num_questions is None:
        questions = config["questions"]
    else:
        questions = random.sample(config["questions"], num_questions)

    with tqdm(questions, desc="Processing Questions") as pbar:
        for question in pbar:
            # Format the question for display in the progress bar
            formatted_question = (
                (question[:32] + "...?") if len(question) > 35 else question
            )
            description = f"[Q: {formatted_question}]"
            pbar.set_description(description)

            summary = language_model.process_with_llm(pdf_text, question)

            # Print the question and summary
            tqdm.write("\n")
            tqdm.write(make_bold(question))
            tqdm.write("-" * len(question))
            tqdm.write(summary.strip())
            tqdm.write("\n")


if __name__ == "__main__":
    main()

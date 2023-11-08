import argparse
import random
from tqdm import tqdm

from arxamination import arxiv_parser
from arxamination.llm_interaction import LocalLLM
from arxamination.utils import load_config_file, make_bold


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Fetch and analyze arXiv articles.")
    parser.add_argument("arxiv_id", help="The arXiv article ID (e.g., '1706.03762')")
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

    args = parser.parse_args()
    arxiv_id = args.arxiv_id
    num_questions = args.num_questions

    # Fetch and read PDF
    pdf_text = arxiv_parser.process_arxiv(arxiv_id)

    if not pdf_text:
        print(f"Failed to load text of {arxiv_id}")
        return

    # Load config and LLM
    config_file = "config.toml"
    llm = LocalLLM(config_file, verbose=args.verbose)
    config = load_config_file(config_file)

    print(f"Using model {config['model_choice']}")

    # If num_questions has not been set, go through all questions; otherwise, sample num_questions
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

            summary = llm.process_with_llm(pdf_text, question)

            # Print the question and summary
            tqdm.write("\n")
            tqdm.write(make_bold(question))
            tqdm.write("-" * len(question))
            tqdm.write(summary.strip())
            tqdm.write("\n")


if __name__ == "__main__":
    main()

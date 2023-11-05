import argparse
from tqdm import tqdm

from arxamination import arxiv_parser
from arxamination.llm_interaction import LocalLLM
from arxamination.utils import load_config_file, make_bold


def main():
    parser = argparse.ArgumentParser(description="Fetch and analyze arXiv articles.")
    parser.add_argument("arxiv_id", help="The arXiv article ID (e.g., '1706.03762')")
    args = parser.parse_args()
    arxiv_id = args.arxiv_id

    pdf_text = arxiv_parser.process_arxiv(arxiv_id)

    if not pdf_text:
        print(f"Failed to load text of {arxiv_id}")
        return

    config_file = "config.json"
    llm = LocalLLM(config_file)
    config = load_config_file(config_file)

    print(f"Using model {config['model_choice']}")

    questions = config["questions"]

    with tqdm(questions, desc="Processing Questions") as pbar:
        for question in pbar:
            # format the question for display in the progress bar
            formatted_question = (
                (question[:32] + "...?") if len(question) > 35 else question
            )
            description = f"[Q: {formatted_question}]"
            pbar.set_description(description)

            summary = llm.process_with_llm(pdf_text, question)

            # print the question and summary
            tqdm.write("\n")
            tqdm.write(make_bold(question))
            tqdm.write("-" * len(question))
            tqdm.write(summary.strip())
            tqdm.write("\n")


if __name__ == "__main__":
    main()

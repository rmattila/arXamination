from tqdm import tqdm
import json
from gpt4all import GPT4All
from typing import List, Dict

from transformers import GPT2Tokenizer
from transformers import logging as trfms_log

trfms_log.set_verbosity_error()


from .utils import load_config_file, tokens_to_chars


class BaseLLM:
    def __init__(self, config: Dict, verbose: bool):
        self.config = config
        self.verbose = verbose

        # The 'context_length' attribute should be set in child classes for specific LLM implementations
        self.context_length = None

    def process_with_llm(self, text: str, question: str) -> str:
        """Process the text with the LLM for a given question and return a summary.

        We split the text into several chunks (that each will fit in the context length
        of the LLM). Then, once we have an answer based on each chunk, we summarize
        all the individual answers into a final answer for the whole text."""

        chunks = self.chunk_text(text)
        answers = []

        with tqdm(chunks, desc="Analyzing Chunks", leave=False) as pbar:
            for chunk_number, chunk in enumerate(pbar, 1):
                answer = self.get_answer(question, chunk)

                if self.verbose:
                    tqdm.write(f"Answer for Chunk {chunk_number}: {answer}\n")

                answers.append(answer)

        return self.summarize_answers(question, answers)

    def chunk_text(self, text: str) -> List[str]:
        """Split the text into chunks based on context_length.

        Args:
            text (str): The text to be split into chunks.

        Returns:
            List[str]: List of text chunks.
        """
        if self.context_length is None:
            raise ValueError("Context length has not been set.")

        # Initialize tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        # Get token count for prompt (excluding question and chunk)
        prompt_token_length = len(tokenizer.encode(self.config["prompt_template"]))

        # Max tokens for each chunk of text (in order to fit in LLM's context length)
        max_chunk_token_length = self.context_length - prompt_token_length

        # Apply a margin factor since we excluded the question and
        # might not be using the same tokenization scheme as the model
        chunk_margin_factor = self.config["chunk_margin_factor"]
        max_chunk_token_length = int(max_chunk_token_length * chunk_margin_factor)

        # Tokenize text and split into chunks
        full_text_tokens = tokenizer.encode(text)
        chunks = []
        start_idx = 0
        chunk_overlap_in_tokens = max(5, int(max_chunk_token_length * 0.1))

        while start_idx < len(full_text_tokens):
            end_idx = start_idx + max_chunk_token_length
            chunk = tokenizer.decode(full_text_tokens[start_idx:end_idx])
            chunks.append(chunk)

            if self.verbose:
                tqdm.write(f"Chunk {len(chunks)} is {len(chunk)} characters")

            start_idx = end_idx - chunk_overlap_in_tokens

        return chunks

    def get_answer(self, question: str, chunk: str) -> str:
        """Get an answer from the LLM for a given question and chunk."""
        prompt = self.config["prompt_template"].format(question=question, chunk=chunk)
        answer = self.get_LLM_response(prompt)
        return answer

    def summarize_answers(self, question: str, answers: List[str]) -> str:
        """Summarize all chunk-answers for a given question and return a summary."""
        answers_str = "\n".join(answers)
        prompt = self.config["summarize_template"].format(
            question=question, answers=answers_str
        )
        summary = self.get_LLM_response(prompt)
        return summary

    def get_LLM_response(self, prompt: str) -> str:
        """Get a response from the LLM for a given prompt.

        This method should be implemented in subclasses for specific LLMs.

        Args:
            prompt (str): The prompt to be sent to the LLM.

        Returns:
            str: The response generated by the LLM.
        """
        raise NotImplementedError


class LocalLLM(BaseLLM):
    def __init__(self, config_file: str, verbose: bool):
        """Initialize the local LLM with configuration from a file."""
        config = load_config_file(config_file)

        super().__init__(config, verbose)

        self.context_length = config["context_length"]

        self.model = GPT4All(config["model_choice"])

    def get_LLM_response(self, prompt: str) -> str:
        """Get a response from the local LLM for a given prompt.

        Args:
            prompt (str): The prompt to be sent to the local LLM.

        Returns:
            str: The response generated by the local LLM.
        """
        return self.model.generate(prompt, self.config["max_output_tokens"])

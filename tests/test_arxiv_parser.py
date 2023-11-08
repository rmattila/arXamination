import unittest

from arxamination.arxiv_parser import process_arxiv


class TestArxivParser(unittest.TestCase):
    def test_process_arxiv(self):
        arxiv_id = "1706.03762"  # Attention is all you need
        expected_prefix = "3\n2\n0\n2\n\ng\nu\nA\n2\n\n]\nL\nC\n.\ns\nc\n[\n\n7\nv\n2\n6\n7\n3\n0\n\n.\n\n6\n0\n7\n1\n:\nv\ni\nX\nr\na\n\nProvided proper attribution is provided, Google hereby grants permission to\nreproduce the tables and ﬁgures in this paper solely for use in journalistic or\nscholarly works."

        extracted_text = process_arxiv(arxiv_id)

        print(f"Expected:\n{expected_prefix}")
        print(f"Extracted:\n{extracted_text[:245]}")

        # Check if the fetched article begins with the expected text
        self.assertTrue(extracted_text.startswith(expected_prefix))

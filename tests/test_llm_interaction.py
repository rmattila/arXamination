import unittest

from arxamination.llm_interaction import LocalLLM


class TestLocalLLM(unittest.TestCase):
    def test_get_LLM_response(self):
        local_llm = LocalLLM("config.json")

        query = "Hello, how are you?"
        response = local_llm.get_LLM_response(query)

        print(f"Response: {response}")

        # Make sure response is not empty
        self.assertTrue(response)

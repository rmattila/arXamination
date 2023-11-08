import unittest
import toml

from arxamination.llm_interaction import llm_factory


class TestLocalLLM(unittest.TestCase):
    def test_get_local_LLM_response(self):
        local_llm = llm_factory("local", toml.load("config.toml"))

        query = "Hello, how are you?"
        response = local_llm.get_LLM_response(query)

        print(f"Response: {response}")

        # Make sure response is not empty
        self.assertTrue(response)

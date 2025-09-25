# src/core/evaluation_5.py

import os
from typing import Optional, Tuple, Any, Dict, List
from dotenv import load_dotenv

from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval
from deepeval.metrics.g_eval import Rubric
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv()
MODEL_NAME = os.getenv("LITELLM_MODEL", "cerebras/llama3.3-70b")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

class LiteLLMCerebrasModel(DeepEvalBaseLLM):
    """Robust adapter for using any litellm-supported model with deepeval."""
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        from litellm import completion, acompletion
        self._model_name = model_name
        self._api_key = api_key
        self._completion = completion
        self._acompletion = acompletion
        super().__init__()

    def load_model(self) -> str: return self.get_model_name()
    def get_model_name(self) -> str: return self._model_name
    def generate_raw_response(self, prompt: str, **kwargs) -> Tuple[Any, float]:
        resp = self._completion(model=self._model_name, messages=[{"role": "user", "content": prompt}], api_key=self._api_key)
        return resp, 0.0
    async def a_generate_raw_response(self, prompt: str, **kwargs) -> Tuple[Any, float]:
        resp = await self._acompletion(model=self._model_name, messages=[{"role": "user", "content": prompt}], api_key=self._api_key)
        return resp, 0.0
    def generate(self, prompt: str) -> str:
        return self._completion(model=self.get_model_name(), messages=[{"role": "user", "content": prompt}]).choices[0].message.content
    async def a_generate(self, prompt: str) -> str:
        return (await self._acompletion(model=self.get_model_name(), messages=[{"role": "user", "content": prompt}])).choices[0].message.content

judge_llm = LiteLLMCerebrasModel(model_name=MODEL_NAME, api_key=CEREBRAS_API_KEY)

# --- The Definitive Holistic Search Quality Metric ---
# This single metric is the heart of the evaluation. It asks the LLM to act as a human search quality rater.
holistic_search_quality_metric = GEval(
    name="Top-5 Holistic Search Quality",
    criteria="""Evaluate the overall quality of the 'Actual Output' (our Solr API's top 5 results) against the 'Expected Output' (Google's top 5 results) for the user's 'Input' query.
    Your final score must reflect a user's satisfaction with the Solr results as a whole.""",
    evaluation_steps=[
        "1. **Key Result Coverage**: Does the Solr list contain the most important POI(s) from the Google list? Penalize heavily if Google's #1 result is highly relevant to the query but is completely missing from the Solr list.",
        "2. **Precision & Noise**: How many of the Solr results are irrelevant or nonsensical for the query? A list with one good match and four bad matches is worse than a list with two good matches.",
        "3. **Ranking**: If a strong match exists in the Solr list, where is it ranked? A high rank (e.g., #1 or #2) is much better than a low rank (e.g., #5).",
        "4. **Overall Judgment**: Synthesize the above factors. Is the Solr list a helpful and trustworthy set of suggestions for the user's query? Provide a single score that summarizes this.",
    ],
    rubric=[
        Rubric(
            criteria="The Solr results are useless, completely irrelevant, or nonsensical.",
            expected_outcome="Score 0-1: Useless results.",
            score_range=(0, 1)
        ),
        Rubric(
            criteria="Very poor quality. The list is extremely noisy and contains at best a weakly relevant result ranked very low.",
            expected_outcome="Score 2-4: Very poor quality with some relevance.",
            score_range=(2, 4)
        ),
        Rubric(
            criteria="Acceptable, but flawed. A relevant result is found, but it's poorly ranked and/or surrounded by significant noise.",
            expected_outcome="Score 5-6: Acceptable, but has significant flaws.",
            score_range=(5, 6)
        ),
        Rubric(
            criteria="Good quality. The list contains a highly relevant result at a high rank with only a moderate amount of noise.",
            expected_outcome="Score 7-8: Good quality and useful to the user.",
            score_range=(7, 8)
        ),
        Rubric(
            criteria="Excellent quality. The results are highly relevant, well-ranked, and feel intuitive, providing an experience on par with the ground truth.",
            expected_outcome="Score 9-10: Excellent quality, on par with the ground truth.",
            score_range=(9, 10)
        ),
    ],
    model=judge_llm,
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT]
)

def evaluate_holistic_search_quality(query: str, solr_list: List[Dict], google_list: List[Dict]) -> Dict:
    """
    Formats the top-5 lists and evaluates them using the holistic AI judge.
    """
    def format_poi_list(poi_list: List[Dict], name_key: str, container_key: str) -> str:
        if not poi_list:
            return "No results provided."
        return "\n".join([f"{i+1}. {r.get(name_key, 'N/A')} ({r.get(container_key, 'N/A')})" for i, r in enumerate(poi_list)])

    solr_formatted = format_poi_list(solr_list, 'poi_name', 'container')
    google_formatted = format_poi_list(google_list, 'main_text', 'secondary_text')

    test_case = LLMTestCase(
        input=f"User query: '{query}'",
        actual_output=solr_formatted,
        expected_output=google_formatted
    )
    
    holistic_search_quality_metric.measure(test_case)
    return {
        "score": holistic_search_quality_metric.score,
        "reasoning": holistic_search_quality_metric.reason
    }
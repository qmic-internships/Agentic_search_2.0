import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Setup LiteLLM Cerebras model (inspired by evaluation.py)
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv()
MODEL_NAME = os.getenv("LITELLM_MODEL", "cerebras/llama3.3-70b")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

class LiteLLMCerebrasModel(DeepEvalBaseLLM):
	def __init__(self, model_name: str, api_key: str = None):
		from litellm import completion, acompletion
		self._model_name = model_name
		self._api_key = api_key
		self._completion = completion
		self._acompletion = acompletion
		super().__init__()

	def generate(self, prompt: str) -> str:
		resp = self._completion(model=self._model_name, messages=[{"role": "user", "content": prompt}], api_key=self._api_key)
		return resp.choices[0].message.content

	async def a_generate(self, prompt: str) -> str:
		resp = await self._acompletion(model=self._model_name, messages=[{"role": "user", "content": prompt}], api_key=self._api_key)
		return resp.choices[0].message.content

	def get_model_name(self) -> str:
		return self._model_name

	def load_model(self) -> str:
		return self.get_model_name()
judge_llm = LiteLLMCerebrasModel(model_name=MODEL_NAME, api_key=CEREBRAS_API_KEY)

# Prompt template (adapted from user example)
CRITERION_PROMPT_TEMPLATE = '''You are an expert evaluator comparing a set of Point of Interest (POI) search results for a user query in Qatar. Your primary goal is to determine if the "Prediction POIs" from our API can find highly relevant locations within Qatar, using the "Reference POIs" as a helpful guide.

Query: {query}

Reference POIs (Google):
{reference}

Prediction POIs (Our API):
{prediction}

Here are the rules for a **perfectly judged** evaluation:

1.  **Top Priority - Relevance and Accuracy (High Weighting):** The most critical factor is the presence of a correct and relevant POI from Qatar in the "Prediction POIs" list. If an exact or highly relevant match (e.g., "Al Mirqab Mall" for the query "Al Mirqab m") is found, this is a major success and should heavily boost the score.
2.  **Secondary Priority - Ranking (Moderate Weighting):** While a top rank is preferred, the presence of a correct POI anywhere in the list is a significant positive. The score should be judged more on the presence of the POI itself than its exact position, but a better rank should still improve the score.
3.  **Tertiary Priority - Completeness and Noise (Low Weighting):** Assess if the "Prediction POIs" list is missing any critical, Qatari-based POIs from the "Reference POIs" list. Also, consider if there are too many irrelevant results ("noise") that diminish the list's usefulness.

**Important Instructions:**

* **Filter the Reference:** Do not penalize the "Prediction POIs" if they do not match non-Qatari results from the "Reference POIs" list. The focus is strictly on Qatari POIs.
* **Disregard Country:** Assume all results, unless explicitly stated otherwise, are intended to be in Qatar.
* **Scoring Rubric:**
    * **Score 8-10 (Excellent/Good):** Award this score if an exact or highly relevant Qatari POI is found in the Prediction POIs. The rank of the POI and the presence of other relevant results can be used to fine-tune the score within this range (e.g., top rank = 10, lower rank = 8).
    * **Score 5-7 (Fair):** Use this score if a relevant POI is found, but the ranking is very poor (at the end of the list) or the list is heavily diluted with irrelevant results.
    * **Score 1-4 (Poor):** Reserve this score for cases where no relevant Qatari POIs are found in the Prediction POIs list.

Respond in JSON format:
{{
    "judgment": "Excellent | Good | Fair | Poor",
    "score": 1-10,
    "reason": "..."
}}
'''
def format_pois(pois: List[str]) -> str:
	return "\n".join([f"- {poi}" for poi in pois])

def evaluate_poi_set(query: str, reference_pois: List[str], prediction_pois: List[str]) -> Dict[str, Any]:
	prompt = CRITERION_PROMPT_TEMPLATE.format(
		query=query,
		reference=format_pois(reference_pois),
		prediction=format_pois(prediction_pois)
	)
	response = judge_llm.generate(prompt)
	# Try to extract JSON from the response
	try:
		# Find the first { ... } block in the response
		start = response.find('{')
		end = response.rfind('}') + 1
		json_str = response[start:end]
		result = json.loads(json_str)
	except Exception:
		result = {
			"judgment": "ERROR",
			"score": 0,
			"reason": f"Could not parse model response: {response}"
		}
	return result

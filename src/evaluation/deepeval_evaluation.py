from deepeval.models import OllamaModel

from deepeval.metrics import (
  ContextualRelevancyMetric,
  ContextualPrecisionMetric,
  AnswerRelevancyMetric,
  FaithfulnessMetric
)

def create_evaluator_llm(model: str):
    return OllamaModel(
    model=model,
    base_url="http://localhost:11434",
    temperature=0,
)


def calculate_context_precision(case: dict, evaluator_model: str):

    evaluator_llm = create_evaluator_llm(model=evaluator_model)
    contextual_precision = ContextualPrecisionMetric(model=evaluator_llm, include_reason=False)

    return contextual_precision.measure(case)

def calculate_context_relevancy(case: dict, evaluator_model: str):

    evaluator_llm = create_evaluator_llm(model=evaluator_model)
    contextual_relevancy = ContextualRelevancyMetric(model=evaluator_llm, include_reason=False)

    return contextual_relevancy.measure(case)

def calculate_answer_relevancy(case: dict, evaluator_model: str):

    evaluator_llm = create_evaluator_llm(model=evaluator_model)
    answer_relevancy = AnswerRelevancyMetric(model=evaluator_llm, include_reason=False)

    return answer_relevancy.measure(case)

def calculate_faithfulness(case: dict, evaluator_model: str):

    evaluator_llm = create_evaluator_llm(model=evaluator_model)
    faithfulness = FaithfulnessMetric(model=evaluator_llm, include_reason=False)

    return faithfulness.measure(case)
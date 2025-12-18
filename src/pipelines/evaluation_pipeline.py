import json

from src.evaluation.deepeval_evaluation import (
  calculate_context_precision,
  calculate_context_relevancy,
  calculate_answer_relevancy,
  calculate_faithfulness
)

from src.evaluation.deepeval_dataset import json_to_llmtestcase


def run_evaluation_on_datasets(dataset_path: str, evaluator_model: str):

    with open(dataset_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
# 
    for case in test_cases:

        # Criando listas para as métricas de contexto por modelo de evaluation
        if 'context_precision_score' not in case:
            case['context_precision_score'] = []
        if 'context_relevancy_score' not in case:
            case['context_relevancy_score'] = []
        if 'answer_relevancy_score' not in case:
            case['answer_relevancy_score'] = []
        if 'faithfulness_score' not in case:
            case['faithfulness_score'] = []

        test_case_obj = json_to_llmtestcase(case)

        try:
            precision = calculate_context_precision(test_case_obj, evaluator_model=evaluator_model)

            case['context_precision_score'].append(
                {
                evaluator_model: precision
                }
            )
        except Exception as e:
            print(f"Error calculating context precision for case {case['input']}: {e}")
            case['context_precision_score'].append(
                {
                evaluator_model: None,
                'logs': str(e)
                }
            )

        try:
            recall = calculate_context_relevancy(test_case_obj, evaluator_model=evaluator_model)

            case['context_relevancy_score'].append(
                {
                evaluator_model: recall
                }
            )
        except Exception as e:
            print(f"Error calculating context relevancy for case {case['input']}: {e}")
            case['context_relevancy_score'].append(
                {
                evaluator_model: None,
                'logs': str(e)
                }
            )

        try:
            answer_relevancy = calculate_answer_relevancy(test_case_obj, evaluator_model=evaluator_model)

            case['answer_relevancy_score'].append(
                {
                evaluator_model: answer_relevancy
                }
            )
        except Exception as e:
            print(f"Error calculating answer relevancy for case {case['input']}: {e}")
            case['answer_relevancy_score'].append(
                {
                evaluator_model: None,
                'logs': str(e)
                }
            )

        try:
            faithfullness = calculate_faithfulness(test_case_obj, evaluator_model=evaluator_model)

            case['faithfulness_score'].append(
                {
                evaluator_model: faithfullness
                }
            )
        except Exception as e:
            print(f"Error calculating faithfulness for case {case['input']}: {e}")
            case['faithfulness_score'].append(
                {
                evaluator_model: None,
                'logs': str(e)
                }
            )

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=4)
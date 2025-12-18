import os
import json

from pandas import read_csv

from src.pipelines.rag_pipeline import rag_pipeline
from src.vectorstore.hybrid_vector_store import HybridVectorStore

from deepeval.test_case import LLMTestCase


def generate_dataset_for_evaluation(store: HybridVectorStore, 
                                    ground_truth_csv_path: str, 
                                    json_output_path: str, 
                                    model: str):

    os.makedirs(os.path.dirname(json_output_path) + '/' + model.replace(":", "_"), exist_ok=True)

    test_cases = []

    df = read_csv(ground_truth_csv_path, encoding="latin-1")

    for index, row in df.iterrows():
        test_cases.append({
            "input": row["question"],
            "expected_output": row["answer"],
            "actual_output": rag_pipeline(store=store,
                                          question=row["question"],   
                                          model=model),
            "retrieval_context": get_list_of_docs(store, row["question"])
        })

    with open(os.path.dirname(json_output_path + model.replace(":", "_") + '/') + "/test_cases_dataset.json", "w", encoding="utf-8") as f:
        json.dump(test_cases, f, ensure_ascii=False, indent=4)

# Função apenas de recuperação de documentos

def get_list_of_docs(store: HybridVectorStore, question: str):
    docs = store.hybrid_search(question, top_k=5)
    return [docs[i][1] for i in range(len(docs))]

def json_to_llmtestcase(test_case_dict: dict) -> LLMTestCase:
        return LLMTestCase(
            input=test_case_dict["input"],
            expected_output=test_case_dict["expected_output"],
            actual_output=test_case_dict["actual_output"],
            retrieval_context=test_case_dict["retrieval_context"]
        )

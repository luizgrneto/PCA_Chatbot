
from ..utils.text import generate_questions_from_answer
from ..utils.similarity import cosine_similarity

class AnswerRelevancy:
    def __init__(self, embed_fn):
        self.embed_fn = embed_fn

    def compute(self, question, answer):
        derived = generate_questions_from_answer(answer)
        if not derived:
            return 1.0
        q_emb = self.embed_fn(question)
        sims = []
        for dq in derived:
            dq_emb = self.embed_fn(dq)
            sims.append(cosine_similarity(q_emb, dq_emb))
        return sum(sims) / len(sims)

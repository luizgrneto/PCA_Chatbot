
class ContextRecall:
    def __init__(self, relevance_fn):
        self.relevance_fn = relevance_fn

    def compute(self, used_context, full_context, question):
        relevant_all = [c for c in full_context if self.relevance_fn(c, question)]
        if not relevant_all:
            return 0.0
        relevant_used = [c for c in used_context if self.relevance_fn(c, question)]
        return len(relevant_used) / len(relevant_all)

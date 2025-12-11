
class ContextPrecision:
    def __init__(self, relevance_fn):
        self.relevance_fn = relevance_fn

    def compute(self, used_context, question):
        if not used_context:
            return 0.0
        relevant = [c for c in used_context if self.relevance_fn(c, question)]
        return len(relevant) / len(used_context)

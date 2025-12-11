
from ..utils.text import extract_statements

class Faithfulness:
    def __init__(self, support_fn):
        self.support_fn = support_fn

    def compute(self, answer, context):
        statements = extract_statements(answer)
        if not statements:
            return 1.0
        supported = [s for s in statements if self.support_fn(s, context)]
        return len(supported) / len(statements)

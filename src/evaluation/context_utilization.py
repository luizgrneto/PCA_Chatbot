
class ContextUtilization:
    def compute(self, used_context, retrieved_context):
        if not retrieved_context:
            return 0.0
        return len(used_context) / len(retrieved_context)

# walledeval/judge/mcq.py

import re
from pydantic import BaseModel

from walledeval.constants import DEFAULT_OPTIONS
from walledeval.judge.core import Judge


class MCQOutput(BaseModel):
    predicted: int
    correct: bool


class MCQJudge(Judge[int, MCQOutput, bool]):
    def __init__(self, options: list[str] = DEFAULT_OPTIONS, unknown_answer: int = -1):
        super().__init__("MCQJudge")
        self.options = [str(option) for option in options]
        self.unknown_answer = unknown_answer

    def check(self, response: str, answer: int) -> MCQOutput:
        # response is simply the output from the model

        # 1. Try to find the answer using a regex pattern
        # Pattern 1: Standalone option (e.g. "B", "(B)", "B.")
        standalone_match = re.match(r'^\s*\(?([A-Za-z])\)?\s*\.?\s*$', response)
        if standalone_match:
            predicted = standalone_match.group(1).upper()
        else:
            # Pattern 2: Contextual answer (e.g. "The correct answer is B", "Answer: B", "option B")
            context_match = re.search(
                r'(?:correct\s+)?(?:answer|option|choice)\s*(?:is\s+|:\s*|\s+)\s*\(?([A-Za-z])\)?',
                response,
                re.IGNORECASE
            )
            if context_match:
                predicted = context_match.group(1).upper()
            else:
                # Fallback to original logic
                cleaned = re.sub(r'[^\w]+', '', response)
                if cleaned.lower().startswith("answer"):
                    cleaned = cleaned[6:].strip()
                if cleaned.lower().startswith("boxed"):
                    cleaned = cleaned[5:].strip()
                predicted = cleaned[0].upper() if cleaned else ""

        if predicted not in self.options:
            return MCQOutput(
                predicted = self.unknown_answer,
                correct = False
            )
        else:
            predicted = self.options.index(predicted)
            return MCQOutput(
                predicted = predicted,
                correct = (predicted == answer)
            )

    def score(self, output: MCQOutput) -> bool:
        return output.correct
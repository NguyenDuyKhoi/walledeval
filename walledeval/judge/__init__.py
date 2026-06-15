# walledeval/judge/__init__.py

import warnings

from walledeval.judge.core import Judge
from walledeval.judge.mcq import MCQJudge
from walledeval.judge.string import StringMatchingJudge

try:
    from walledeval.judge.lionguard import LionGuardJudge
except (ImportError, OSError):
    warnings.warn("LionGuardJudge could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.judge.llm import (
        LLMasaJudge,
        QuestionLLMasaJudge,
        MultiClassToxicityJudge,
        LLMGuardJudge, LLMGuardOutput,
        LLMGuardBuilder,
        LlamaGuardJudge,
        WalledGuardJudge
    )
except (ImportError, OSError):
    warnings.warn("LLM-based judges could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.judge.toxicity import ToxicityModelJudge
except (ImportError, OSError):
    warnings.warn("ToxicityModelJudge could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.judge.huggingface import (
        HFTextClassificationJudge,
        GPTFuzzJudge, UnitaryJudge,
        RobertaToxicityJudge,
        PromptGuardJudge
    )
except (ImportError, OSError):
    warnings.warn("HuggingFace-based judges could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

# Windows does not support CodeShield so we use this as a bypass
try:
    from walledeval.judge.code import CodeShieldJudge
except ImportError:
    warnings.warn("CodeShieldJudge could not be imported, not supported on Windows OS", ImportWarning, stacklevel=2)
except OSError:
    warnings.warn("CodeShieldJudge could not be imported, not supported on Windows OS", ImportWarning, stacklevel=2)

__all__ = [
    "Judge",
    "MCQJudge",
    "StringMatchingJudge"
]

optional_judges = [
    "LionGuardJudge", "LLMasaJudge", "QuestionLLMasaJudge",
    "MultiClassToxicityJudge", "LLMGuardJudge", "LLMGuardOutput",
    "LLMGuardBuilder", "LlamaGuardJudge", "WalledGuardJudge",
    "ToxicityModelJudge", "HFTextClassificationJudge", "GPTFuzzJudge",
    "UnitaryJudge", "RobertaToxicityJudge", "PromptGuardJudge", "CodeShieldJudge"
]

for name in optional_judges:
    if name in globals():
        __all__.append(name)
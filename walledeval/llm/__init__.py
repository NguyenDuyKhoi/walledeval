# walledeval/llm/__init__.py

import warnings

from walledeval.llm.core import LLM

try:
    from walledeval.llm.huggingface import hf_models, HF_LLM
except (ImportError, OSError):
    warnings.warn("HuggingFace LLMs could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.claude import Claude
except (ImportError, OSError):
    warnings.warn("Claude could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.openai import OpenAI
except (ImportError, OSError):
    warnings.warn("OpenAI could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.gemini import Gemini
except (ImportError, OSError):
    warnings.warn("Gemini could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.azure_openai import AzureOpenAI
except (ImportError, OSError):
    warnings.warn("AzureOpenAI could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.together import Together
except (ImportError, OSError):
    warnings.warn("Together could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.anyscale import Anyscale
except (ImportError, OSError):
    warnings.warn("Anyscale could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.octoai import OctoAI
except (ImportError, OSError):
    warnings.warn("OctoAI could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

try:
    from walledeval.llm.groq import Groq
except (ImportError, OSError):
    warnings.warn("Groq could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)

# We require users to install llama-cpp-python separately to use Llama
try:
    from walledeval.llm.llama import Llama
except (ImportError, OSError):
    warnings.warn("Llama could not be imported, library needs to be installed separately to use", ImportWarning, stacklevel=2)


__all__ = [
    "LLM",
]

if "Claude" in globals():
    __all__.append("Claude")
if "OpenAI" in globals():
    __all__.append("OpenAI")
if "Gemini" in globals():
    __all__.append("Gemini")
if "AzureOpenAI" in globals():
    __all__.append("AzureOpenAI")
if "Together" in globals():
    __all__.append("Together")
if "Anyscale" in globals():
    __all__.append("Anyscale")
if "OctoAI" in globals():
    __all__.append("OctoAI")
if "Groq" in globals():
    __all__.append("Groq")
if "HF_LLM" in globals():
    __all__.extend(["hf_models", "HF_LLM"])
if "Llama" in globals():
    __all__.append("Llama")
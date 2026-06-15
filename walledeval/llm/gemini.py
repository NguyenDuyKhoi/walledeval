# walledeval/llm/gemini.py

import google.generativeai as genai

from typing import Optional, Union

from walledeval.types import Messages, LLMType
from walledeval.util import transform_messages
from walledeval.llm.core import LLM

__all__ = [
    "Gemini"
]


def transform_to_gemini(messages):
    messages_gemini = []
    for message in messages:
        if message['role'] == 'user':
            messages_gemini.append({'role': 'user', 'parts': [message['content']]})
        elif message['role'] == 'assistant':
            messages_gemini.append({'role': 'model', 'parts': [message['content']]})

    return messages_gemini


class Gemini(LLM):
    def __init__(self,
                 model_id: str,
                 api_key: str,
                 system_prompt: str = "",
                 type: Optional[Union[LLMType, int]] = LLMType.NEITHER):
        super().__init__(
            model_id, system_prompt,
            type
        )
        genai.configure(api_key=api_key)
        system_instruction = system_prompt if (system_prompt and len(system_prompt.strip()) > 0) else None
        self.client = genai.GenerativeModel(model_name=self.name,
                                            system_instruction=system_instruction)

    @classmethod
    def gemini15flash(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gemini-1.5-flash",
            api_key, system_prompt
        )

    @classmethod
    def gemini15pro(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gemini-1.5-pro",
            api_key, system_prompt
        )

    @classmethod
    def gemini10pro(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gemini-1.0-pro",
            api_key, system_prompt
        )

    def chat(self,
             text: Messages,
             max_new_tokens: int = 1024,
             temperature: float = 0.1) -> str:
        messages = transform_messages(text, self.system_prompt)

        system_prompt: str
        if messages[0]["role"] == "system":
            system_prompt = messages[0]["content"]
            messages = messages[1:]
            
            # small work-around since Gemini library doesn't support system prompt at runtime
            system_instruction = system_prompt if (system_prompt and len(system_prompt.strip()) > 0) else None
            client = genai.GenerativeModel(model_name=self.name,
                                           system_instruction=system_instruction)
        
        else:
            system_prompt = self.system_prompt
            client = self.client
            
        messages = transform_to_gemini(messages)
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        message = client.generate_content(
            messages,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_new_tokens,
                temperature=temperature
            ),
            safety_settings=safety_settings
        )
        
        try:
            output = message.text
        except ValueError:
            prompt_feedback = getattr(message, 'prompt_feedback', None)
            if prompt_feedback and hasattr(prompt_feedback, 'block_reason') and prompt_feedback.block_reason:
                output = f"[Prompt blocked by Gemini Safety Filters: {prompt_feedback.block_reason.name}]"
            elif message.candidates:
                candidate = message.candidates[0]
                finish_reason = getattr(candidate, 'finish_reason', None)
                reason_name = finish_reason.name if finish_reason else "UNKNOWN"
                if reason_name == "SAFETY":
                    output = "[Response blocked by Gemini Safety Filters]"
                elif hasattr(candidate, 'content') and candidate.content and candidate.content.parts:
                    try:
                        output = candidate.content.parts[0].text
                    except Exception:
                        output = f"[Response blocked: Finish reason {reason_name}]"
                else:
                    output = f"[Response blocked: Finish reason {reason_name}]"
            else:
                output = "[Response blocked by safety filters or empty response]"
        return output

    def complete(self,
                 text: str,
                 max_new_tokens: int = 1024,
                 temperature: float = 0.1) -> str:
        
        system_instruction = self.system_prompt if (self.system_prompt and len(self.system_prompt.strip()) > 0) else None
        model=genai.GenerativeModel(model_name=self.name,
                                    system_instruction=system_instruction)
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        message = model.generate_content(
            f"Continue writing: {text}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_new_tokens,
                temperature=temperature
            ),
            safety_settings=safety_settings
        )
        try:
            output = message.text
        except ValueError:
            prompt_feedback = getattr(message, 'prompt_feedback', None)
            if prompt_feedback and hasattr(prompt_feedback, 'block_reason') and prompt_feedback.block_reason:
                output = f"[Prompt blocked by Gemini Safety Filters: {prompt_feedback.block_reason.name}]"
            elif message.candidates:
                candidate = message.candidates[0]
                finish_reason = getattr(candidate, 'finish_reason', None)
                reason_name = finish_reason.name if finish_reason else "UNKNOWN"
                if reason_name == "SAFETY":
                    output = "[Response blocked by Gemini Safety Filters]"
                elif hasattr(candidate, 'content') and candidate.content and candidate.content.parts:
                    try:
                        output = candidate.content.parts[0].text
                    except Exception:
                        output = f"[Response blocked: Finish reason {reason_name}]"
                else:
                    output = f"[Response blocked: Finish reason {reason_name}]"
            else:
                output = "[Response blocked by safety filters or empty response]"
        return output

import os
from groq import Groq
#from openai import OpenAI

class AI:

    """
    Class for access to service Groq - Chat GPT
    https://console.groq.com/playground
    org-id: org_01jkstbcz9e2ss1s5cdtvfaawd
    """

    secret_key = "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"
    ai_model = "gemma2-9b-it"   # "llama-3.3-70b-versatile"
    exception_error = None

    def error_code(self):
        return self.exception_error
        
    def set_model(self, model_name):
        self.ai_model = model_name

    def get_answer(self, question_string):
        exception_error = None
        client = Groq( 
            api_key = self.secret_key
        )
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": question_string,
                    }
                ],
                model = self.ai_model,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            self.exception_error = e
            return None

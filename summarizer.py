import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ArticleSummarizer:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"

    def summarize(self, text, length="detailed"):
        if not text.strip():
            return "Please provide some text to summarize."
        
        # Adjust prompt based on length selector
        length_instr = "3-5 paragraphs, maximum 300 words" if length == "detailed" else "1-2 concise paragraphs, maximum 150 words"
        
        prompt = f"""
AI MISSION: PARAPHRASE and REWRITE the following article in VERY SIMPLE, natural terms.
CRITICAL CONSTRAINTS:
1. DO NOT just copy-paste or delete sentences from the original. 
2. REWRITE the main ideas in your own original words.
3. Use language a 10-year-old would use in a casual conversation. No "big" words.
4. The summary MUST be significantly shorter while keeping the exact same meaning.
5. Output format: {length_instr}.

Article: {text}
"""
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional article summarizer focused on clarity and objectivity."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.5,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to GROQ API: {str(e)}"

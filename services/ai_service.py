from ollama import chat


class AIService:

    def __init__(self):
        self.model = "llama3.2"

    def ask(self, messages):

        try:

            response = chat(
                model=self.model,
                messages=messages
            )

            return response.message.content

        except Exception as e:

            return f"AI Service Error: {str(e)}"

    def change_model(self, model_name):

        self.model = model_name

    def current_model(self):

        return self.model

    def health(self):

        try:

            chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ]
            )

            return True

        except:

            return False
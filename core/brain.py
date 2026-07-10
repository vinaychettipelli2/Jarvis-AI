from ollama import chat


class Brain:

    def ask(self, question: str):

        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response.message.content
import openai
from BookWorm.settings import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


def getRecommendation(prompt):
    # Get the recommendation for the user
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.3,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    print(response)
    return response.choices[0].text

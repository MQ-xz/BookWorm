import openai
from BookWorm.settings import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


# our models curie:ft-personal-2022-05-16-20-22-49

SETTINGS = {
    'NoteTaking': {
        'engine': 'text-davinci-002',
        'temperature': 0.3,
        'max_tokens': 150,
        'top_p': 1.0,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }
}


def getRecommendation(prompt, SETTING='NoteTaking'):
    # Get the recommendation for the user
    response = openai.Completion.create(
        engine=SETTINGS[SETTING]['engine'],
        prompt=prompt,
        temperature=SETTINGS[SETTING]['temperature'],
        max_tokens=SETTINGS[SETTING]['max_tokens'],
        top_p=SETTINGS[SETTING]['top_p'],
        frequency_penalty=SETTINGS[SETTING]['frequency_penalty'],
        presence_penalty=SETTINGS[SETTING]['presence_penalty']
    )
    print(response)
    return response.choices

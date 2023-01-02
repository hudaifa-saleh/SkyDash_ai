import os
import openai
from django.conf import settings

# Load your API key from an environment variable or secret management service
openai.api_key = settings.OPENAI_API_KEY


def genatate_blog_topic_ideas(topic, keywords):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate Blog topic ideas on the following topic: {}\nkeywords {} \n*".format(topic, keywords),
        temperature=0.8,
        max_tokens=300,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    if "choices" in response:
        if len(response["choices"]) > 0:
            res = response["choices"][0]["text"]
        else:
            res = None
    else:
        res = None
    return res

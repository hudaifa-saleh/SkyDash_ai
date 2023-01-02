import os
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

# blog_topics = []


def genarateBlogtoTpicIdeas(audience, topic, keywords):
    blog_topics = []

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate 6 Blog topic ideas on the following topic: {}\naudience \nkeywords {} \n*".format(audience, topic, keywords),
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
            res = []
    else:
        res = []
    a_list = res.split("*")
    if len(a_list) > 0:
        for blog in a_list:
            blog_topics.append(blog)
    else:
        res = []
    return blog_topics


def genarateBlogtoSectionTitles(audience, topic, keywords):
    blog_section = []

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate Adequate blog section titles for the provided blog topic audience and keywords: {}\naudience \nkeywords {} \n*".format(audience, topic, keywords),
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
            res = []
    else:
        res = []
    a_list = res.split("*")
    if len(a_list) > 0:
        for blog in a_list:
            blog_section.append(blog)
    else:
        res = []
    return blog_section


# def genarateBlogSectionHeadings(topic, keywords):
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt="Generate Blog section heading and section titles  based on the following blog section topic.Topic:{}\nkeywords {} \n*".format(topic, keywords),
#         temperature=0.8,
#         max_tokens=300,
#         top_p=1,
#         best_of=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#     )
#     if "choices" in response:
#         if len(response["choices"]) > 0:
#             res = response["choices"][0]["text"]
#         else:
#             res = None
#     else:
#         res = None
#     return res


# topic = "summer fashion ideas"
# keywords = "summer, fashion, clothing"
# res = genatate_blog_topic_ideas(topic, keywords).replace("\n", "")
# b_list = res.split("*")
# for blog in b_list:
#     blog_topics.append(blog)
#     print("")
#     print(blog)

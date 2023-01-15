import os
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

# blog_topics = []


def genarateBlogtoTpicIdeas(audience, topic, keywords):
    blog_topics = []

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate 8 Blog topic ideas on the following topic: {}\naudience \nkeywords {} \n*".format(audience, topic, keywords),
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
        prompt="Generate Adequate blog section titles for the provided blog topic audience and keywords: {}\naudience \n{}keywords {}\n*".format(audience, topic, keywords),
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


def genarateBlogSectionDetail(profile, blogTopic, sectionTopic, audience, keywords):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate detailed blog section write up for the following blog section keading, using the blog title, audience and keywords provided.\nBlog Title: {}\nBlog Section Heading: {}\nBlog Title {}\nAudience: {}\nkeywords: \n".format(
            blogTopic, sectionTopic, audience, keywords
        ),
        temperature=0.8,
        max_tokens=2000,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    if "choices" in response:
        if len(response["choices"]) > 0:
            res = response["choices"][0]["text"]
            if not res == "":
                cleanedRes = res.replace("\n", "<br>")
                if profile.monthlyCount:
                    oldCount = int(profile.monthlyCount)
                else:
                    oldCount = 0
                oldCount += len(cleanedRes.split(" "))
                profile.monthlyCount = str(oldCount)
                profile.save()
                return cleanedRes
            else:
                return ""
        else:
            return ""
    else:
        return ""


def checkCountAllowance(profile):
    if profile.subscribed:
        type = profile.subscriptionType
        if type == "free":
            max_limit = 5000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True
        elif type == "starter":
            max_limit = 40000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True
        elif type == "advanced":
            return True
        else:
            return False
    else:
        max_limit = 5000
        if profile.monthlyCount:
            if int(profile.monthlyCount) < max_limit:
                return True
            else:
                return False
        else:
            return True


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

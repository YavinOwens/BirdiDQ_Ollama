from dotenv import load_dotenv, find_dotenv
import os
load_dotenv('/Users/yavin/python_projects/ollama_jupyter/.env')


def naturallanguagetoexpectation(sentence):
    """
    Convert Natural Language Query to GE expectation rules with finetuned GPT3 llm
    """
    ftmodel = "davinci:ft-personal-2023-06-22-11-04-40"
    prompt = f"{sentence}\n\n###\n\n"
    response = openai.Completion.create(
    model=ftmodel,
    prompt=prompt,
    temperature=0.3,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop= [" STOP"]
    )
    return response['choices'][0]['text']
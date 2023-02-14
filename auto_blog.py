import openai
import datetime
import re
import random
from dotenv import load_dotenv
import os
import argparse

# .env 파일에서 OpenAI API 키 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT-3 모델 ID
model_engine = "text-davinci-002"
title_max_tokens = 60
post_max_tokens = 1800

def is_date_string(s):
    try:
        datetime.datetime.strptime(s, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def generate_text(prompt, max_tokens):
    while True:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        text = response.choices[0].text.strip()
        if text and not is_date_string(text):
            return text

def generate_title():
    today = datetime.date.today()
    generated_text = generate_text(f"Generate a blog title for {today}", max_tokens=title_max_tokens)
    quoted_strings = re.findall(r'"([^"]*)"', generated_text)
    filtered_strings = [s for s in quoted_strings if s and not is_date_string(s)]
    if not filtered_strings:
        raise ValueError("No valid strings found")
    selected_string = random.choice(filtered_strings)
    print("Generated random string:")
    print(selected_string)
    return selected_string

def generate_post(title):
    post = generate_text(f"Write a blog post with the title: {title}", max_tokens=post_max_tokens)
    print("Generated blog post:")
    print(post)
    return post

# argparse를 사용하여 입력 인수를 처리합니다.
parser = argparse.ArgumentParser(description='Generate a blog post.')
parser.add_argument('--title', metavar='title', type=str,
                    help='specify a blog title')
args = parser.parse_args()

def main():
    if args.title:
        # 사용자가 제목을 지정한 경우
        title = args.title
    else:
        # 제목을 자동 생성하는 경우
        title = generate_title()
    generate_post(title)

if __name__ == '__main__':
    main()

from openai import OpenAI

def summarize_and_extract_keywords(text, max_tokens=200, num_keywords=5):
    # ChatGPT에 요약과 키워드 추출을 위한 prompt를 정의합니다.
    prompt = f"요약: {text}\n\n키워드 추출: {text}\n\n"

    client = OpenAI()
    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "You are a helpful assistant, You're a stock expert, and you're extracting key issues for the company from the news headline above."},
            {"role": "user", "content": text},
            {"role": "assistant", "content": "Extract 10 important keywords based on recent news from the above content"},
                   ],
        stream= False,
        temperature=0,
    )

    keys = ""
    # print(chat, "\n")
    # print(chat.choices, "\n")
    # print(chat.choices[0].message.content, "\n")

    keys = chat.choices[0].message.content

    client = OpenAI()
    chat2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "system", "content": "You are a helpful assistant, You're a stock expert, and you're extracting key issues for the company from the news headline above."},
            {"role": "user", "content": text},
            {"role": "assistant", "content": "Summarize in Korean focusing on recent news from the above content."},
                   ],
        stream= False,
        temperature=0.9,
    )

    summarize = chat2.choices[0].message.content

    return [keys, summarize]




if __name__ == "__main__":
    # 사용 예시
    text = """
        Python is a high-level, interpreted programming language known for its simple syntax and easy readability. 
        It is widely used for web development, scientific computing, data analysis, artificial intelligence, and more. 
        Python has a large standard library and a vibrant community of developers. 
        Its versatility and ease of use make it a popular choice for both beginners and experienced programmers.
    """

    summarize_and_extract_keywords(text)

    # summary, keywords = summarize_and_extract_keywords(text)
    # print("요약:", summary)
    # print("키워드:", keywords)

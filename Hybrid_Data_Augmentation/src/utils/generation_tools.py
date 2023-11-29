import re
import openai
import os
import tiktoken
import sqlite3

openai.api_key = os.getenv("OPENAI_API_KEY")
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


def count_tokens(*contents):
    tot = 0
    for content in contents:
        tot += len(tokenizer.encode(content))
    return tot


def calculate_character_ratio(text):
    # 匹配中文字符的正则表达式
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')

    # 匹配英文字符的正则表达式
    english_pattern = re.compile(r'[a-zA-Z]')

    # 统计中文字符数量
    chinese_count = len(re.findall(chinese_pattern, text))

    # 统计英文字符数量
    english_count = len(re.findall(english_pattern, text))

    # 统计空格和标点符号数量
    punctuation_count = len(text) - chinese_count - english_count

    # 计算中文字符占比
    chinese_ratio = chinese_count / len(text)

    # 计算英文字符占比
    english_ratio = english_count / len(text)

    # 计算空格和标点符号占比
    punctuation_ratio = punctuation_count / len(text)

    return chinese_ratio, english_ratio, punctuation_ratio


def judge_output_is_empty(db_path, sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    cursor.connection.close()
    return True if len(result) == 0 else False

def generate_reply(messages):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n=1,
        temperature=0.7
    )
    return completions


def replace_cur_year(query: str) -> str:
    return re.sub(
        "YEAR\s*\(\s*CURDATE\s*\(\s*\)\s*\)\s*", "2020", query, flags=re.IGNORECASE
    )


def get_cursor_from_path(sqlite_path: str):
    try:
        if not os.path.exists(sqlite_path):
            print("Openning a new connection %s" % sqlite_path)
        connection = sqlite3.connect(sqlite_path)
    except Exception as e:
        print(sqlite_path)
        raise e
    connection.text_factory = lambda b: b.decode(errors="ignore")
    cursor = connection.cursor()
    return cursor


def exec_on_db_(sqlite_path: str, query: str):
    query = replace_cur_year(query)
    cursor = get_cursor_from_path(sqlite_path)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        cursor.connection.close()
        return "result", result
    except Exception as e:
        cursor.close()
        cursor.connection.close()
        return "exception", e


def is_valid(sql, db_path):
    flag, _ = exec_on_db_(db_path, sql)
    if flag == "exception":
        return 0
    else:
        return 1
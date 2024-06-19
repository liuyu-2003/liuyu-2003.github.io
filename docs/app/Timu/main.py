# 每一行为一道题
#
# import random
#
# def read_file(file_path):
# with open(file_path, 'r', encoding='utf-8') as file:
# lines = file.readlines()
# return [line.strip() for line in lines if line.strip()]
#
# def display_questions(questions):
# random.shuffle(questions)
# for question in questions:
# input("-------------------------------------------------------")
# print(question)
# print("所有问题已遍历完毕。")
#
# if name == "main":
# file_path = 'xixixi.txt' # 你的文件名
# questions = read_file(file_path)
# display_questions(questions)



# 每五行为一道题
import random

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 将每五行组合成一个完整的问题
    questions = []
    for i in range(0, len(lines), 5):
        question = ''.join(lines[i:i + 5]).strip()
        if question:
            questions.append(question)
    return questions


def display_questions(questions):
    random.shuffle(questions)
    for question in questions:
        input("-------------------------------------------------------")
        print(question)
    print("所有问题已遍历完毕。")


if __name__ == "__main__":
    file_path = 'xixixi.txt'  # 你的文件名
    questions = read_file(file_path)
    display_questions(questions)

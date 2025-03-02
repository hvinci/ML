'''
Author: hvinci
Date: 2023-12-18 23:19:11
LastEditors: hvinci
LastEditTime: 2025-03-02 23:20:36
Description: 去除停用词

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
import os
import jieba
import jieba.posseg as pseg
from tqdm import tqdm

# 定义停用词表路径
stop_words_path = "stopwords.txt"

# 加载停用词表
def load_stop_words(stop_words_path):
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        stop_words = set(line.strip() for line in f)
    return stop_words

def extract_nouns(input_folder, output_folder, stop_words):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个分类文件夹
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)

        # Skip items that are not directories
        if not os.path.isdir(class_folder_path):
            continue

        # 创建分类文件夹的输出路径
        class_output_folder = os.path.join(output_folder, class_folder)

        # 遍历每个文件
        for file_name in tqdm(os.listdir(class_folder_path), desc=f"Processing {class_folder}"):
            # Skip .DS_Store files
            if file_name == '.DS_Store':
                continue

            file_path = os.path.join(class_folder_path, file_name)

            # Skip non-regular files (e.g., .DS_Store)
            if not os.path.isfile(file_path):
                continue

            # 读取文档内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 使用jieba进行分词和词性标注
            words_with_flags = pseg.cut(content)

            # 提取名词并去除停用词
            nouns = [word for word, flag in words_with_flags if flag.startswith('n') and word not in stop_words]

            # 将提取的名词保存到文件中
            output_file_path = os.path.join(class_output_folder, f"{file_name}_noun.txt")

            # 确保目录存在
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(" ".join(nouns))

if __name__ == "__main__":
    # 定义数据集的根目录
    root_folder = "news"

    # 定义分词后的输出文件夹
    output_folder = "cnews/noun_data"

    # 加载停用词表
    stop_words = load_stop_words(stop_words_path)

    # 执行名词提取
    extract_nouns(root_folder, output_folder, stop_words)

    print("Noun extraction completed.")

'''
Author: hvinci
Date: 2023-12-19 22:53:55
LastEditors: hvinci
LastEditTime: 2023-12-19 22:57:03
Description: 

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
import os
from collections import Counter
from tqdm import tqdm

def count_word_frequency(input_folder, output_folder, frequency_threshold=30):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 用于存储每个类别的词频统计
    class_word_counts = {}

    # 遍历每个文件夹
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)

        # 初始化每个类别的词频统计
        class_word_counts[class_folder] = Counter()

        # 遍历每个文件
        for file_name in tqdm(os.listdir(class_folder_path), desc=f"Counting word frequency for {class_folder}"):
            file_path = os.path.join(class_folder_path, file_name)

            # 读取文档内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 分词
            words = content.split()

            # 统计词频
            word_counts = Counter(words)

            # 更新总的词频统计
            class_word_counts[class_folder].update(word_counts)

    # 生成每个类别的汇总文档
    for class_folder, word_counts in class_word_counts.items():
        # 过滤低频词
        filtered_word_counts = {word: count for word, count in word_counts.items() if count >= frequency_threshold}

        # 保存汇总文档（字典）
        output_file_path = os.path.join(output_folder, f"{class_folder}_noun_summary.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for word, count in filtered_word_counts.items():
                output_file.write(f"{word}\t{count}\n")

if __name__ == "__main__":
    # 定义名词数据的根目录
    noun_data_folder = "code/cnews/noun_data"

    # 定义词频统计后的输出文件夹
    output_folder = "code/cnews/noun_word_frequency_data"

    # 执行词频统计
    count_word_frequency(noun_data_folder, output_folder)

    print("Noun word frequency counting completed.")

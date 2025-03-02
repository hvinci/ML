'''
Author: hvinci
Date: 2025-02-25 15:34:30
LastEditors: hvinci
LastEditTime: 2025-03-02 23:22:36
Description: 根据词频筛选词汇

Copyright (c) 2025 by ${hvinci}, All Rights Reserved. 
'''

import os

def filter_words_by_summary(input_folder, summary_folder, output_folder):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个文件夹
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)

        # 读取该类别的汇总文档
        summary_file_path = os.path.join(summary_folder, f"{class_folder}_noun_summary.txt")

        # 打印文件路径以进行调试
        print(f"Processing: {summary_file_path}")

        # 跳过不存在的文件
        if not os.path.exists(summary_file_path):
            continue

        # 跳过 .DS_Store_noun_summary.txt 文件
        if summary_file_path.endswith('.DS_Store_noun_summary.txt'):
            continue

        with open(summary_file_path, 'r', encoding='utf-8') as summary_file:
            # 获取该类别汇总文档中的词汇集合
            class_vocabulary = {line.split('\t')[0] for line in summary_file}

        # 遍历每个文件
        for file_name in os.listdir(class_folder_path):
            # Skip .DS_Store files
            if file_name == '.DS_Store':
                continue

            file_path = os.path.join(class_folder_path, file_name)

            # 读取文档内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 按空格分词
            words = content.split()

            # 过滤出在该类别汇总文档中的词汇
            filtered_words = [word for word in words if word in class_vocabulary]

            # 保存处理后的文档
            output_file_path = os.path.join(output_folder, class_folder, f"{file_name}_filtered.txt")
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(" ".join(filtered_words))

if __name__ == "__main__":
    # 定义名词数据的根目录
    noun_data_folder = "cnews/noun_data"

    # 定义汇总文档的根目录
    summary_folder = "cnews/noun_word_frequency_data"

    # 定义输出文件夹
    output_folder = "cnews/filtered_noun_data"

    # 执行过滤操作
    filter_words_by_summary(noun_data_folder, summary_folder, output_folder)

    print("Filtering words by summary completed.")

'''
Author: hvinci
Date: 2023-12-19 23:41:48
LastEditors: hvinci
LastEditTime: 2023-12-19 23:42:05
Description: 

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
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
        with open(summary_file_path, 'r', encoding='utf-8') as summary_file:
            # 获取该类别汇总文档中的词汇集合
            class_vocabulary = {line.split('\t')[0] for line in summary_file}

        # 遍历每个文件
        for file_name in os.listdir(class_folder_path):
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
    noun_data_folder = "code/cnews/noun_data"

    # 定义汇总文档的根目录
    summary_folder = "code/cnews/noun_word_frequency_data"

    # 定义输出文件夹
    output_folder = "code/cnews/filtered_noun_data"

    # 执行过滤操作
    filter_words_by_summary(noun_data_folder, summary_folder, output_folder)

    print("Filtering words by summary completed.")

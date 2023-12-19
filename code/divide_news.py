'''
Author: hvinci
Date: 2023-12-18 23:17:09
LastEditors: hvinci
LastEditTime: 2023-12-18 23:17:23
Description: 

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
import os
import jieba
from tqdm import tqdm  # 如果没有安装tqdm，可以使用 pip install tqdm 安装

# 定义数据集的根目录
root_folder = "news"

# 定义分词后的输出文件夹
output_folder = "cnews/tokenized_data"

# 如果输出文件夹不存在，创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历每个文件夹
for class_folder in os.listdir(root_folder):
    class_folder_path = os.path.join(root_folder, class_folder)

    # 遍历每个文件
    for file_name in tqdm(os.listdir(class_folder_path), desc=f"Processing {class_folder}"):
        file_path = os.path.join(class_folder_path, file_name)

        # 读取文档内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用jieba进行分词
        words = jieba.cut(content)

        # 将分词结果保存到文件中
        output_file_path = os.path.join(output_folder, class_folder, f"{file_name}_tokenized.txt")

        # 确保目录存在
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(" ".join(words))

print("Tokenization completed.")

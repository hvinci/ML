'''
Author: hvinci
Date: 2023-12-19 23:51:37
LastEditors: hvinci
LastEditTime: 2023-12-21 23:43:11
Description: 

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
import os
from sklearn.feature_extraction.text import TfidfVectorizer

def calculate_tfidf(input_folder, output_folder, min_tfidf=0.01):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个文件夹
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)

        # 遍历每个文件
        for file_name in os.listdir(class_folder_path):
            file_path = os.path.join(class_folder_path, file_name)

            # 读取文档内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 初始化 TfidfVectorizer
            vectorizer = TfidfVectorizer()

            # 文档内容列表
            documents = [content]

            # 计算 TF-IDF 值
            tfidf_matrix = vectorizer.fit_transform(documents)

            # 获取特征名（单词）
            feature_names = vectorizer.get_feature_names_out()

            # 创建字典以存储每个文档的 TF-IDF 值
            tfidf_dict = {}

            # 遍历每个文档，将 TF-IDF 值存储在字典中
            for i, doc_tfidf_values in enumerate(tfidf_matrix.toarray()):
                # 将 TF-IDF 值小于 min_tfidf 的设为 0
                doc_tfidf_values[doc_tfidf_values < min_tfidf] = 0
                doc_tfidf_dict = {feature: tfidf for feature, tfidf in zip(feature_names, doc_tfidf_values)}
                tfidf_dict[file_path] = doc_tfidf_dict

            # 保存 TF-IDF 值到文件
            output_file_path = os.path.join(output_folder, class_folder, f"{file_name}_tfidf_values.txt")
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for file_path, doc_tfidf_dict in tfidf_dict.items():
                    for feature, tfidf in doc_tfidf_dict.items():
                        # 格式化 TF-IDF 值为两位小数
                        formatted_tfidf = f"{tfidf:f}"
                        output_file.write(f"{feature}:{formatted_tfidf}\n")
                    output_file.write("\n")

if __name__ == "__main__":
    # 定义输入文件夹（过滤后的名词数据）
    input_folder = "cnews/filtered_noun_data"

    # 定义输出文件夹
    output_folder = "cnews/tfidf_values"

    # 执行计算 TF-IDF 操作，设置 min_tfidf 参数为 0.01
    calculate_tfidf(input_folder, output_folder, min_tfidf=0.01)

    print("Calculating TF-IDF completed.")

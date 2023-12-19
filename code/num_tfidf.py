'''
Author: hvinci
Date: 2023-12-19 23:45:32
LastEditors: hvinci
LastEditTime: 2023-12-19 23:45:40
Description: 

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

def load_summary(summary_file_path):
    high_frequency_words = set()
    with open(summary_file_path, 'r', encoding='utf-8') as summary_file:
        for line in summary_file:
            word, _ = line.strip().split('\t')
            high_frequency_words.add(word)
    return high_frequency_words

def process_documents(input_folder, output_folder, summary_words):
    # 如果输出文件夹不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历每个文件夹
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)

        # 初始化每个类别的文档
        class_documents = []

        # 遍历每个文件
        for file_name in os.listdir(class_folder_path):
            file_path = os.path.join(class_folder_path, file_name)

            # 读取文档内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 添加到该类别的文档列表中
            class_documents.append(content)

        # 将每个文档对应的 TF-IDF 特征值表写入文件
        tfidf_vectorizer = TfidfVectorizer(vocabulary=summary_words)
        tfidf_matrix = tfidf_vectorizer.fit_transform(class_documents)
        tfidf_output_path = os.path.join(output_folder, f"{class_folder}_tfidf_values.txt")

        with open(tfidf_output_path, 'w', encoding='utf-8') as output_file:
            for doc_tfidf_values in tfidf_matrix.toarray():
                for feature_index, tfidf_value in enumerate(doc_tfidf_values):
                    output_file.write(f"{feature_index + 1}:{tfidf_value} ")
                output_file.write("\n")

        # 将 TF 特征值表写入文件（用于 LIBSVM 格式）
        count_vectorizer = CountVectorizer(vocabulary=summary_words, binary=True)
        count_matrix = count_vectorizer.fit_transform(class_documents)
        count_output_path = os.path.join(output_folder, f"{class_folder}_count_values.txt")

        with open(count_output_path, 'w', encoding='utf-8') as output_file:
            for doc_count_values in count_matrix.toarray():
                for feature_index, count_value in enumerate(doc_count_values):
                    output_file.write(f"{feature_index + 1}:{count_value} ")
                output_file.write("\n")

if __name__ == "__main__":
    # 定义输入和输出文件夹路径
    input_folder = "cnews/high_frequency_data/tokenized_data"
    output_folder = "cnews/libsvm_data/tokenized_data"

    # 加载停用词表
    stop_words_path = "stopwords_ch.txt"
    stop_words = set()
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.add(line.strip())

    # 提取名词并去除停用词
    summary_words = load_summary("cnews/summary.txt")
    summary_words = [word for word in summary_words if word not in stop_words]

    # 处理文档
    process_documents(input_folder, output_folder, summary_words)

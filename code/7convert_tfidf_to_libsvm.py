'''
Author: hvinci
Date: 2023-12-19 23:43:27
LastEditors: hvinci
LastEditTime: 2025-03-02 23:27:55
Description: 
    ​TF-IDF 值​ 转换为 ​LIBSVM 格式​
    分别给类别和词汇编号，提取单词和对应的 TF-IDF 值
    按 LIBSVM 格式
    LIBSVM 是支持向量机（SVM）等机器学习模型的通用输入格式

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
import os

def convert_tfidf_to_libsvm(input_folder, output_file_path):
    # 如果输出文件夹不存在，创建它
    output_folder = os.path.dirname(output_file_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 初始化类别编号计数器
    class_index = 1

    # 创建字典以存储每个类别的编号
    class_index_dict = {}

    # 打开输出文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # 遍历每个文件夹
        for class_folder in os.listdir(input_folder):
            class_folder_path = os.path.join(input_folder, class_folder)

            # 初始化单词编号计数器
            word_index = 1

            # 创建字典以存储每个单词的编号
            word_index_dict = {}

            # 获取类别编号，如果类别不在字典中，则分配一个新的编号
            if class_folder not in class_index_dict:
                class_index_dict[class_folder] = class_index
                class_index += 1

            class_index_val = class_index_dict[class_folder]

            # 遍历每个文件
            for file_name in os.listdir(class_folder_path):
                file_path = os.path.join(class_folder_path, file_name)

                # 读取 TF-IDF 值文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # 写入类标号
                output_file.write(f"{class_index_val} ")

                # 遍历每行 TF-IDF 值
                tfidf_list = []
                for line in lines:
                    # 提取单词和 TF-IDF 值
                    tokens = line.strip().split(':')

                    # 跳过不含有效 TF-IDF 值的行
                    if len(tokens) != 2 or tokens[1] == '':
                        continue

                    word = tokens[0]
                    tfidf = float(tokens[1])

                    # 获取单词编号，如果单词不在字典中，则分配一个新的编号
                    if word not in word_index_dict:
                        word_index_dict[word] = word_index
                        word_index += 1

                    word_index_val = word_index_dict[word]
                    tfidf_list.append((word_index_val, tfidf))

                # 补齐特征数量，确保每个文档的特征数量一致
                max_word_index = max(tfidf_list, key=lambda x: x[0])[0]
                for i in range(1, max_word_index + 1):
                    if i not in [word_index_val for word_index_val, _ in tfidf_list]:
                        tfidf_list.append((i, 0.0))

                # 排序单词编号并写入输出文件
                tfidf_list.sort(key=lambda x: x[0])
                for word_index_val, tfidf in tfidf_list:
                    output_file.write(f"{word_index_val}:{tfidf} ")

                output_file.write("\n")

if __name__ == "__main__":
    # 定义输入文件夹（TF-IDF 值数据）
    input_folder = "cnews/tfidf_values"

    # 定义输出文件夹
    output_file_path = "cnews/libsvm_data/libsvm_results.libsvm"

    # 执行转换操作
    convert_tfidf_to_libsvm(input_folder, output_file_path)

    print("Converting TF-IDF to LIBSVM completed.")

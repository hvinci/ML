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
                        print(f"Skipping line: {line}")
                        continue

                    word = tokens[0]
                    tfidf = float(tokens[1])

                    # 获取单词编号，如果单词不在字典中，则分配一个新的编号
                    if word not in word_index_dict:
                        word_index_dict[word] = word_index
                        word_index += 1

                    word_index_val = word_index_dict[word]
                    tfidf_list.append((word_index_val, tfidf))

                # 排序单词编号并写入输出文件
                tfidf_list.sort(key=lambda x: x[0])
                for word_index_val, tfidf in tfidf_list:
                    output_file.write(f"{word_index_val}:{tfidf} ")

                output_file.write("\n")

if __name__ == "__main__":
    # 定义输入文件夹（TF-IDF 值数据）
    input_folder = "code/cnews/tfidf_values"

    # 定义输出文件夹
    output_file_path = "code/cnews/libsvm_data/libsvm_results.libsvm"

    # 执行转换操作
    convert_tfidf_to_libsvm(input_folder, output_file_path)

    print("Converting TF-IDF to LIBSVM completed.")

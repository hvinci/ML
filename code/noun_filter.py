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

    # 遍历每个文件夹
    for class_folder in os.listdir(input_folder):
        class_folder_path = os.path.join(input_folder, class_folder)

        # 遍历每个文件
        for file_name in tqdm(os.listdir(class_folder_path), desc=f"Processing {class_folder}"):
            file_path = os.path.join(class_folder_path, file_name)

            # 读取文档内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 使用jieba进行分词和词性标注
            words_with_flags = pseg.cut(content)

            # 提取名词并去除停用词
            nouns = [word for word, flag in words_with_flags if flag.startswith('n') and word not in stop_words]

            # 将提取的名词保存到文件中
            output_file_path = os.path.join(output_folder, class_folder, f"{file_name}_noun.txt")

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

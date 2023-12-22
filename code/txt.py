'''
Author: hvinci
Date: 2023-12-20 23:40:40
LastEditors: hvinci
LastEditTime: 2023-12-20 23:43:35
Description: 

Copyright (c) 2023 by ${hvinci}, All Rights Reserved. 
'''
def extract_education_lines(input_file_path, output_directory):
    # 读取输入文件
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # 找到以“教育”开头的行
    education_lines = [line.strip() for line in lines if line.startswith('财经')]

    # 将提取的行分组，每组1000行
    grouped_lines = [education_lines[i:i + 1000] for i in range(0, len(education_lines), 1000)]

    # 将每组写入一个新的文档
    for i, group in enumerate(grouped_lines):
        output_file_path = f"{output_directory}/finance{i + 1}.txt"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(group))

    print(f"提取并分组完成，共 {len(grouped_lines)} 个文件。")

# 调用函数并传递文件路径和输出目录
input_file_path = 'file/cnews.train.txt'  # 替换为实际的输入文件路径
output_directory = 'ML/code/news/finance'        # 替换为实际的输出目录
extract_education_lines(input_file_path, output_directory)

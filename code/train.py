'''
Author: hvinci
Date: 2025-02-25 15:34:31
LastEditors: hvinci
LastEditTime: 2025-03-02 23:32:30
Description: 
    确保训练集和测试集的特征索引一致。

    精确率 (Precision)：预测为正类的样本中，实际为正类的比例。
    ​召回率 (Recall)：实际为正类的样本中，预测为正类的比例。
​    F1 分数 (F1 Score)：精确率和召回率的调和平均值。

    SVM：
        基于最大间隔分类，寻找一个超平面将不同类别的样本分开。
        适用于高维数据（如文本分类中的 TF-IDF 特征）。
        通过核函数处理非线性分类问题
    贝叶斯：
        基于贝叶斯定理，假设特征之间相互独立。
        适用于离散特征（如文本分类中的词频或 TF-IDF 值）。
        通过计算条件概率来预测类别。
        
Copyright (c) 2025 by ${hvinci}, All Rights Reserved. 
'''

from sklearn.datasets import load_svmlight_file
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
from sklearn.feature_extraction.text import TfidfVectorizer

# 步骤一：加载数据
def align_max_feature_indices(train_file_path, test_file_path):
    # 读取训练集的最大特征索引
    with open(train_file_path, 'r', encoding='utf-8') as train_file:
        train_max_index = max([int(index.split(':')[0]) for line in train_file for index in line.strip().split()[1:]], default=0)

    # 读取测试集的最大特征索引
    with open(test_file_path, 'r', encoding='utf-8') as test_file:
        test_max_index = max([int(index.split(':')[0]) for line in test_file for index in line.strip().split()[1:]], default=0)

    # 找到两个集的最大值
    overall_max_index = max(train_max_index, test_max_index)

    # 更新训练集的最大特征索引
    with open(train_file_path, 'r+', encoding='utf-8') as train_file:
        content = train_file.read()
        train_file.seek(0)
        train_file.write(content.replace(str(train_max_index), str(overall_max_index)))
        train_file.truncate()

    # 更新测试集的最大特征索引
    with open(test_file_path, 'r+', encoding='utf-8') as test_file:
        content = test_file.read()
        test_file.seek(0)
        test_file.write(content.replace(str(test_max_index), str(overall_max_index)))
        test_file.truncate()

# 使用示例
align_max_feature_indices('code/cnews/libsvm_data/libsvm_results.libsvm', 'code/cnews/libsvm_data/test.libsvm')

X_train, y_train = load_svmlight_file('code/cnews/libsvm_data/libsvm_results.libsvm')
X_test, y_test = load_svmlight_file('code/cnews/libsvm_data/test.libsvm')
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# 步骤二：选择分类算法

# 朴素贝叶斯分类器
nb_classifier = MultinomialNB()
nb_classifier.fit(X_train, y_train)
y_pred_nb = nb_classifier.predict(X_test)

# SVM分类器
svm_classifier = SVC()
svm_classifier.fit(X_train, y_train)
y_pred_svm = svm_classifier.predict(X_test)

# 步骤三：评估分类结果

# 朴素贝叶斯分类器评估
accuracy_nb = accuracy_score(y_test, y_pred_nb)
print("Naive Bayes Classifier:")
print(f'Accuracy: {accuracy_nb}')
print(classification_report(y_test, y_pred_nb))

# SVM分类器评估
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print("\nSVM Classifier:")
print(f'Accuracy: {accuracy_svm}')
print(classification_report(y_test, y_pred_svm))

# 计算每类的正确率、召回率和 F1 分数（朴素贝叶斯）
precision_nb, recall_nb, f1_nb, _ = precision_recall_fscore_support(y_test, y_pred_nb, average=None)
for i in range(len(precision_nb)):
    print(f'Naive Bayes - Class {i + 1}: Precision={precision_nb[i]}, Recall={recall_nb[i]}, F1={f1_nb[i]}')

# 计算总体正确率、召回率和 F1 分数（朴素贝叶斯）
precision_macro_nb, recall_macro_nb, f1_macro_nb, _ = precision_recall_fscore_support(y_test, y_pred_nb, average='macro')
print(f'\nNaive Bayes - Macro-Averaged Precision={precision_macro_nb}, Recall={recall_macro_nb}, F1={f1_macro_nb}')

# 计算每类的正确率、召回率和 F1 分数（SVM）
precision_svm, recall_svm, f1_svm, _ = precision_recall_fscore_support(y_test, y_pred_svm, average=None)
for i in range(len(precision_svm)):
    print(f'SVM - Class {i + 1}: Precision={precision_svm[i]}, Recall={recall_svm[i]}, F1={f1_svm[i]}')

# 计算总体正确率、召回率和 F1 分数（SVM）
precision_macro_svm, recall_macro_svm, f1_macro_svm, _ = precision_recall_fscore_support(y_test, y_pred_svm, average='macro')
print(f'\nSVM - Macro-Averaged Precision={precision_macro_svm}, Recall={recall_macro_svm}, F1={f1_macro_svm}')

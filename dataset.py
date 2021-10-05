import os
import numpy as np
import re
import csv

# print(os.listdir())

# os.mkdir('')
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


# def load_data(txt_path, max_len=None, num_words=None):
def load_data(txt_path):
    dataset_data = []
    dataset_labels = []
    pattern = r'\d+\.\d*'

    for txt in os.listdir(txt_path):
        if txt[-3:] == 'txt':
            old_key = ''
            with open(os.path.join(txt_path, txt), 'r', encoding='utf-8') as txt_read:
                for line in txt_read:
                    line = line.strip()
                    if line != '\n'.strip():
                        key = line.split('.')[0]
                        if old_key == key:
                            pass
                        else:
                            old_key = key
                        line_question = re.sub(pattern=pattern, string=line.split('|')[0].strip(), repl='')
                        line_question = line_question.strip(' . ')
                        line_points = [i.strip(" ;") for i in line.split('|')[1:]]
                        if ':' in line_question:
                            continue
                        else:
                            dataset_data.append(line_question)
                            dataset_labels.append(", ".join(line_points))
    return dataset_data, dataset_labels


def get_class_dict(txt_path):
    class_dict = {}
    # dataset, labels = load_data()
    old_c = ''
    old_i = 0
    # for i, c in enumerate(load_data(txt_path)[1]):
    for i, c in enumerate(transform_voz_kod(txt_path)[1]):
        if c == old_c:
            pass
        else:
            class_dict[old_i] = c
            old_c = c
            old_i += 1
    return class_dict


def transform_voz_kod(voz_kod_dir_path, res_path=None):
    dataset_data = []
    dataset_labels = []
    pattern = r'\d+\.\d*'
    for txt in os.listdir(voz_kod_dir_path):
        if txt[-3:] == 'txt':
            with open(os.path.join(voz_kod_dir_path, txt), 'r', encoding='utf-8') as read_f:
                    # open(os.path.join(res_path, txt), 'w', encoding='utf-8') as write_f:
                idx = 0
                read_f = [line for line in read_f.read().split('\n') if line != '']
                one_state = ''
                for line in read_f:
                    line = line.strip()
                    if 'Статья' in line and len(dataset_labels) == 0:
                        dataset_labels.append(line)
                        continue
                    elif 'Статья' in line:
                        dataset_labels.append(line)
                        dataset_data.append(one_state)
                        one_state = ''
                        idx += 1
                        continue
                    elif 'Бесплатная юридическая консультация' in line:
                        break
                    elif 'Глава' in line:
                        continue
                    if len(one_state) != 0:
                        one_state += f' {re.sub(pattern=pattern, string=line, repl="").strip()}'
                        continue
                    one_state += re.sub(pattern=pattern, string=line, repl='').strip()
                else:
                    dataset_data.append(one_state)
    return dataset_data, dataset_labels


def read_sets(txt_path, max_len=None, num_words=None):
    class_dict = get_class_dict(txt_path)
    dataset_data, dataset_labels = transform_voz_kod(
        voz_kod_dir_path=txt_path
    )
    # dataset_data, dataset_labels = load_data(txt_path)
    x_train = np.array(dataset_data[:101])
    y_train = np.array(dataset_labels[:101])
    x_test = np.array(dataset_data[101:])
    y_test = np.array(dataset_labels[101:])
    with open('train.csv', 'w', encoding='utf-8') as train_csv, open('test.csv', 'w', encoding='utf-8') as test_csv:
        writer_train, writer_test = csv.writer(train_csv), csv.writer(test_csv)
        for c, l in zip(x_train, y_train):
            writer_train.writerow((get_key(class_dict, l), c))
        for c, l in zip(x_test, y_test):
            writer_test.writerow((get_key(class_dict, l), c))


# def load_data(txt_path, max_len=None, num_words=None):
#     dataset_data = []
#     dataset_labels = []
#     pattern = r'\d+\.\d*'
#     for txt in os.listdir(txt_path):
#         if txt[-3:] == 'txt':
#             old_key = ''
#             with open(os.path.join(txt_path, txt), 'r', encoding='utf-8') as txt_read:
#                 for line in txt_read:
#                     line = line.strip()
#                     if line != '\n'.strip():
#                         key = line.split('.')[0]
#                         if old_key == key:
#                             pass
#                         else:
#                             old_key = key
#                         line_question = re.sub(pattern=pattern, string=line.split('|')[0].strip(), repl='')
#                         line_question = line_question.strip(' . ')
#                         line_points = [i.strip(" ;") for i in line.split('|')[1:]]
#                         if ':' in line_question:
#                             continue
#                         else:
#                             dataset_data.append(line_question)
#                             dataset_labels.append(", ".join(line_points))
#     x_train = np.array(dataset_data[:75])
#     # print(x_train[-4])
#     y_train = np.array(dataset_labels[:75])
#     x_test = np.array(dataset_data[75:])
#     y_test = np.array(dataset_labels[75:])
#     tokenizer = Tokenizer(num_words=num_words)
#     tokenizer.fit_on_texts(dataset_data)
#     # print(tokenizer.word_index)
#     x_train = tokenizer.texts_to_sequences(x_train)
#     x_test = tokenizer.texts_to_sequences(x_test)
#     x_train = pad_sequences(x_train, maxlen=max_len)
#     x_test = pad_sequences(x_test, maxlen=max_len)
#     # index = 1
#     # print(dataset_data[index])
#     # print(sequences[index])
#     # print(x_train)
#     return (x_train, y_train), (x_test, y_test)


path = os.path.join(os.getcwd(), 'example', 'txt')
path = "C:/Users/SanZenSekai/PycharmProjects/NN_python/example/txt/voz_kod/voz_kod"
read_sets(path)
# print(get_class_dict(path))

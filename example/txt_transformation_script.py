import re
import os

cmd = "\"C:/Program Files (x86)/Tesseract-OCR/tesseract.exe \" {} {} -l rus"
img_dir = "C:/Users/SanZenSekai/PycharmProjects/NN_python/example/pic"
txt_dir = "C:/Users/SanZenSekai/PycharmProjects/NN_python/example/txt"


def img_to_txt():
    for item in os.listdir(img_dir):
        if os.path.isdir(os.path.join(img_dir, item)):
            # os.mkdir(os.path.join(txt_dir, item))
            for img in os.listdir(os.path.join(img_dir, item)):
                # print(img)
                filename, file_ext = img.split('.')
                cmd_res = cmd.format(os.path.join(img_dir, item, img), os.path.join(txt_dir, item, filename))
                print("run> ", cmd_res)
                os.system(cmd_res)


# img_to_txt()
def lot_txt_to_one(dir_path, res_path, filename):
    res_path = os.path.join(res_path, filename[:-4])
    os.mkdir(res_path)
    with open(os.path.join(res_path, filename), 'w', encoding='utf-8') as write_big:
        for f in os.listdir(dir_path):
            if f[-3:] == 'txt':
                print(f)
                with open(os.path.join(dir_path, f), 'r', encoding='utf-8') as read_small:
                    for line in read_small:
                        write_big.write(line)


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


# lot_txt_to_one(dir_path="C:/Users/SanZenSekai/PycharmProjects/NN_python/example/txt/voz_kod",
#                res_path="C:/Users/SanZenSekai/PycharmProjects/NN_python/example/txt/voz_kod",
#                filename="voz_kod.txt")
# a, b = transform_voz_kod(voz_kod_dir_path="C:/Users/SanZenSekai/PycharmProjects/NN_python/example/txt/voz_kod/voz_kod")

# print(a[-1])
# print(b[-1])

# csv 文件读取
def read_csv(file_path):
    res_dict = []
    index = 0
    title_dict = []
    for line in open(file_path):
        data = line.replace('\n', '').split('\t')
        if index == 0:
            title_dict = data
        else:
            data_dict = {}
            for i in range(len(title_dict)):
                data_dict[title_dict[i]] = data[i]
            res_dict.append(data_dict)
        index += 1
    return res_dict
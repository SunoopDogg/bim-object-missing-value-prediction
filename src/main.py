import json
import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rc

from similarity.cosine_similarity import get_cosine_similarity, get_cosine_similarity_tf_idf
# from similarity.gestalt_pattern_matching import get_gestalt_pattern_matching
from similarity.gestalt_pattern_matching import get_gestalt_pattern_matching
from similarity.jaccard_similarity import get_jaccard_similarity
from similarity.sorensen_dice_coefficient import get_sorensen_dice_coefficient
from util.change_extension import xlsx_to_json
from util.pre_processing import get_tfidf_matrix, get_token, remove_except_parentheses


def get_object_name(json_data):
    object_name = []
    for data in json_data:
        object_name.append(data["Name"])
    return object_name


def get_object_values(json_data):
    object_values = []
    for data in json_data:
        values = []
        for value in data.values():
            if isinstance(value, dict):
                values.extend(value.values())
            else:
                values.append(value)
        object_values.append(values)
    return object_values


if __name__ == '__main__':
    data_dir = os.path.join(os.getcwd(), "data")
    json_dir = os.path.join(data_dir, "json")

    file_name = "속성테이블(가양동)"

    # xlsx_to_json(file_name)

    json_path = os.path.join(json_dir, f"{file_name}.json")
    json_data = None

    with open(json_path, "r") as f:
        json_data = json.load(f)

    names = get_object_name(json_data)
    values = get_object_values(json_data)

    result = get_cosine_similarity_tf_idf([names[1]], [values[1]])

    # 각 result 컬럼의 최대값을 구함
    max_values = result[0].max().values
    max_token = result[0].idxmax().values
    memo = set()
    for i in range(len(max_token)):
        temp = str(max_token[i])
        if temp in memo:
            max_token[i] = f"{max_token[i]}_{i}"
        else:
            max_token[i] = temp

        memo.add(str(max_token[i]))

    print(max_token)

    # 각 result 컬럼의 최대값을 시각화
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 11))
    plt.title(f"{names[1]}")
    plt.bar(max_token, max_values, width=0.5)

    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.4)

    for i, v in enumerate(max_values):
        # colum - value
        plt.text(i, v, f"{result[0].columns[i]
                          } - {v:.2f}", ha='center', va='bottom')

    plt.show()

# save_path = os.path.join(data_dir, "similarity", f"{
#                          file_name}_cosine_tfidf.xlsx")

# last_row = 0
# size = len(result)
# with pd.ExcelWriter(save_path) as writer:
#     for idx, df in enumerate(result):
#         print(f"{idx+1}/{size}")
#         object_name = names[idx]
#         object_name_df = pd.DataFrame(
#             [object_name], columns=["Object Name"])
#         object_name_df.to_excel(writer, startrow=last_row, index=False)
#         last_row += len(object_name_df) + 1

#         df.to_excel(writer, startrow=last_row, index=True)
#         last_row += len(df) + 2

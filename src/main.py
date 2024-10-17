import json
import os
import pandas as pd


from similarity.cosine_similarity import get_cosine_similarity
from similarity.gestalt_pattern_matching import get_gestalt_pattern_matching
from util.change_extension import xlsx_to_json


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

    file_name = "속성테이블2(빌딩스마트협화)"

    # xlsx_to_json(file_name)

    json_path = os.path.join(json_dir, f"{file_name}.json")
    json_data = None

    with open(json_path, "r") as f:
        json_data = json.load(f)

    names = get_object_name(json_data)
    values = get_object_values(json_data)

    # result = get_gestalt_pattern_matching(names, values)
    result = get_cosine_similarity(names, values)

    save_path = os.path.join(data_dir, "similarity", f"{
                             file_name}_cosine.xlsx")

    last_row = 0
    with pd.ExcelWriter(save_path) as writer:
        for idx, df in enumerate(result):
            object_name = names[idx]
            object_name_df = pd.DataFrame(
                [object_name], columns=["Object Name"])
            object_name_df.to_excel(writer, startrow=last_row, index=False)
            last_row += len(object_name_df) + 1

            df.to_excel(writer, startrow=last_row, index=True)
            last_row += len(df) + 2

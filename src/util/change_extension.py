import pandas as pd
import os
import json


def xlsx_to_json(file_name: str):
    data_dir = os.path.join(os.getcwd(), "data")
    xlsx_dir = os.path.join(data_dir, "xlsx")
    file_path = os.path.join(xlsx_dir, f"{file_name}.xlsx")

    df = pd.read_excel(file_path)

    result = []
    item = {}
    step = 3
    object_type = None
    global_id = None

    for idx, row in df.iterrows():
        row_dict = row.to_dict()

        if step == 3 and pd.isna(row_dict["속성세트"]) and pd.isna(row_dict["속성명"]) and pd.isna(row_dict["속성값"]):
            result.append(item)
            item = {}
            step = 1

            if row_dict["객체명"].startswith("객체유형"):
                object_type = row_dict["객체명"].split(":")[1].strip()
                continue

        if step == 1:
            step = 2
            global_id = row_dict["객체명"].split(":")[1].strip()
        elif step == 2:
            step = 3
            item["ObjectType"] = object_type
            item["GlobalID"] = global_id
            item["Name"] = row_dict["객체명"]

        if step == 3:
            if item.get(row_dict["속성세트"]) is None:
                item[row_dict["속성세트"]] = {}
            item[row_dict["속성세트"]
                 ][row_dict["속성명"]] = row_dict["속성값"]

    result.append(item)
    result = result[1:]

    save_path = os.path.join(data_dir, "json", f"{file_name}.json")
    with open(save_path, "w") as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))

    return result


def list_to_xlsx(columns, data, file):

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(file, index=False)


def df_to_xlsx(df, file):
    df.to_excel(file, index=False)

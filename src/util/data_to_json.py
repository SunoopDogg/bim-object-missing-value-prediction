import pandas as pd
import os
import json


if __name__ == "__main__":
    data_dir = os.path.join(os.getcwd(), "data")
    xlsx_dir = os.path.join(data_dir, "xlsx")
    file_path = os.path.join(xlsx_dir, "속성테이블(프로세스).xlsx")

    df = pd.read_excel(file_path)

    result = []
    item = {}
    step = 0

    for idx, row in df.iterrows():
        row_dict = row.to_dict()

        if row_dict["객체명"].startswith("객체유형"):
            step = 1
            if item:
                result.append(item)
                item = {}
        elif step == 1:
            step = 2
            item["GlobalId"] = row_dict["객체명"].split(":")[1].strip()
        elif step == 2:
            step = 3
            item["name"] = row_dict["객체명"]
            item[row_dict["속성명"]] = row_dict["속성값"]
        elif step == 3:
            step = 4
            item[row_dict["속성명"]] = row_dict["속성값"]
        elif step == 4:
            if not item.get(row_dict["속성세트"]):
                item[row_dict["속성세트"]] = {}
            item[row_dict["속성세트"]][row_dict["속성명"]] = row_dict["속성값"]
    result.append(item)

    save_path = os.path.join(data_dir, "json", "속성테이블(프로세스).json")
    with open(save_path, "w") as f:
        f.write(json.dumps(result, indent=4, ensure_ascii=False))

from util.change_extension import xlsx_to_json
from db.mongo_insert import insert_json_to_collection
from util.xlsx_list import load_filenames_from_txt


if __name__ == '__main__':
    file_names = load_filenames_from_txt()

    file_names = [
        file_name for file_name in file_names if '속성테이블(프로세스)' in file_name]

    for file_name in file_names:
        json_data = xlsx_to_json(file_name)
        insert_json_to_collection('bim', file_name, json_data)

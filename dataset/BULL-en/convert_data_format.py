import json
import copy
import argparse

def parse_option():
    parser = argparse.ArgumentParser("command line arguments for generating the ranked dataset.")

    parser.add_argument('--input_dataset_path', type=str, default="./db_info.json",
                        help='filepath of the input dataset.')
    parser.add_argument('--output_dataset_path', type=str, default="./tables.json",
                        help='filepath of the output dataset.')

    opt = parser.parse_args()

    return opt


def main(opt):
    with open(opt.input_dataset_path) as f:
        ccks_tables = json.load(f)

    converted_data = []
    for ccks_table in ccks_tables:
        column_names_original, column_names_chinese = [[-1, "*"]], [[-1, "*"]]
        column_types = ["text"]
        table_name_to_idx = {}
        column_name_to_idx = {}
        for idx, column_info in enumerate(ccks_table["column_info"]):
            # print(column_info["table"])
            table_name = column_info["table"]
            table_name_to_idx[table_name] = idx
            for column_name in column_info["columns"]:
                if column_name == "*":
                    continue
                column_names_original.append(
                    [
                        idx,
                        column_name
                    ]
                )
                column_name_to_idx[table_name + "." + column_name] = len(column_names_original)
            for column_name_chinese in column_info["column_chiName"]:
                if column_name_chinese == "*" or not column_name_chinese:
                    continue
                column_names_chinese.append(
                    [
                        idx,
                        column_name_chinese
                    ]
                )
            for column_type in column_info["columnType_sqlite3"]:
                if not column_type:
                    continue
                column_types.append(column_type)

        db_id = ccks_table["db_name"]

        table_names_original, table_names_chinese = [], []
        for idx, table_name_pair in enumerate(ccks_table["table_name"]):
            table_name, table_name_chinese = table_name_pair

            assert table_name_to_idx[table_name] == idx
            table_names_original.append(table_name)
            table_names_chinese.append(table_name_chinese)

        fks = []
        for fk_pair in ccks_table["table_rel"]:
            pair1, pair2 = fk_pair
            # TODO 这里有些fk是错误的，直接跳过
            try:
                column_idx_1 = column_name_to_idx[".".join(pair1)]
                column_idx_2 = column_name_to_idx[".".join(pair2)]
            except:
                continue

            fks.append([column_idx_1, column_idx_2])

        pks = []
        for pk_pair in ccks_table["primary_keys"]:
            column_idx = column_name_to_idx[".".join(pk_pair)]
            pks.append(column_idx)

        db_schema = {
            "db_id": db_id,
            "table_names_original": table_names_original,
            "table_names": table_names_chinese,
            "column_names_original": column_names_original,
            "column_names": column_names_chinese,
            "column_types": column_types,
            "foreign_keys": fks,
            "primary_keys": pks
        }

        converted_data.append(db_schema)


    with open(opt.output_dataset_path, "w") as f:
        json.dump(converted_data, f, indent=2, ensure_ascii=False)
    # exit()


if __name__ == "__main__":
    opt = parse_option()
    main(opt)

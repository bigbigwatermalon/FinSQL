import json
import re
from fuzzywuzzy import process, fuzz

# from .sqliteStructureTrans_modified import sqlite_2_struct
from sqliteStructureTrans_modified import sqlite_2_struct

with open("src/utils/tables.json") as f:
    tables = json.load(f)
db_map = {}
for table in tables:
    db_id = table["db_id"]
    table_names_original = table["table_names_original"]
    column_names_original = table["column_names_original"]
    column_map_table = {}
    table_map_column = {}
    for column_info in column_names_original[1:]:
        # if column_info[1].lower() == "leadername":
        # print(column_info)
        # exit()
        if column_info[1].lower() not in column_map_table:
            column_map_table[column_info[1].lower()] = []
        column_map_table[column_info[1].lower()].append(table_names_original[column_info[0]].lower())
        if table_names_original[column_info[0]].lower() not in table_map_column:
            table_map_column[table_names_original[column_info[0]].lower()] = []
        table_map_column[table_names_original[column_info[0]].lower()].append(column_info[1].lower())
    # print(len(column_map_table))
    # print(table_map_column)
    # exit()
    db_map[db_id] = {
        "column2table": column_map_table,
        "table2column": table_map_column
    }


# print(db_map["ccks_stock"]["column2table"]["leadername"])
# exit()
def get_all_table_dot_column(sql_struct):
    table_column_list = []
    # select
    for select_item in sql_struct["select"][1:]:
        if select_item[1]:
            table_column_list.append((select_item[1].lower(), select_item[2].lower()))

    # where
    for where_item in sql_struct["where"]:
        if not isinstance(where_item, list):
            continue
        where_item = where_item[0]
        if where_item[0]:
            table_column_list.append((where_item[0].lower(), where_item[1].lower()))

    # grouBy
    for groupBy_item in sql_struct["groupBy"]:
        # groupBy_item = groupBy_item[0]
        if groupBy_item[0]:
            table_column_list.append((groupBy_item[0].lower(), groupBy_item[1].lower()))

    # orderBy
    for orderBy_item in sql_struct["orderBy"]:
        #         orderBy_item = orderBy_item[0]
        if orderBy_item[3]:
            table_column_list.append((orderBy_item[3].lower(), orderBy_item[4].lower()))

    return table_column_list


# def parse_join_condition(sql_query):
#     # 使用正则表达式匹配 JOIN 子句
#     # print(f"sql_query: {sql_query}")
#     join_match = re.search(r'join\s+(\w+)\s+(?:as \w+\s+)?on\s+(\w+\.\w+)\s*=\s*(\w+\.\w+)', sql_query, re.IGNORECASE)
#
#     if join_match:
#         # 提取表名和外键
#         joined_table = join_match.group(1)
#         left_column = join_match.group(2)
#         right_column = join_match.group(3)
#
#         return joined_table, left_column, right_column
#     else:
#         return None

def parse_join_condition(sql_query):
    # 使用正则表达式匹配 JOIN 子句
    join_match = re.search(r'join\s+(\w+)\s+(?:as \w+\s+)?(?:on\s+(\w+\.\w+)\s*=\s*(\w+\.\w+))?', sql_query,
                           re.IGNORECASE)

    if join_match:
        # 提取表名和可能的外键
        joined_table = join_match.group(1)
        left_column = join_match.group(2)
        right_column = join_match.group(3) if join_match.group(3) else None

        return joined_table, left_column, right_column
    else:
        return None


def schema_item_match(sql, table_column_list, db_schema, alias_2_table=None):
    # case1: x.column_a -> a.column_a
    # case2: a.column_b  b.column_a -> a.column_a  b.column_b
    dismatch_table_column_list = []
    for table, column in table_column_list:
        if table not in db_schema["column2table"][column]:
            dismatch_table_column_list.append((table, column))

    # print(dismatch_table_column_list)
    # print(db_schema["column2table"][dismatch_table_column_list[0][1]])
    if alias_2_table:
        table2_2_alias = {v: k for k, v in alias_2_table.items()}
        for table_wrong, column in dismatch_table_column_list:
            table_list = table2_2_alias.keys()
            is_fixed = False
            for table_i in table_list:
                if table_i in db_schema["column2table"][column]:
                    sql = sql.replace(f"{table2_2_alias[table_wrong]}.{column}", f"{table2_2_alias[table_i]}.{column}")
                    is_fixed = True
                    break
            if not is_fixed:
                # print(db_schema["column2table"][column])
                _, left_column, right_column = parse_join_condition(sql)
                alias_2_column = {
                    left_column.split(".")[0]: left_column.split(".")[1],
                    right_column.split(".")[0]: right_column.split(".")[1]
                }
                sampled_one_table = db_schema["column2table"][column][0]
                join_column = alias_2_column[table2_2_alias[table_wrong]]
                for table_i in db_schema["column2table"][column]:
                    if join_column in db_schema["table2column"][table_i]:
                        sampled_one_table = table_i
                        break
                # print(f"sql: {sql}")
                # print(f"wrong: {table_wrong}")
                # print(f"sampled_one_table: {sampled_one_table}")
                sql = sql.replace(f"{table_wrong}", f"{sampled_one_table}")
    else:
        # print(2)
        for table, column in dismatch_table_column_list:
            sql = sql.replace(f"{table}.{column}", f"{db_schema['column2table'][column][0]}.{column}")
    return sql


def fix_type_error(sql):
    # fix typo error
    sql = sql.replace("==", "=")
    # table_a as a join table_b as b; add as key word
    while "  " in sql:
        sql = sql.replace("  ", " ")
    if "join" in sql:
        if "as a join" not in sql:
            sql = sql.replace("a join", "as a join")
        if "as b on" not in sql:
            sql = sql.replace("b on", "as b on")
    return sql


def get_struct(sql):
    try:
        sql_struct = sqlite_2_struct("", "", sql, "")
    except:
        print(f"sql: {sql}")
        print(f"sql struct parsing error, not available...")
        return [], {}
    # print(sql_struct)
    try:
        table_column_list = get_all_table_dot_column(sql_struct)
    except:
        table_column_list = []
    return table_column_list, sql_struct


def alignment(sql, db_id):
    # sql = fix_type_error(sql)
    db_schema = db_map[db_id]
    table_column_list, sql_struct = get_struct(sql)
    try:
        sql = schema_item_match(sql, table_column_list, db_schema, sql_struct["alias_2_table"])
    except:
        print("=====================")
        print(sql)
        print(f"alignment error")
        print("=====================")

    return sql


def post_process(sql, db_id):
    db_schema = db_map[db_id]
    is_available = True
    # fix typo error
    sql = sql.replace("==", "=")
    # table_a as a join table_b as b; add as key word
    while "  " in sql:
        sql = sql.replace("  ", " ")
    if "join" in sql:
        if "as a join" not in sql:
            sql = sql.replace("a join", "as a join")
        if "as b on" not in sql:
            sql = sql.replace("b on", "as b on")
    # TODO add join on
    try:
        sql_struct = sqlite_2_struct("", "", sql, "")
    except:
        print(f"sql: {sql}")
        print(f"sql struct parsing error, not available...")
        return sql, False
    # print(sql_struct)
    try:
        table_column_list = get_all_table_dot_column(sql_struct)
    # print(table_column_list)
    except:
        table_column_list = []
    for table, column in table_column_list:
        # print(table, column)
        # print(db_schema["column2table"][column])
        # print(db_schema["column2table"].keys())
        # if table not in db_schema["table2column"]:
        #     is_available = False
        #     break
        if column not in db_schema["column2table"]:
            # is_available = False
            column_choices = list(db_schema["column2table"].keys())
            column_chosen, score = process.extractOne(column, column_choices)
            print(f"sql: {sql}")
            print(column)
            print(column_chosen)
            sql = sql.replace(column, column_chosen)
            # exit()
            # break
    if not is_available:
        print("*********************")
        print(f"sql grammar error, not available...")
        print(sql)
        print("*********************")
        return sql, False  # not available
    # sql = schema_item_match(sql, table_column_list, db_schema, sql_struct["alias_2_table"])
    # print(sql)
    return sql, True


if __name__ == "__main__":
    pass

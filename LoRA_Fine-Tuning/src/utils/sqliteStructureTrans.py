#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Software: PyCharm

import re
import json
import pandas as pd

from_split_reg = re.compile(" FROM | from | From ")
# 按照ON进行切分
on_split_reg = re.compile(" ON | On | on")
# 按照where关键字进行切分
where_split_reg = re.compile(" WHERE | Where | where ")
# 按照AS关键字进行切分
as_split_reg = re.compile(" +AS | +As | +as ")
# 按照join关键字进行切分
join_split_reg = re.compile(
    " LEFT +JOIN | Left +Join | left +join | INNER +JOIN | Inner +Join | inner +join | JOIN | Join | join")
# 按照select关键字进行切分
sel_split_reg = re.compile("SELECT +|Select +|select +")
# 按照group by关键字进行切分
grp_by_split_reg = re.compile(" GROUP +BY | Group +By | group +by ")
# 按照having关键字进行切分
hav_split_reg = re.compile(" HAVING | Having | having ")
# 按照group by关键字进行切分
limit_split_reg = re.compile(" LIMIT | Limit | limit")
# 按照group by关键字进行切分
order_split_reg = re.compile(" ORDER +BY | Order +By | order +by | ORDER +by ")
# 按照and/or进行切分
and_or_split_reg = re.compile("( AND | And | and | OR | Or | or )")
# 按照and/or进行切分
agg_split_reg = re.compile("count\(|avg\(|sum\(|max\(|min\(")
agg_split_reg_in = re.compile("(count\(|avg\(|sum\(|max\(|min\()")
# WHERE OP操作 (between不支持)
where_op_split_reg = re.compile(
    "(" + "|".join([' like ', " LIKE ", " IS +NOT ", " is +not ", " ?>= ?", " ?<= ?", " ?!= ?",
                    " ?= ?", " ?> ?", " ?< ?", " ?!= ?", " ?!= ?"]) + ")")
# date关键字处理
date_key_reg = re.compile("(strftime\(\'%Y\',|strftime\(\'%m\',|strftime\(\'%d\',|round\(strftime\(\'%m\',)")

date_op_dict_new = {
    "strftime('%Y',": "strftime('%Y', {})",
    "strftime('%m',": "strftime('%m', {})",
    "strftime('%d',": "strftime('%d', {})",
    "round(strftime('%m',": "round(strftime('%m',{})/3.0 + 0.495)"
}


def write_json(obj, filename):
    with open(filename, mode="w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def extract_from_span(sql_query):
    """抽取from关键字对应的span"""
    # 基于from关键字进行划分
    sql_split_res = from_split_reg.split(sql_query)
    # print(f"sql_split_res: {sql_split_res}")
    # 将其他关键字对应内容干掉
    # 干掉where的内容
    tab_info_tmp = where_split_reg.split(sql_split_res[1])[0]
    # print(f"tab_info_tmp: {tab_info_tmp}")
    # 干掉group by内容
    tab_info_tmp = grp_by_split_reg.split(tab_info_tmp)[0]
    # print(f"before: {tab_info_tmp}")
    # 干掉order by内容
    tab_info_tmp = order_split_reg.split(tab_info_tmp)[0]
    # print(f"after: {tab_info_tmp}")

    # 干掉limit内容
    from_string = limit_split_reg.split(tab_info_tmp)[0].strip()

    return from_string


def table_alias_gen(from_string):
    """生成表别名到表名之间的映射"""
    alias_2_table = {}
    # 模式1：通过join创建联系
    if " join " in from_string.lower():
        from_tokens = [x for x in from_string.split(" ") if x]
        # 找到join，on前面的内容，定位别称和表名
        for k, tokk in enumerate(from_tokens):
            tokk = tokk.lower()
            # todo, 当前支持join
            if tokk in ["join", "on"]:
                # 前一个一定是别称
                alias_ = from_tokens[k - 1]
                # 前面第二个是as或者表名
                tok2 = from_tokens[k - 2]
                tok3 = from_tokens[k - 3]
                tab_name = tok2 if tok2.lower() != "as" else tok3
                alias_2_table[alias_] = tab_name
    else:  # 模式2：没有join，是单表
        # 对第一个元素进行处理
        tab_info_tmp = [x.strip() for x in from_string.split(",")]
        # 逐个表提及及进行解析
        for tab_mention in tab_info_tmp:
            # 按照空格进行切分
            tab_m_info = [x for x in tab_mention.split(" ") if x]
            # 第一个是表名，最后一个是别称
            tab_name = tab_m_info[0]
            alias_ = "" if len(tab_m_info) == 1 else tab_m_info[-1]
            alias_2_table[alias_] = tab_name
    return alias_2_table


def extract_from_conds(from_string, alias_2_table):
    """解析from信息中的关联条件"""
    if len(alias_2_table) <= 1:
        conds = []
    else:
        # 多表管理那一定采用join，关联条件用on
        on_tokens = on_split_reg.split(from_string)[1:]
        conds = []
        for on_condi in on_tokens:
            # 按照等号将表切分出来
            cond_split = on_condi.split("=")
            # 第一个表信息
            tab_1_info = cond_split[0].split(".")
            tab1, col1 = tab_1_info[0].strip(), tab_1_info[1].strip()
            tab1 = alias_2_table[tab1]
            # 第二个表信息
            tab_2_info = cond_split[1].strip().split(" ")[0].split(".")
            tab2, col2 = tab_2_info[0].strip(), tab_2_info[1].strip()
            tab2 = alias_2_table[tab2]
            conds.append([[tab1, col1], [tab2, col2]])
    return conds


def parse_from_info(sql_query):
    """基于正则方法抽取出from信息，多表只支持join形式建立关联"""
    # 初始化from输出字典
    from_dict = {}
    # 基于from关键字段内容进行划分
    from_string = extract_from_span(sql_query)
    # 生成表表名到表名之间的映射
    alias_2_table = table_alias_gen(from_string)
    # 生成table_units
    from_dict["table_units"] = [v for u, v in alias_2_table.items()]
    # 解析关联关系
    conds = extract_from_conds(from_string, alias_2_table)
    from_dict["conds"] = conds
    return from_dict, alias_2_table


def is_distinct_extract(token_span):
    """判断是否有distinct, 并将它除掉"""
    is_distinct = False
    if token_span.lower().startswith("distinct"):
        is_distinct = True
        token_span = " ".join(token_span.split(" ")[1:]).strip()
    return is_distinct, token_span


def agg_extract(token_span):
    """判断是否有agg操作, 并将它除掉"""
    agg_res = agg_split_reg.findall(token_span.lower())
    agg_op = None
    if agg_res != []:
        agg_op = agg_res[0][:-1].lower()  # 最后一个反括号去掉
        token_span = token_span[len(agg_op) + 1:][:-1].strip()
    return agg_op, token_span

def agg_extract_hav(token_span):
    """判断是否有agg操作, 并将它除掉"""
    agg_res = agg_split_reg.findall(token_span.lower())
    agg_op = None
    if agg_res != []:
        agg_op = agg_res[0][:-1].lower()  # 最后一个反括号去掉
        token_span = token_span[len(agg_op) + 1:].strip()
    return agg_op, token_span


def select_extract(sql_query, alias_2_table):
    """抽取select条件"""
    # select所在段落抽取出来
    select_span = sel_split_reg.split(sql_query)[1].strip()
    select_span = from_split_reg.split(select_span)[0].strip()
    # 抽取总的distinct信息
    is_distinct, select_span = is_distinct_extract(select_span)
    # 基于英文逗号分隔多个select内容
    select_tokens = select_span.split(",")
    # 初始化select结果
    sel_info = [is_distinct]
    # 逐个token去处理
    for tokeni in select_tokens:
        tokeni = tokeni.strip()
        # 查找当前查询对象是否有agg操作
        agg_op, tokeni = agg_extract(tokeni)
        # 判断是否进行distinct操作
        is_distinct_i, tokeni = is_distinct_extract(tokeni)
        # 取字段名称
        tok_tuple = tokeni.split(".")
        if len(tok_tuple) == 1:
            tab_name = None
            col_name = tok_tuple[0]
        else:
            alias_, col_name = tok_tuple
            tab_name = alias_2_table[alias_]
        sel_info.append([agg_op, tab_name, col_name, is_distinct_i])
    return sel_info


def groupBy_extract(sql_query, alias_2_table):
    """抽取group by关键字信息"""
    # group 所在段落抽取出来
    if " group " not in sql_query.lower():
        return []
    grp_span = grp_by_split_reg.split(sql_query)[1].strip()
    # 基于limit进行切分
    grp_span = limit_split_reg.split(grp_span)[0]
    # 基于having进行切分
    grp_span = hav_split_reg.split(grp_span)[0]
    # 基于order by进行切分
    grp_span = order_split_reg.split(grp_span)[0]
    # 抽取group by信息
    grp_tokens = [x.strip() for x in grp_span.split(",")]
    grp_tokens = [x.split(".") for x in grp_tokens if len(x)]

    grp_info = []
    for grp_toki in grp_tokens:
        # 逐个判断
        if len(grp_toki) == 1:
            grp_info.append([None, grp_toki[0]])
        elif len(grp_toki) == 2:
            grp_info.append([alias_2_table[grp_toki[0]], grp_toki[1]])
    return grp_info


def order_grp_parse(col_info, alias_2_table):
    """解析order by的每个col单元"""
    # 解析agg信息
    agg_, col_info = agg_extract(col_info)
    # 解析distinct
    is_distinct, col_info = is_distinct_extract(col_info)
    # 解析表和字段
    col_info = col_info.split(".")
    if len(col_info) == 2:
        tab_, col_ = alias_2_table[col_info[0]], col_info[1]
    else:
        tab_, col_ = None, col_info[0]
    return [agg_, is_distinct, tab_, col_]


def orderBy_extract(sql_query, alias_2_table):
    # group 所在段落抽取出来
    if " order " not in sql_query.lower():
        return []
    order_span = order_split_reg.split(sql_query)[1].strip()
    # 基于limit进行切分
    order_span = limit_split_reg.split(order_span)[0]
    # 基于having进行切分
    order_span = hav_split_reg.split(order_span)[0]
    # 基于group by进行切分
    order_span = grp_by_split_reg.split(order_span)[0]
    # 抽取order by信息
    order_tokens = [x.strip() for x in order_span.split(",")]

    order_info = []
    for order_toki in order_tokens:
        order_toki = [x for x in order_toki.split(" ") if len(x)]
        # 如果最后一个token是asc, desc
        if order_toki[-1].lower() in ["asc", "desc"]:
            order_toki = [" ".join(order_toki[:-1]), order_toki[-1].lower()]
        else:
            order_toki = [" ".join(order_toki), None]
        # 赋值两块内容
        col_info, order_ = order_toki
        # 解析order里面的agg, distinct, table, column等
        agg_, is_distinct_, tab_, col_ = order_grp_parse(col_info, alias_2_table)
        # 逐个判断
        order_info.append([order_, agg_, is_distinct_, tab_, col_])
    return order_info


def limit_extract(sql_query):
    """抽取limit数值"""
    limit_tuple = sql_query.lower().split(" limit ")
    limit_num = None if len(limit_tuple) <= 1 else int(limit_tuple[1])
    return limit_num


def one_where_constraint(where_token, alias_2_table, agg_op_tmp):
    """解析where的一个约束条件"""
    # 将约束条件切分成多个子串
    sql_tokens = where_op_split_reg.split(where_token)
    # 如果agg_op找到了，那么第一个token最后一个反括号要去掉
    if agg_op_tmp is not None:
        sql_tokens[0] = sql_tokens[0].strip()[:-1]
    # 将sql_tokens中的不同token解析出来
    col_info = sql_tokens[0].split(".")
    date_split = date_key_reg.split(sql_tokens[0])
    date_op = None
    if len(date_split) == 3:
        date_op = date_op_dict_new[date_split[1]]
        # date_op = date_split[1][:-1].lower()

    if len(col_info) == 2 and date_op is not None:
        # 这里谨防as abc
        alias_ = col_info[0].strip().split(",")[-1].strip()
        tab_name = alias_2_table[alias_]
        col_name = col_info[1][:-1]
    elif len(col_info) == 2 and date_op is None:
        alias_ = col_info[0].strip().split("(")[-1].strip()
        tab_name = alias_2_table[alias_]
        col_name = col_info[1]
    elif len(col_info) == 1 and date_op is not None:
        tab_name = None
        col_name = date_split[-1][:-1].strip()
    elif len(col_info) >= 3:
        # "round(strftime('%m',{})/3.0 + 0.495)"
        # tab_info = re.compile("round\(strftime\('%m', (.+)\) / 3.0 + 0.495\)").findall(sql_tokens[0])
        tab_info = sql_tokens[0].replace("round(strftime('%m',", "").replace(")/3.0 + 0.495)", "").strip().split(".")
        col_tuple = [x.strip() for x in tab_info[0].split(".") if len(x.strip())]
        if len(col_tuple) == 1:
            col_name = col_tuple[0]
            tab_name = None
        else:
            col_name = col_tuple[1]
            tab_name = col_tuple[0]
    else:
        tab_name = None
        col_name = col_info[0].strip()
    where_op = sql_tokens[1].strip().lower()
    # 考虑到not写的是is not
    if re.compile("(is +not)").findall(where_op):
        where_op = "not"
    val_tmp = sql_tokens[2].strip()
    # 最终条件形式
    one_constraint = [tab_name, col_name, where_op, val_tmp, date_op]
    return one_constraint


def where_grp_revise(where_grps):
    """对where条件组进行修正，保证每个应该成组的进行打包"""
    output_grps = [[]]
    is_holdon = False
    for i, grpi in enumerate(where_grps):
        if i % 2 == 1:
            if is_holdon:
                output_grps[-1].append(grpi)
            else:
                output_grps.append(grpi)
                output_grps.append([])
            continue
        key_tmp = grpi[1]
        value_tmp = grpi[3]
        date_op_tmp = grpi[4]
        if output_grps[-1] == []:  # 初始条件
            if key_tmp.startswith("("):  # 可能是key被该表了，作为条件组的初始
                is_holdon = True
                key_tmp = key_tmp.strip("(| ")
                if value_tmp.endswith(")"):
                    value_tmp = value_tmp[:-1]
                    grpi[3] = value_tmp
                    is_holdon = False
                grpi[1] = key_tmp
                output_grps[-1].append(grpi)
            else:
                output_grps[-1].append(grpi)
                is_holdon = False
        else:
            right_cnt = list(value_tmp).count("(")
            left_cnt = list(value_tmp).count(")")
            if value_tmp.endswith(")") and left_cnt - right_cnt == 1:  # 必须是反向括号比正向括号多一个
                is_holdon = False
                value_tmp = value_tmp.strip()[:-1].strip()
                grpi[3] = value_tmp
                output_grps[-1].append(grpi)
            else:
                output_grps[-1].append(grpi)
    return output_grps


def where_having_extract(sql_query, alias_2_table, mode="where"):
    """抽取where和having条件"""
    # 判断关键字是否在sql_query中
    if " {} ".format(mode) not in sql_query.lower():
        return []
    # 抽取目标段落
    if mode == "where":
        target_span = where_split_reg.split(sql_query)[1].strip()
    elif mode == "having":
        target_span = hav_split_reg.split(sql_query)[1].strip()

    # 基于limit进行切分
    target_span = limit_split_reg.split(target_span)[0]
    # 基于group by进行切分
    target_span = grp_by_split_reg.split(target_span)[0]
    # 基于having进行切分
    target_span = order_split_reg.split(target_span)[0]
    # 多个约束条件
    constraints_all = and_or_split_reg.split(target_span)
    constraints_all = [x.strip() for x in constraints_all if len(x.strip())]
    # 逐个约束条件进行转化
    output_res = []
    for i, infoi in enumerate(constraints_all):
        # 判断是否条件组开始
        is_start_grp = True if infoi.startswith("(") else False
        if is_start_grp:
            infoi = infoi[1:]

        if i % 2 == 1:  # 约束条件连接符
            output_res.append(infoi.lower())
            continue
        current_info = []
        agg_op_tmp = None
        if mode == "having":
            # 抽取agg算子
            agg_op_tmp, infoi = agg_extract_hav(infoi)
            # 抽取distinct
            is_distinct, infoi = is_distinct_extract(infoi)
            current_info.extend([agg_op_tmp, is_distinct])

        # 解析当前where条件
        one_constraint = one_where_constraint(infoi, alias_2_table, agg_op_tmp)

        if mode == "where" and is_start_grp:
            one_constraint[1] = "(" + one_constraint[1]
        current_info.extend(one_constraint)
        if mode == "having":
            current_info = current_info[:-1]
        output_res.append(current_info)
    if mode == "where":
        # 对结果济宁修正，实现where条件组
        output_res = where_grp_revise(output_res)
    return output_res


def sqlite_2_struct(question, q_id, sql_query, db_name):
    """自动生成提交的数据dict形式"""
    # sql_query = sql_query.replace("\n", "")
    sql_query = sql_query.replace("\n", " ")
    res_dict = {}
    res_dict["q_id"] = q_id
    res_dict["question"] = question
    res_dict["db_name"] = db_name
    res_dict["sql_query"] = sql_query
    # 去掉一些无用字符
    sql_query = sql_query.strip(";| ")
    # 解析from信息
    from_info, alias_2_table = parse_from_info(sql_query)
    # print(f"from_info: {from_info}")
    # print(f"alias_2_table: {alias_2_table}")
    res_dict["from"] = from_info
    # 生成select条件
    sel_info = select_extract(sql_query, alias_2_table)
    res_dict["select"] = sel_info
    # 生成where条件
    where_info = where_having_extract(sql_query, alias_2_table, mode="where")
    res_dict["where"] = where_info
    # 生成group by条件
    grp_info = groupBy_extract(sql_query, alias_2_table)
    res_dict["groupBy"] = grp_info
    # 生成having条件
    having_info = where_having_extract(sql_query, alias_2_table, mode="having")
    res_dict["having"] = having_info
    # 生成order by
    order_info = orderBy_extract(sql_query, alias_2_table)
    res_dict["orderBy"] = order_info
    # 生成limit
    limit_num = limit_extract(sql_query)
    res_dict["limit"] = limit_num
    return res_dict


def gen_sqlite_struct_file(input_file):
    """生成sqlite文件"""
    my_data = pd.read_excel(input_file)

    sqlite_struct_list = []
    for j in range(my_data.shape[0]):
        q_idj = int(my_data.loc[j, "q_id"])
        sql_queryj = my_data.loc[j, "sqlite_query"]
        questionj = my_data.loc[j, "question"]
        db_namej = my_data.loc[j, "db_name"]
        try:
            res_dict = sqlite_2_struct(questionj, q_idj, sql_queryj, db_namej)
        except:
            res_dict = {
                "q_id": q_idj,
                "question": questionj,
                "db_name": db_namej,
                "sql_query": sql_queryj,
                "from": {
                    "table_units": [],
                    "conds": []
                },
                "select": [],
                "where": [],
                "groupBy": [],
                "having": [],
                "orderBy": [],
                "limit": None
            }
        sqlite_struct_list.append(res_dict)
    output_file = input_file.replace(".xlsx", ".json")

    write_json(sqlite_struct_list, output_file)


if __name__ == '__main__':
    test_results_file = "results.xlsx"
    gen_sqlite_struct_file(test_results_file)




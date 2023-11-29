import json
from typing import Tuple
from .sqliteStructureTrans import sqlite_2_struct
from tqdm import tqdm
from .sql_post_process import post_process


def result_eq(sql_dict_1, sql_dict_2, keep_distinct=False) -> Tuple[bool, str]:
    # compare tables
    from_tables_1 = sql_dict_1["from"]["table_units"]
    from_tables_2 = sql_dict_2["from"]["table_units"]
    if len(from_tables_1) != len(from_tables_2):
        return False, "different table number"
    table_set_1 = set(from_tables_1)
    table_set_2 = set(from_tables_2)
    if table_set_1 != table_set_2:
        return False, "table doesn't match!!!"

    # compare select
    select_items_1 = sql_dict_1["select"]
    tot_distinct_1 = select_items_1[0]
    select_items_2 = sql_dict_2["select"]
    tot_distinct_2 = select_items_2[0]
    if keep_distinct and tot_distinct_1 != tot_distinct_2:
        return False, "global distinct differs"
    columns_set_1 = set()
    for column_info in select_items_1[1:]:
        column_descriptions = []
        # print(f"column_info: {column_info}")
        if column_info[0]:
            column_descriptions.append(column_info[0])
        if column_info[1]:
            column_descriptions.append(column_info[1])
        if column_info[3]:
            column_descriptions.append("distinct " + column_info[2])
        else:
            column_descriptions.append(column_info[2])
        #         print(sql_dict_1)
        #         print(f"column_descriptions: {column_descriptions}")
        column_str = " ".join(column_descriptions)
        #         print(f"column_str: {column_str}")
        columns_set_1.add(column_str)
    columns_set_2 = set()
    for column_info in select_items_2[1:]:
        column_descriptions = []
        if column_info[0]:
            column_descriptions.append(column_info[0])
        if keep_distinct and column_info[3]:
            column_descriptions.append("distinct " + column_info[2])
        else:
            column_descriptions.append(column_info[2])
        columns_set_2.add(" ".join(column_descriptions))
    if columns_set_1 != columns_set_2:
        return False, "column doesn't match"

    # compare where
    where_items_1 = sql_dict_1["where"]
    where_items_2 = sql_dict_2["where"]
    where_set_1 = set()
    where_set_2 = set()
    for item in where_items_1:
        if isinstance(item, str):
            continue
        item = item[0]
        cond_list = item[1:3]
        if item[4]:
            cond_list.append(item[4].format(item[3]))
        else:
            cond_list.append(item[3])
        where_set_1.add(" ".join(cond_list))
    for item in where_items_2:
        if isinstance(item, str):
            continue
        item = item[0]
        cond_list = item[1:3]
        if item[4]:
            cond_list.append(item[4].format(item[3]))
        else:
            cond_list.append(item[3])
        where_set_2.add(" ".join(cond_list))
    if where_set_1 != where_set_2:
        return False, "where condition doesn't match"

    # compare groupBy
    group_by_items_1 = sql_dict_1["groupBy"]
    group_by_items_2 = sql_dict_2["groupBy"]
    group_by_set_1 = set()
    group_by_set_2 = set()
    for item in group_by_items_1:
        group_by_set_1.add(item[1])
    for item in group_by_items_2:
        group_by_set_2.add(item[1])
    if group_by_set_1 != group_by_set_2:
        return False, "groupBy doesn't match"

    # compare having
    having_items_1 = sql_dict_1["having"]
    having_items_2 = sql_dict_2["having"]
    having_set_1 = set()
    having_set_2 = set()
    for item in having_items_1:
        item_list = []
        if item[0]:
            item_list.append(item[0])
        if item[1]:
            item_list.append("distinct")
        if item[2]:
            item_list.append(item[2] + ".")
        if item[3]:
            item_list.append(item[3])
        if item[4]:
            item_list.append(item[4])
        if item[5]:
            item_list.append(item[5])
        having_set_1.add(" ".join(item_list))

    for item in having_items_2:
        item_list = []
        if item[0]:
            item_list.append(item[0])
        if item[1]:
            item_list.append("distinct")
        if item[2]:
            item_list.append(item[2] + ".")
        if item[3]:
            item_list.append(item[3])
        if item[4]:
            item_list.append(item[4])
        if item[5]:
            item_list.append(item[5])
        having_set_2.add(" ".join(item_list))
    if having_set_1 != having_set_2:
        return False, "having doesn't match"

    # compare orderBy
    order_by_items_1 = sql_dict_1["orderBy"]
    order_by_items_2 = sql_dict_2["orderBy"]
    limit_items_1 = sql_dict_1["limit"]
    limit_items_2 = sql_dict_2["limit"]
    order_by_set_1 = set()
    order_by_set_2 = set()
    for item in order_by_items_1:
        item_list = []
        if item[0]:
            item_list.append(item[0])
        else:
            item_list.append("asc")
        if item[1]:
            item_list.append(item[1])
        if item[2]:
            item_list.append(item[2] + ".")
        if item[3]:
            item_list.append(item[3])
        if item[4]:
            item_list.append(item[4])
        if limit_items_1:
            item_list.append(str(limit_items_1))
        order_by_set_1.add(" ".join(item_list))

    for item in order_by_items_2:
        item_list = []
        if item[0]:
            item_list.append(item[0])
        else:
            item_list.append("asc")
        if item[1]:
            item_list.append(item[1])
        if item[2]:
            item_list.append(item[2] + ".")
        if item[3]:
            item_list.append(item[3])
        if item[4]:
            item_list.append(item[4])
        if limit_items_2:
            item_list.append(str(limit_items_2))
        order_by_set_2.add(" ".join(item_list))

    if order_by_set_1 != order_by_set_2:
        return False, "orderBy doesn't match"

    return True, ""


def get_consistent_sqls(results, select_number=100):
    '''
    results: List[Dict]
    e.g.
    {
        "db_id": "ccks_fund",
        "p_sqls": [
            sql_1,
            sql_2,
            ...,
        ],
    }
    '''

    db_ids = []
    all_p_sqls = []
    for item in results:
        p_sqls = []
        db_ids.append(item['db_id'])
        for idx, x in enumerate(item["p_sqls"]):
            p_sqls.append(x)
            if idx + 1 == select_number:
                break
        all_p_sqls.append(p_sqls)
    # print(f"all_p_sqls: {all_p_sqls}")
    chosen_p_sqls = []
    for idx, db_id in enumerate(tqdm(db_ids)):
        p_sqls = all_p_sqls[idx]
        cluster_sql_list = []
        map_sql_to_struct = {}
        # print(f"p_sqls: {p_sqls}")
        for sql in p_sqls:
            # TODO 在self-consistency之前做一步SQL自检，基于规则修正一些语法错误
            try:
                sql_dict = sqlite_2_struct("question", "q_id", sql, "db_name")
                # print(f"sql_dict: {sql_dict}")
            except:
                print(f"sql parse err, {sql}")
                continue
            map_sql_to_struct[sql] = sql_dict
            struct_match = False
            for idx, cluster in enumerate(cluster_sql_list):
                centenr_sql = cluster[0]
                print(f"center_sql: {centenr_sql}")
                print(map_sql_to_struct[centenr_sql])
                try:
                    is_eq = result_eq(map_sql_to_struct[centenr_sql], sql_dict)
                except:
                    is_eq = False
                if is_eq:
                    cluster_sql_list[idx].append(sql)
                    struct_match = True
                    break
            if not struct_match:
                cluster_sql_list.append([sql])
        cluster_sql_list.sort(key=lambda x: len(x), reverse=True)
        if not cluster_sql_list:
            chosen_p_sqls.append(p_sqls[0])
        else:
            chosen_p_sqls.append(cluster_sql_list[0][0])

    print("save chosen sqls and results...")

    return chosen_p_sqls


if __name__ == "__main__":
    # with open("data/1010_test_sc_ccks_instruction_dev_gold_v1.txt") as f:
    # file_name = "ccks_instruction_dev_gold_v1_1002_Baichuan2_13B_ccks_skeleton_v1_ccks_cot_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_1nodes_sc12.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1002_Baichuan2_13B_ccks_skeleton_v1_ccks_cot_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_1nodes_sc12_temperature1.2.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1002_Baichuan2_13B_ccks_skeleton_v1_ccks_cot_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_1nodes_sc12_top_p1.0.txt"

    # file_name = "ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc15.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc25.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc18.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc18.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc25.txt"
    # file_name = "ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc15.txt"

    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28_top_p0.9_temperature1.2.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28_temperature1.5.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28_top_p0.9.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28_temperature1.2.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28.txt"
    # file_name="ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc28.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc25.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc18.txt"
    # file_name="ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc25.txt"
    # file_name="ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc18.txt"
    # file_name="ccks_instruction_dev_gold_v1_1013_Baichuan2_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc15.txt"
    # file_name="ccks_instruction_dev_gold_v1_1012_Qwen_7B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_all_targets_lora_8nodes_sc15.txt"
    #
    #
    # with open("data/" + file_name) as f:
    #     dataset = json.load(f)
    #
    # # print(dataset)
    # top_1_sqls = []
    # format_dataset = []
    # for sqls in dataset:
    #     top_1_sqls.append(sqls[0])
    #     # print(sqls)
    #     data = {
    #         "p_sqls": sqls,
    #         "db_id": "db_id"
    #     }
    #     format_dataset.append(data)
    #     # print(get_consistent_sqls(data))
    #     # exit()
    # # print(format_dataset[:2])
    # sc_sqls = get_consistent_sqls(format_dataset)
    # # print(sc_sqls)
    # #
    # # exit()
    # with open("data/sc_data/" + file_name[:-4] + "_top_1.txt", "w") as f:
    #     for data in top_1_sqls:
    #         f.write(data + "\n")
    # with open("data/sc_data/" + file_name[:-4] + "sc.txt", "w") as f:
    #     for data in sc_sqls:
    #         f.write(data + "\n")

    # sql_1 = "select b.chinameabbr, a.leadername from lc_executivesholdings as a join lc_stockarchives as b on a.companycode = b.companycode where a.positiondescription like '%副总经理%' and b.state = '浙江省'"
    # sql_2 = "select b.chinameabbr, b.leadername from lc_stockarchives as a join lc_executivesholdings as b on a.companycode = b.companycode where a.state = '浙江省' and b.positiondescription like '%副总经理%'"

    # sql_1 = "select b.chinameabbr, a.leadername from lc_executivesholdings as a join lc_stockarchives as b on a.companycode = b.companycode"
    # sql_2 = "select b.chinameabbr, b.leadername from lc_stockarchives as a join lc_executivesholdings as b on a.companycode = b.companycode"
    #
    # sql_1 = "SELECT b.secuabbr, b.manager FROM mf_bondportifoliodetail AS a JOIN mf_fundarchives AS b ON a.chiname = b.chiname GROUP BY bondtype ORDER BY COUNT(*) DESC LIMIT 10;"
    # sql_1 = "select a.name from mf_fundmanagernew as a join mf_fundrisklevel as b on a.innercode = b.innercode join mf_fundarchives as c on a.innercode = c.innercode where b.risklevel = '中低' group by a.name having count(a.secuabbr) > 5"
    # sql_1 = "select a.name from mf_fundmanagernew as a join mf_fundrisklevel as b on a.innercode = b.innercode where b.risklevel = '中低' group by a.name having count(distinct a.secuabbr) > 5"
    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # print(sql_dict_1)
    # sql_1 = "select fundtypename, count(*) from mf_fcretscaleanalysis where abbrchiname like '易方达基金%' group by fundtypename having count(*) > 1;"
    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # print(sql_dict_1)
    # sql_1 = "select fundtypename, count(*) from mf_fcretscaleanalysis where abbrchiname like '易方达基金%' group by fundtypename having abbrchiname = 'sfsdf';"
    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # print(sql_dict_1)
    # sql_1 = "select secuabbr from mf_fundreturnrank where fundtypename='股票型' order by fundannreturn desc limit 10"
    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # print(sql_dict_1)
    # sql_1 = "select b.secuabbr,b.manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.innercode=b.innercode order by a.holdvolume desc limit 10;"
    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # print(sql_dict_1)
    # sql_1 = "select b.secuabbr,b.manager from mf_bondportifoliodetail as a join mf_fundarchives as b on a.innercode=b.innercode order by a.holdvolume limit 10;"
    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # print(sql_dict_1)
    #
    # sql_1 = "SELECT controllername FROM lc_actualcontroller GROUP BY controllername ORDER BY COUNT(*) DESC LIMIT 1;"
    # sql_2 = "select controllername from lc_actualcontroller group by controllername order by count(*) desc limit 1;"

    # sql_dict_1 = sqlite_2_struct("question", "q_id", sql_1, "db_name")
    # sql_dict_2 = sqlite_2_struct("question", "q_id", sql_2, "db_name")
    # print(sql_dict_1)
    # print(sql_dict_2)
    #
    # print(result_eq(sql_dict_1, sql_dict_2))


    file_name = "vanilla_LoRA_ccks_skeleton_dev_v1_1101_1112_Baichuan2_13B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_qkv_all_targets_lora_1nodes_sc8_temperature15_response.json"
    with open("src/utils/vanilla_LoRA_ccks_skeleton_dev_v1_1112_Baichuan2_13B_ccks_cot_v1_ccks_skeleton_v1_ccks_synonymous_v1_8_epochs_qkv_all_targets_lora_1nodes.json") as f:
        aaa = json.load(f)
    db_ids = []
    for data in aaa:
        db_ids.append(data["db_id"])
    with open("src/utils/sc_results/" + file_name) as f:
        dataset = json.load(f)
    # print(dataset[0])
    format_dataset = []
    top1_sqls = []
    only_post_process = []
    for id, data in enumerate(dataset):
        pred_sql_list = []
        for query_i in data:
            pred_sql_match = query_i.rsplit("```")[-2]
            pred_sql = pred_sql_match.strip("\n").strip(" ")
            pred_sql = pred_sql.replace("\n", " ")
            pred_sql_list.append(pred_sql)
        top1_sqls.append(pred_sql_list[0])
        only_post_process.append(post_process(pred_sql_list[0], db_ids[id])[0])
        # only_post_process.append()
        post_process_pred_sql_list = []
        for idx, pred_sql in enumerate(pred_sql_list):
            is_available = False
            # print(f"pred_sql: {pred_sql}")
            # print(f"db_id: {data['db_id']}")
            if not pred_sql:
                pred_sql = "SELECT"
            else:
                pred_sql, is_available = post_process(pred_sql, db_ids[id])
            while "  " in pred_sql:
                pred_sql = pred_sql.replace("  ", " ")
            pred_sql_list[idx] = pred_sql
            if is_available:
                post_process_pred_sql_list.append(pred_sql)
        if len(post_process_pred_sql_list) == 0:
            post_process_pred_sql_list.append(pred_sql_list[0])

        format_dataset.append(
            {
                "db_id": db_ids[idx],
                "p_sqls": pred_sql_list
            }
        )

    chosen_p_sqls = get_consistent_sqls(format_dataset, 8)
    # print(chosen_p_sqls)

    with open("src/utils/sc_results/" + file_name[:-5] + "_sc8.txt", "w") as f:
        for data in chosen_p_sqls:
            f.write(data + "\n")
    with open("src/utils/sc_results/" + file_name[:-5] + "_top1.txt", "w") as f:
        for data in top1_sqls:
            f.write(data + "\n")
    with open("src/utils/sc_results/" + file_name[:-5] + "_only_post_process.txt", "w") as f:
        for data in only_post_process:
            f.write(data + "\n")



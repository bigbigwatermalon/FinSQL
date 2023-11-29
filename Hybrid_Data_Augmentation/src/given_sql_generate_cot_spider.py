import openai
import json
from third_party.test_suite_sql_eval.exec_eval import eval_exec_match
from utils.templates import few_shot_examples_spider, schema_template_en_list, few_shot_examples_cspider, hs_schema_template_1, few_shot_map
from utils.extra import get_logger
from utils.template import Template
from generation_function import generate_augment_data_without_llm, generate_augment_data_from_llm
import random
import re
import time
import os
import sqlite3
import argparse
import tiktoken
import datetime


logger = get_logger(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")
# tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


def parse_option():
    parser = argparse.ArgumentParser("command line arguments for generate cot data")
    parser.add_argument("--seed", type=int, default=4399)
    parser.add_argument("--max_attempt_times", type=int, default=3)
    parser.add_argument("--input_dataset_path", type=str,
                        default="preprocessed_data/preprocessed_train_spider.json")
    parser.add_argument("--output_dataset_path", type=str,
                        default="preprocessed_data/succ_spider_cot_train.json")
    parser.add_argument("--db_dir", type=str, default="datasets/spider/database")
    parser.add_argument("--token_usage_limit", type=int, default=1000000000)
    parser.add_argument("--add_output_timestamp", action="store_true")
    parser.add_argument("--start_idx", type=int, default=0)
    parser.add_argument("--init_input_tokens", type=int, default=0)
    parser.add_argument("--init_completion_tokens", type=int, default=0)
    parser.add_argument("--task_type", type=str, default="cot")
    parser.add_argument("--input_template", type=str, default="instruction_spider_1")
    parser.add_argument("--output_template", type=str, default="normal_sql_output_template")
    parser.add_argument("--fail_data_template", type=str, default="instruction_spider_1,instruction_spider_2,instruction_spider_3")
    parser.add_argument("--fs_example", type=str, default="spider")
    opt = parser.parse_args()

    return opt


# TODO add in the config file
synonymous_template_spider = """Give you a sentence, please write a sentence with the same meaning as this sentence.
Requirements:
1 - Try to use a different sentence structure and expression method.
2 - Maintain consistent semantics.
3 - Do not provide any explanations.

Some examples about this question:

Q: How many singers do we have?
A: What is the total count of singers?

Q: Display the names, countries, and ages of each singer, sorted from oldest to youngest.
A: Show the names, countries, and ages of each singer, sorted in descending order of age.

Q: Show the names and release years of songs by the youngest singer.
A: What are the names and release years of all songs by the youngest singer?

Q: From which different countries do singers above 20 years old come?
A: Which countries have singers above 20 years old?

Q: Return the names of countries with at least 3 different languages and the number of languages for each.
A: What are the names of countries that speak more than 2 languages, and how many languages do they speak?

Q: Find the number of cities in each region where the population is above the average population of all cities.
A: How many cities in each region have a population higher than the average population of all cities?

Q: What are the orchestra record companies sorted in descending order of establishment year?
A: Provide the names of music companies with orchestras, sorted in descending order of establishment year.

Q: List the airport code and name for the city of "Lhasa."
A: Give the airport code and airport name corresponding to the city "Lhasa."

Q:
"""

synonymous_template_cspider = """给你一个句子，请你写出一句和这个句子语义相同的句子。
要求：
1 - 句式结构，表达方式尽可能不同。
2 - 保持语义一致。
3 - 不要有任何解释。

关于这个问题的一些示例：

Q：我们有多少歌手？
A：歌手的总数是多少？

Q：按歌手年龄从最大到最小，显示每个歌手的姓名、国家、年龄。
A：按年龄降序，每个歌手的名字、国家、年龄是什么？

Q：显示最年轻歌手的歌曲的名字和发行年份。
A：最年轻歌手的所有歌曲的名字和发行年是多少？

Q：20岁以上的歌手来自哪些不同国家？
A：哪些国家有20岁以上的歌手？

Q：返回至少使用3种语言的不同国家名称和语言数量。
A：讲2种以上语言的国家的名称是什么，以及它们讲多少种语言？

Q：找出每个地区其人口大于城市平均人口的城市数量。
A：每个地区有多少城市的人口高于所有城市的平均人口？

Q：按创立年份的降序排列的管弦乐队唱片公司是哪些？
A：返回按创立年份降序排列的乐团唱片公司的名称。

Q：列出“拉萨”市的机场代码和名称。
A：给出与城市“拉萨”对应的机场代码和机场名称。

Q："""

hs_fs_example_1 = "样例：\n客户问题\"查询出tableA中column1大于5万的所有数据\"对应的mysql语句是：select * from tableA where column1 >= \"5万\""
hs_fs_example_none = ""
if __name__ == "__main__":
    opt = parse_option()
    print(opt)
    random.seed(opt.seed)
    input_path = opt.input_dataset_path
    saved_path = opt.output_dataset_path
    if opt.add_output_timestamp:
        saved_path = saved_path.split(".json")[0] + "_" + datetime.datetime.now().strftime(
            "%y_%m_%d_%H_%M_%S") + ".json"
    tot_input_tokens, tot_completion_tokens = opt.init_input_tokens, opt.init_completion_tokens
    with open(input_path) as f:
        dataset = json.load(f)
    # print(len(dataset))


    input_template_list = [Template(name) for name in opt.input_template.split(",")]

    # TODO add more output template
    output_template_list = [Template(name) for name in opt.output_template.split(",")]

    fail_template_list = [Template(name) for name in opt.fail_data_template.split(",")]

    result_list = []
    for idx, data in enumerate(dataset):
        # print(data["question"])
        # exit()
        if idx < opt.start_idx:
            continue
        print(f"id: {idx}")
        used_tables = {}
        # TODO 写成更好的形式
        for table_info in data["db_schema"]:
            used_tables[table_info["table_name_original"]] = table_info["column_names_original"]
        used_fks = []
        for fk_info in data["fk"]:
            source_table = fk_info["source_table_name_original"]
            source_column = fk_info["source_column_name_original"]
            target_table = fk_info["target_table_name_original"]
            target_column = fk_info["target_column_name_original"]
            used_fks.append(
                f"{source_table}.{source_column} = {target_table}.{target_column}"
            )
        # if len(used_tables) > 10:
        #     print(data["question"])
        #     exit()
        # print(len(used_tables))
        question = data["question"]
        sql = data["sql"]
        db_id = data["db_id"]
        # exit()
        db_path = f"{opt.db_dir}/{db_id}/{db_id}.sqlite"
        # logger.info(f"db_path: {db_path}")
        # get schema template func
        used_schema_template_func_idx = random.randint(0, len(schema_template_en_list) - 1)
        schema_template_func = schema_template_en_list[used_schema_template_func_idx]
        # schema_template_func = hs_schema_template_1

        # get instruction template
        used_instruction_template_idx = random.randint(0, len(input_template_list) - 1)
        instruction_template = input_template_list[used_instruction_template_idx]

        # get output template
        used_output_template_idx = random.randint(0, len(output_template_list) - 1)
        output_template = output_template_list[used_output_template_idx]

        return_dict = {}
        if opt.task_type == "cot":
            # TODO 写成参数形式
            # few_shot_examples = few_shot_examples_cspider if opt.fs_example == "cspider" else few_shot_examples_spider
            few_shot_examples = few_shot_map[opt.fs_example]
            used_few_shot_example_idx = random.randint(0, len(few_shot_examples) - 1)
            used_few_shot_example = few_shot_examples[used_few_shot_example_idx]

            return_dict = generate_augment_data_from_llm(
                opt=opt,
                instruction_template=instruction_template,
                schema_template_func=schema_template_func,
                question=question,
                tables=used_tables,
                fks=used_fks,
                gold_sql=sql,
                fs_example=used_few_shot_example,
                task_type=opt.task_type,
                db_path=db_path
            )
            # print(return_dict)
            input_tokens, completion_tokens = return_dict["input_tokens"], return_dict["completion_tokens"]
            flag = return_dict["flag"]
            # TODO 整合统一起来
            used_fail_template_idx = random.randint(0, len(fail_template_list) - 1)
            fail_template = fail_template_list[used_fail_template_idx]
            if flag in ["fail", "invalid SQL", "empty SQL"]:  # fail to generate cot, then we use normally instruction prompt
                logger.info(f"{idx} 失败")
                output_variables = {
                    "gold_sql": sql
                }
                return_dict = generate_augment_data_without_llm(
                    opt=opt,
                    instruction_template=fail_template,
                    schema_template_func=schema_template_func,
                    question=question,
                    tables=used_tables,
                    fks=used_fks,
                    gold_sql=sql,
                    output_template=output_template,
                    output_variables=output_variables,
                    task_type="instruction",
                )
                return_dict["flag"] = flag
                return_dict["input_tokens"] = input_tokens
                return_dict["completion_tokens"] = completion_tokens
            # print(return_dict)
            logger.info(f"保存成功")

        elif opt.task_type == "synonymous":
            synonymous_template = synonymous_template_cspider if opt.fs_example == "cspider" else synonymous_template_spider
            return_dict = generate_augment_data_from_llm(
                opt=opt,
                instruction_template=instruction_template,
                schema_template_func=schema_template_func,
                question=question,
                tables=used_tables,
                fks=used_fks,
                gold_sql=sql,
                fs_example=synonymous_template,
                task_type=opt.task_type,
            )
        elif opt.task_type in ["skeleton", "instruction", "natsql",
                               "natsql_skeleton", "sql_to_natsql", "natsql_to_sql",
                               "instruction_no_fks"]:
            skeleton = data["sql_skeleton"]
            natsql = data["natsql"]
            natsql_skeleton = data["natsql_skeleton"]
            # TODO 写成模板
            if opt.task_type in ["instruction", "instruction_no_fks"]:
                output_variables = {
                    "gold_sql": sql
                }
            elif opt.task_type == "skeleton":
                output_variables = {
                    "gold_sql": sql,
                    "skeleton": skeleton
                }
            elif opt.task_type == "natsql":
                output_variables = {
                    "natsql": natsql
                }
            elif opt.task_type == "natsql_skeleton":
                output_variables = {
                    "natsql_skeleton": natsql_skeleton,
                    "natsql": natsql
                }
            elif opt.task_type == "sql_to_natsql":
                output_variables = {
                    "natsql": natsql
                }
            elif opt.task_type == "natsql_to_sql":
                output_variables = {
                    "gold_sql": sql
                }
            else:
                output_variables = {}
            # logger.info(output_variables)
            # exit()
            return_dict = generate_augment_data_without_llm(
                opt=opt,
                instruction_template=instruction_template,
                schema_template_func=schema_template_func,
                question=question,
                tables=used_tables,
                fks=used_fks,
                gold_sql=sql,
                output_template=output_template,
                output_variables=output_variables,
                task_type=opt.task_type,
                natsql=natsql,
                fs_example=hs_fs_example_none
            )

        return_dict["db_id"] = db_id

        if opt.task_type in ["cot", "synonymous"]:
            input_tokens, completion_tokens = return_dict["input_tokens"], return_dict["completion_tokens"]
            tot_input_tokens += input_tokens
            tot_completion_tokens += completion_tokens
            print(f"at the {idx} example, we have used:\n"
                  f"{tot_input_tokens} input tokens, {tot_completion_tokens} completion tokens, "
                  f"and {(0.0015 * tot_input_tokens + 0.002 * tot_completion_tokens) / 1000} dollars")

        result_list.append(return_dict)
        # TODO Jsonl
        if idx % 20 == 0 or idx == len(dataset) - 1:
            if idx >= 1:
                with open(saved_path, "r") as f:
                    results = json.load(f)
            else:
                results = []
            # results.append(return_dict)
            results.extend(result_list)
            with open(saved_path, "w") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            result_list = []

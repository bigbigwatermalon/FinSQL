import time
from utils.generation_tools import count_tokens, judge_output_is_empty, is_valid, generate_reply
from third_party.test_suite_sql_eval.exec_eval import eval_exec_match
from utils.extra import get_logger

logger = get_logger(__name__)


# TODO 函数放在别的地方统一管理
def generate_augment_data_from_llm(opt, instruction_template, schema_template_func,
                                   question, tables, fks, gold_sql, fs_example=None, task_type="cot", db_path=None):
    assert task_type in ["cot", "synonymous"], f"task_type should be in [cot, synonymous]"
    input_tokens, completion_tokens = 0, 0

    if task_type == "cot":
        assert db_path, f"if you use cot generation task, you should note the db path"
    # 生成CoT时 data排除执行为空和错误SQL
    # 其他增强时跳过
    if task_type == "cot" and db_path and (not is_valid(gold_sql, db_path)):
        print(f"gold_sql: invalid, continue")
        # flag = "fail"
        flag = "invalid SQL"
        return {"flag": flag, "input_tokens": 0, "completion_tokens": 0}

    if task_type == "cot" and judge_output_is_empty(db_path, gold_sql):
        print(f"gold_sql: execution empty, continue")
        # flag = "fail"
        flag = "empty SQL"
        return {"flag": flag, "input_tokens": 0, "completion_tokens": 0}

    # TODO create a new template or function
    if task_type == "cot":
        schema_prompt, fks = schema_template_func(tables, fks)
        variables = {
            "schema": schema_prompt,
            "fks": fks,
            "question": question
        }
        input_prompt = instruction_template.get_prompt(variables)
        # print(input_prompt)
        # exit()
        # input_prompt_with_sql = input_prompt + "\n" + fs_example
        input_prompt_with_sql = input_prompt + f"""
这个问题对应的SQL是
```
{gold_sql}
```
请你先写出生成这条SQL的推理过程，然后再输出最终结果。
{fs_example}"""

        messages = [
            {
                "role": "user",
                "content": input_prompt_with_sql
            }
        ]

        pred_sql = ""
        attempt_times = 0
        completion_reply = ""
        # print(input_prompt_with_sql)
        # exit()
        while not pred_sql and attempt_times < opt.max_attempt_times:
            print(f"尝试次数: {attempt_times}")
            try:
                completions_round_1 = generate_reply(messages)
                completion_reply = completions_round_1.choices[0].message.content
            except:
                print(f"api error, wait for 3 seconds, and try again...")
                # attempt_times += 0.2
                time.sleep(3)
                continue
            logger.info(f"question: {question}\tcompletion_reply: \n{completion_reply}")
            # input_tokens += count_tokens(input_prompt)
            input_tokens += count_tokens(input_prompt_with_sql)
            completion_tokens += count_tokens(completion_reply)
            # 判断返回的Prompt格式是否符合规范，是否可解析出sql
            try:
                pred_sql_match = completion_reply.rsplit("```")[-2]
            except:
                pred_sql_match = ""
                flag = "fail"

            # 判断是否会存在多条SQL，如果存在多条SQL则抛弃。
            if completion_reply.count("```") > 2:
                pred_sql_match = ""
                flag = "fail"

            # judge whether the cot contents are generated
            if len(pred_sql_match) / (len(completion_reply) + 1e-6) > 0.8:
                flag = "fail"
                pred_sql_match = ""

            if not pred_sql_match:
                print(f"生成的prompt的sql部分格式结果不符合规范重新生成...")
                attempt_times += 1
                continue
            else:
                pred_sql = pred_sql_match.strip("\n").strip(" ")
            # print("----------------")
            # print(pred_sql)
            # print("----------------")
            # print(db_path)
            # 判断sql是否可执行
            if not is_valid(pred_sql, db_path):
                pred_sql = None
            attempt_times += 1

        if not pred_sql or not completion_reply:
            print(f"无效SQL")

        # judge whether pred_sql is correct
        if pred_sql:
            exec_result = eval_exec_match(
                db=db_path,
                p_str=pred_sql,
                g_str=gold_sql,
                plug_value=False,
                keep_distinct=True,
                progress_bar_for_each_datapoint=False,
            )
        else:
            exec_result = 0

        if exec_result == 1:
            flag = "succ"
            return_dict = {
                "flag": flag,
                "question": question,
                "gold_sql": gold_sql,
                "pred_sql": pred_sql,
                "instruction": input_prompt,
                "input": "",
                "output": completion_reply,
                "input_tokens": input_tokens,
                "completion_tokens": completion_tokens
            }
        else:
            flag = "fail"
            return_dict = {
                "flag": flag,
                "input_tokens": input_tokens,
                "completion_tokens": completion_tokens
            }
        return return_dict

    elif task_type == "synonymous":
        input_prompt = fs_example + question + "\nA: "
        messages = [
            {
                "role": "user",
                "content": input_prompt
            }
        ]
        synonymous_question = None
        while not synonymous_question:
            try:
                completions = generate_reply(messages)
                synonymous_question = completions.choices[0].message.content
            except:
                synonymous_question = None
                time.sleep(3)
                print(f"api error, wait for 3 seconds, and try again...")
                continue

        input_tokens += count_tokens(input_prompt)
        completion_tokens += count_tokens(synonymous_question)

        schema_prompt, fks = schema_template_func(tables, fks)
        variables = {
            "schema": schema_prompt,
            "fks": fks,
            "question": synonymous_question
        }
        instruction = instruction_template.get_prompt(variables)
        output = f"""Generated SQL:
```
{gold_sql}
```
"""
        return_dict = {
            "question": question,
            "synonymous_question": synonymous_question,
            "gold_sql": gold_sql,
            "instruction": instruction,
            "input": "",
            "output": output,
            "input_tokens": input_tokens,
            "completion_tokens": completion_tokens
        }
        return return_dict


# TODO 后期根据需求改一下函数参数
def generate_augment_data_without_llm(opt, instruction_template, schema_template_func,
                                      question, tables, fks, gold_sql, output_template, output_variables, skeleton=None,
                                      fs_example=None, task_type="instruction", natsql=None,
                                      db_path=None):
    """Generate augmented data without using LLM.

    :param opt: The options for generating the data.
    :param instruction_template: The template for generating the instruction prompt.
    :param schema_template_func: The function for generating the schema prompt.
    :param question: The question for the data.
    :param tables: The tables in the schema.
    :param fks: The foreign keys in the schema.
    :param gold_sql: The gold SQL query for the data.
    :param output_template: The template for generating the output prompt.
    :param skeleton: The skeleton for the data (optional).
    :param fs_example: The few-shot example for the data (optional).
    :param task_type: The type of task, either "instruction" or "skeleton" (default is "instruction").
    :param db_path: The path to the database (optional).

    :return: A dictionary containing the generated data.
    """
    schema_prompt, fks = schema_template_func(tables, fks)
    if task_type == "instruction_no_fks":
        variables = {
            "schema": schema_prompt,
            "question": question
        }
    else:
        variables = {
            "schema": schema_prompt,
            "fks": fks,
            "question": question,
            "fs_example": fs_example
        }
    if task_type == "sql_to_natsql":
        variables = {
            "gold_sql": gold_sql
        }
    if task_type == "natsql_to_sql":
        variables = {
            "natsql": natsql
        }
    input_prompt = instruction_template.get_prompt(variables)
    # print(output_variables)
    # exit()
    output = output_template.get_prompt(output_variables)

    return_dict = {
        "question": question,
        "gold_sql": gold_sql,
        "instruction": input_prompt,
        "input": "",
        "output": output
    }
    return return_dict

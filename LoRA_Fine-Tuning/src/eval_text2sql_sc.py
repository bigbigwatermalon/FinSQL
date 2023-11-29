# coding=utf-8
# Implements stream chat in command line for fine-tuned models.
# Usage: python cli_demo.py --model_name_or_path path_to_model --checkpoint_dir path_to_checkpoint

from llmtuner import ChatModel, get_infer_text2sql_args
import json
from tqdm import tqdm
from transformers.utils import logging
from utils.self_consistency import get_consistent_sqls
from utils.sql_post_process import post_process, alignment

logger = logging.get_logger(__name__)


def main():
    max_attempt_times = 5
    predicted_sqls = []

    model = ChatModel(*get_infer_text2sql_args())

    model_args, data_args, finetuning_args, generating_args = get_infer_text2sql_args()
    num_return_sequences = generating_args.num_return_sequences
    print(generating_args)
    eval_dataset = data_args.gold_dataset
    predicted_sqls_path = data_args.pred_dataset

    print(f"eval_dataset: {eval_dataset}")
    print(f"predicted_sqls_path: {predicted_sqls_path}")

    with open(eval_dataset) as f:
        eval_dataset = json.load(f)

    data = eval_dataset[0]
    query = data["instruction"] + data["input"]
    history = []
    response_list = model.chat_return_n(query, history=history, num_return_sequences=generating_args.num_return_sequences)
    print(f"response_list: {response_list}")
    for response in response_list:
        print(f"response: {response}")
        # pred_sql_match = response.rsplit("```")[-2]
        # pred_sql = pred_sql_match.strip("\n").strip(" ")
        # pred_sql = pred_sql.replace("\n", " ")
        # print(f"pred_sql: {pred_sql}")
    # exit()

    pred_results = []
    response_results = []
    format_dataset = []
    wo_sc = []
    wo_ali = []
    wo_sc_ali = []
    db_ids = []
    for idx, data in enumerate(tqdm(eval_dataset)):
        db_ids.append(data["db_id"])
        query = data["instruction"] + data["input"]
        attemp_times = 0
        pred_sql = None
        response = None
        pred_sql_list = []
        while attemp_times < max_attempt_times:
            try:
                history = []
                response_list = model.chat_return_n(query, history=history, num_return_sequences=generating_args.num_return_sequences)
                logger.info(f"response_list: {response_list}")
                response_results.append(response_list)
                for response in response_list:
                    print(f"response: {response}")
                    pred_sql_match = response.rsplit("```")[-2]
                    pred_sql = pred_sql_match.strip("\n").strip(" ")
                    pred_sql = pred_sql.replace("\n", " ")
                    print(f"pred_sql: {pred_sql}")
                    pred_sql_list.append(pred_sql)
                logger.info(f"attempt_times: {attemp_times}")
            except:
                attemp_times += 1
                pred_sql_list.append(None)
                continue
            logger.info(f"response: {response}")
            break
        post_process_pred_sql_list = []
        wo_sc.append(pred_sql_list[0])
        wo_sc_ali.append(pred_sql_list[0])
        for idx, pred_sql in enumerate(pred_sql_list):
            is_available = False
            if not pred_sql:
                pred_sql = "SELECT"
            else:
                pred_sql, is_available = post_process(pred_sql, data["db_id"])
            while "  " in pred_sql:
                pred_sql = pred_sql.replace("  ", " ")
            pred_sql_list[idx] = pred_sql
            if is_available:
                post_process_pred_sql_list.append(pred_sql)
        if len(post_process_pred_sql_list) == 0:
            post_process_pred_sql_list.append(pred_sql_list[0])
        pred_results.append(pred_sql_list)
        format_dataset.append(
            {
                "db_id": data["db_id"],
                "p_sqls": pred_sql_list,
            }
        )
        # print(pred_sql)
        # logger.info(f"idx: {idx}, response: {response}")
        # exit()
        predicted_sqls.append(pred_sql)

    # with open(predicted_sqls_path, "w", encoding="utf-8") as f:
    #     json.dump(pred_results, f, ensure_ascii=False, indent=2)
    with open(predicted_sqls_path[:-4] + "_response.json", "w", encoding="utf-8") as f:
        json.dump(response_results, f, ensure_ascii=False, indent=2)

    chosen_p_sqls = get_consistent_sqls(format_dataset, num_return_sequences)
    w_sc_ali = []
    for idx, p_sql in enumerate(chosen_p_sqls):
        wo_ali.append(p_sql)
        p_sql = alignment(p_sql, db_ids[idx])
        w_sc_ali.append(p_sql)
    for idx, p_sql in enumerate(wo_sc):
        wo_sc[idx] = alignment(p_sql, db_ids[idx])

    with open(predicted_sqls_path[:-4] + "_wo_sc.txt", "w") as f:
        for data in wo_sc:
            f.write(data.strip("\n") + "\n")
    with open(predicted_sqls_path[:-4] + "_wo_ali.txt", "w") as f:
        for data in wo_ali:
            f.write(data.strip("\n") + "\n")
    with open(predicted_sqls_path[:-4] + "_wo_sc_ali.txt", "w") as f:
        for data in wo_sc_ali:
            f.write(data.strip("\n") + "\n")
    with open(predicted_sqls_path[:-4] + "w_sc_ali.txt", "w") as f:
        for data in w_sc_ali:
            f.write(data.strip("\n") + "\n")

    # with open(predicted_sqls_path[:-4] + "_chosen.json", "w", encoding="utf-8") as f:
    #     json.dump(chosen_p_sqls, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    main()

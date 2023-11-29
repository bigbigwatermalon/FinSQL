# coding=utf-8
# Implements stream chat in command line for fine-tuned models.
# Usage: python cli_demo.py --model_name_or_path path_to_model --checkpoint_dir path_to_checkpoint

from llmtuner import ChatModel, get_infer_text2sql_args
import json
from tqdm import tqdm
from transformers.utils import logging

logger = logging.get_logger(__name__)


def main():
    max_attempt_times = 5
    predicted_sqls = []

    model = ChatModel(*get_infer_text2sql_args())

    model_args, data_args, finetuning_args, generating_args = get_infer_text2sql_args()
    eval_dataset = data_args.gold_dataset
    predicted_sqls_path = data_args.pred_dataset

    print(f"eval_dataset: {eval_dataset}")
    print(f"predicted_sqls_path: {predicted_sqls_path}")

    with open(eval_dataset) as f:
        eval_dataset = json.load(f)
    data = eval_dataset[0]
    query = data["instruction"] + data["input"]
    history = []
    response, history = model.chat(query, history=history, num_return_sequences=generating_args.num_return_sequences)
    print(f"length: {history}")
    logger.info(f"response: {response}")
    print(f"response: {response}")
    # exit()
    for idx, data in enumerate(tqdm(eval_dataset)):
        query = data["instruction"] + data["input"]
        attemp_times = 0
        pred_sql = None
        response = None
        while attemp_times < max_attempt_times:
            try:
                history = []
                response, history = model.chat(query, history=history, num_return_sequences=generating_args.num_return_sequences)
                # print(f"length: {history}")
                logger.info(f"response: {response}")
                print(f"response: {response}")
                pred_sql_match = response.rsplit("```")[-2]
                pred_sql = pred_sql_match.strip("\n").strip(" ")
                pred_sql = pred_sql.replace("\n", " ")
                logger.info(f"attempt_times: {attemp_times}")
            except:
                attemp_times += 1
                continue
            logger.info(f"response: {response}")
            break
        if not pred_sql:
            pred_sql = "SELECT"
        while "  " in pred_sql:
            pred_sql = pred_sql.replace("  ", " ")
        # print(pred_sql)
        # logger.info(f"idx: {idx}, response: {response}")
        # exit()
        predicted_sqls.append(pred_sql)

    with open(predicted_sqls_path, "w", encoding="utf-8") as f:
        for sql in predicted_sqls:
            f.write(sql + "\n")


if __name__ == "__main__":
    main()

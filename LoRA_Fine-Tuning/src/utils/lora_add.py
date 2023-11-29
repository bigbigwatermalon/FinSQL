from typing import Literal, Union, Dict
import torch


def add(
    path_1: str,
    path_2: str,
    output_path: str,
    alpha_1: float = 0.5,
    alpha_2: float = 0.5,
):
    lora_1 = torch.load(path_1)
    lora_2 = torch.load(path_2)
    new_lora = {}
    for (k1, v1), (k2, v2) in zip(lora_1.items(), lora_2.items()):
        assert k1 == k2, "error! lora_1 doesn't match lora_2..."
        new_weight = alpha_1 * v1 + alpha_2 * v2
        new_lora[k1] = new_weight

    torch.save(new_lora, output_path)



if __name__ == "__main__":
    # path_1 = "../../checkpoints/resdsql_train_ccks_fund_en_desc/adapter_model.bin"
    # path_2 = "../../checkpoints/resdsql_train_ccks_stock_en_desc/adapter_model.bin"
    # path_1 = "../../checkpoints/resdsql_train_ccks_fund_zh_desc/adapter_model.bin"
    # path_2 = "../../checkpoints/resdsql_train_ccks_stock_zh_desc/adapter_model.bin"
    path_1 = "../../checkpoints/1127/resdsql_train_ccks_fund_zh_desc/adapter_model.bin"
    path_2 = "../../checkpoints/1127/resdsql_train_ccks_stock_zh_desc/adapter_model.bin"
    output_path = "adapter_model.bin"
    alpha_1 = 0.5
    alpha_2 = 0.5
    add(path_1, path_2, output_path)


from load_dataset import *
from reranker_model import *
from reranker import *
from torch.utils.data import DataLoader
from transformers import RobertaTokenizerFast

import unittest


class TestCase(unittest.TestCase):

    def test_RerankerDataset(self):
        dir = "../data/preprocessed_data/reranker_train_natsql_base.txt"
        dataset = RerankerDataset(dir)
        print(dataset[0])
        print(dataset[5])

    def test_prepare_batch_inputs_and_labels(self):
        dir = "../data/preprocessed_data/reranker_train_natsql_base.txt"
        dev_dir = "../data/preprocessed_data/reranker_dev_natsql_base.txt"
        ranked_data_dir = "../data/preprocessed_data/preprocessed_train_spider_natsql.json"
        ranked_data_dev_dir = "../data/preprocessed_data/dev_with_probs_natsql.json"
        train_dataset = RerankerDataset(dir)
        dev_dataset = RerankerDataset(dev_dir)
        train_dataloader = DataLoader(
            train_dataset,
            batch_size=2,
            shuffle=False,
            collate_fn=lambda x: x
        )

        dev_dataloader = DataLoader(
            dev_dataset,
            batch_size=4,
            shuffle=False,
            collate_fn=lambda x: x
        )

        tokenizer = RobertaTokenizerFast.from_pretrained(
            "../models/text2natsql_schema_item_classifier",
            add_prefix_space=True
        )
        ranked_data = get_ranked_data_train(ranked_data_dir, 4, 5)
        for id, batch in enumerate(train_dataloader):
            if id >= 1:
                break
            print(len(batch))
            batch_size = len(batch)
            prepare_batch_inputs_and_labels(batch, tokenizer, ranked_data[id * batch_size: (id + 1) * batch_size])

        randed_dat_dev = get_ranked_data_dev(ranked_data_dev_dir, 4, 5)
        for id, batch in enumerate(dev_dataloader):
            if id >= 1:
                break
            print(len(batch))
            batch_size = len(batch)
            prepare_batch_inputs_and_labels(batch, tokenizer, randed_dat_dev[id * batch_size: (id + 1) * batch_size])

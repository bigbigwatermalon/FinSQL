import torch
import torch.nn as nn

from transformers import AutoConfig, RobertaModel
from utils.print_tools import dprint

class MyReranker(nn.Module):
    def __init__(
            self,
            model_name_or_path,
            vocab_size,
            mode
    ):
        super(MyReranker, self).__init__()

        if mode in ["eval", "test"]:
            # load config
            config = AutoConfig.from_pretrained(model_name_or_path)
            # randomly initialize model's parameters according to the config
            self.plm_encoder = RobertaModel(config)
        elif mode == "train":
            self.plm_encoder = RobertaModel.from_pretrained(model_name_or_path)
            self.plm_encoder.resize_token_embeddings(vocab_size)
        else:
            raise ValueError()

        self.sql_info_cls_head_linear1 = nn.Linear(1024, 256)
        self.sql_info_cls_head_linear2 = nn.Linear(256, 2)

        self.question_info_bilstm = nn.LSTM(
            input_size=1024,
            hidden_size=512,
            num_layers=2,
            dropout=0,
            bidirectional=True
        )
        self.sql_info_bilstm = nn.LSTM(
            input_size=1024,
            hidden_size=512,
            num_layers=2,
            dropout=0,
            bidirectional=True
        )

        self.sql_info_linear_after_pooling = nn.Linear(1024, 1024)

        self.leakyrelu = nn.LeakyReLU()
        self.tanh = nn.Tanh()

        # question 和 sql 作 attention
        self.question_sql_cross_attention_layer = nn.MultiheadAttention(embed_dim=1024, num_heads=8)

        self.dropout = nn.Dropout(p=0.2)

    def question_sql_cross_attention(
            self,
            question_info_embedding,
            sql_info_embedding_in_one_set,
    ):
        sql_num = sql_info_embedding_in_one_set.shape[0]
        sql_info_embedding_attn_list = []
        for sql_id in range(sql_num):
            sql_info_embedding = sql_info_embedding_in_one_set[[sql_id], :]

            sql_info_embedding_attn, _ = self.question_sql_cross_attention_layer(
                sql_info_embedding,
                question_info_embedding,
                question_info_embedding
            )
            sql_info_embedding_attn_list.append(sql_info_embedding_attn)

        sql_info_embedding_in_one_set = sql_info_embedding_in_one_set + torch.cat(sql_info_embedding_attn_list,
                                                                                  dim=0)
        sql_info_embedding_in_one_set = torch.nn.functional.normalize(sql_info_embedding_in_one_set, p=2.0, dim=1)

        return sql_info_embedding_in_one_set

    def sql_cls(
            self,
            encoder_input_ids,
            encoder_input_attention_mask,
            batch_aligned_question_ids,
            batch_aligned_sql_info_ids
    ):

        batch_size = encoder_input_ids.shape[0]

        encoder_output = self.plm_encoder(
            input_ids=encoder_input_ids,
            attention_mask=encoder_input_attention_mask,
            return_dict=True
        )

        batch_sql_cls_logits = []

        for batch_id in range(batch_size):
            sequence_embeddings = encoder_output["last_hidden_state"][batch_id, :, :] # (seq_length x hidden_size)

            question_token_embeddings = sequence_embeddings[batch_aligned_question_ids[batch_id], :]

            aligned_sql_info_ids = batch_aligned_sql_info_ids[batch_id]

            sql_info_embedding_list = []

            # _, (question_hidden_state, _) = self.question_info_bilstm(question_token_embeddings)
            # question_info_embedding = question_hidden_state[-2:, :].view(1, 1024)
            question_info_embedding = torch.mean(question_token_embeddings, dim=0, keepdim=True)
            # print(question_info_embedding.shape)
            for sql_info_ids in aligned_sql_info_ids:
                sql_info_embeddings = sequence_embeddings[sql_info_ids, :]
                # print(f'sql_info_embeddings {sql_info_embeddings.shape}')
                output_t, (hidden_state_t, cell_state_t) = self.sql_info_bilstm(sql_info_embeddings)
                sql_info_embedding = hidden_state_t[-2:, :].view(1, 1024)
                sql_info_embedding_list.append(sql_info_embedding)
            sql_info_embeddings_for_one_set = torch.cat(sql_info_embedding_list, dim=0)
            sql_info_embeddings_for_one_set = self.leakyrelu(
                self.sql_info_linear_after_pooling(sql_info_embeddings_for_one_set)
            )
            # dprint(f'sql_info_embeddings_for_one_set.shape: {sql_info_embeddings_for_one_set.shape}', '3.13')
            # dprint(f'question_token_embeddings.shape: {question_token_embeddings.shape}', '3.13')
            # print(sql_info_embeddings_for_one_set[[0], :].shape)

            # sql_info_embeddings_for_one_set = self.question_sql_cross_attention(
            #     question_info_embedding,
            #     sql_info_embeddings_for_one_set
            # )

            sql_info_embeddings_for_one_set = self.sql_info_cls_head_linear1(sql_info_embeddings_for_one_set)
            sql_info_embeddings_for_one_set = self.dropout(self.leakyrelu(sql_info_embeddings_for_one_set))
            sql_info_cls_logits = self.sql_info_cls_head_linear2(sql_info_embeddings_for_one_set)

            batch_sql_cls_logits.append(sql_info_cls_logits)

        return batch_sql_cls_logits

    def forward(
            self,
            encoder_input_ids,
            encoder_attention_mask,
            batch_aligned_question_ids,
            batch_aligned_sql_info_ids,
    ):
        batch_sql_cls_logits = self.sql_cls(
            encoder_input_ids,
            encoder_attention_mask,
            batch_aligned_question_ids,
            batch_aligned_sql_info_ids,
        )

        return {
            "batch_sql_cls_logits": batch_sql_cls_logits
        }

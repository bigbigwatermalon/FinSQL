set -e

## train schema item classifier
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1120" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1120" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1120.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train"


## train schema item classifier en
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1120" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_ccks_english_v1_1120" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_1120.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train"



### 20219 English schema classifier base_model roberta
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1120" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_ccks_english_v1_1120" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_1120.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "roberta"


### English schema classifier base_model bert
### 1120_cross_encoder_en_bert.txt
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1120_bert" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_ccks_english_v1_1120_bert" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_1120.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"


#### ========== ccks Chinese 1122 few-shot macro =========== ###
## 1122_macro_10_zh_cross_encoder.txt a40c06
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_10" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_10" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1122_macro_10.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"

## 1122_macro_0_zh_cross_encoder.txt a40c08
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_0" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_0" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1122_macro_0.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"

## 1122_macro_200_zh_cross_encoder.txt a40c01
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_200" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_200" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1122_macro_200.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"


## 1122_macro_50_zh_cross_encoder.txt a40c02
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_50" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_50" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1122_macro_50.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"

## 1122_macro_20_zh_cross_encoder.txt a40c10
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_20" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_20" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1122_macro_20.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"

## 1122_macro_100_zh_cross_encoder.txt 20509
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_100" \
#    --tensorboard_save_path "./tensorboard_log/1023_text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_100" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_v1_1122_macro_100.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1120.json" \
#    --model_name_or_path "./pretrained/chinese-roberta-wwm-ext-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "bert"

#### ========== ccks Chinese 1122 few-shot macro =========== ###


#### ========== ccks English 1123 few-shot macro =========== ###
## 1123_macro_100_en_cross_encoder.txt a40c01
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_100" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_100" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1122_macro_100.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "roberta"

## 1123_macro_200_en_cross_encoder.txt a40c09
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_200" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_200" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1122_macro_200.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "roberta"

## 1123_macro_10_en_cross_encoder.txt a40c06
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_10" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_10" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1122_macro_10.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "roberta"

## 1123_macro_0_en_cross_encoder.txt a40c08
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_0" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_0" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1122_macro_0.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "roberta"

# 1123_macro_20_en_cross_encoder.txt
python -u schema_item_classifier_ccks.py \
    --batch_size 16 \
    --gradient_descent_step 2 \
    --device "0" \
    --learning_rate 1e-5 \
    --gamma 2.0 \
    --alpha 0.75 \
    --epochs 128 \
    --patience 16 \
    --seed 42 \
    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_20" \
    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_20" \
    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1122_macro_20.json" \
    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
    --model_name_or_path "./pretrained/roberta-large" \
    --use_contents \
    --add_fk_info \
    --mode "train" \
    --base_model "roberta"

## 1123_macro_50_en_cross_encoder.txt
#python -u schema_item_classifier_ccks.py \
#    --batch_size 16 \
#    --gradient_descent_step 2 \
#    --device "0" \
#    --learning_rate 1e-5 \
#    --gamma 2.0 \
#    --alpha 0.75 \
#    --epochs 128 \
#    --patience 16 \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_50" \
#    --tensorboard_save_path "./tensorboard_log/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_50" \
#    --train_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1122_macro_50.json" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --model_name_or_path "./pretrained/roberta-large" \
#    --use_contents \
#    --add_fk_info \
#    --mode "train" \
#    --base_model "roberta"

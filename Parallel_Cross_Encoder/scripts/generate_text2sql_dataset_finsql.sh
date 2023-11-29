set -e

## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_v1.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_t3c7_v1_nr0.5.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_test_v1.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval"

#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_test_v1.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"



### =====================
## 生成一些数据，用来查错误
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_fix_error.json" \
#    --topk_table_num 2 \
#    --topk_column_num 100 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_gold_ccks_fix_error.json" \
#    --topk_table_num 2 \
#    --topk_column_num 100 \
#    --mode "train" \
#    --add_fk_info \
#    --target_type "sql"

## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks_v1.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1_nr0.2.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"
#
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks_v1.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1_nr0.5.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.5 \
#    --add_fk_info \
#    --target_type "sql"
#
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks_v1.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1_nr0.0.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0 \
#    --add_fk_info \
#    --target_type "sql"

## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks_v1.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1_nr0.8.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.8 \
#    --add_fk_info \
#    --target_type "sql"


# ======= 1101
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_t3c7_v1_1101_with_skeleton.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql" \
#    --output_skeleton


#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_stock_t3c7_v1_1101_with_skeleton.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql" \
#    --output_skeleton

#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1101" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1101.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1101.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval"
#
#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"

#
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_fund_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_fund_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_stock_v1_ccks_1101" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_stock_v1_1101.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_stock_v1_1101.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval"
#
#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_stock_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_stock_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"



#
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_stock_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_stock_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_fund_v1_ccks_1101" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_fund_v1_1101.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_fund_v1_1101.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval"
#
#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_fund_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_fund_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"

#
## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_stock_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_macro_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_macro_v1_ccks_1101" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_macro_v1_1101.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_macro_v1_1101.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval"
#
#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_macro_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_macro_t3c7_v1_1101.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"


## preprocess train_spider dataset
#python preprocessing_ccks.py \
#    --mode "train" \
#    --table_path "./data/ccks_en_final/tables.json" \
#    --input_dataset_path "./data/ccks_en_final/train.json" \
#    --output_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_en_1110.json" \
#    --db_path "./data/ccks_nl2sql/ccks2022_sqlitedb" \
#    --target_type "sql"

## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_train_ccks_en_1110.json" \
#    --output_dataset_path "./data/preprocessed_data/train_ccks_en_t3c7_v1_1110.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"

## generate text2sql training dataset with noise_rate 0.2
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks_en_1110.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_en_t3c7_v1_golden.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "train" \
#    --noise_rate 0.2 \
#    --add_fk_info \
#    --target_type "sql"


## preprocess train_spider dataset
#python preprocessing_ccks.py \
#    --mode "eval" \
#    --table_path "./data/ccks_en_final/tables.json" \
#    --input_dataset_path "./data/ccks_en_final/dev.json" \
#    --output_dataset_path "./data/preprocessed_data/preprocessed_dev_ccks_en_1110.json" \
#    --db_path "./data/ccks_nl2sql/ccks2022_sqlitedb" \
#    --target_type "sql"


## 1114 text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1110
#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1110" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1110.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_en_1110.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval"

#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_en_1110.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_en_1110.json" \
#    --topk_table_num 4 \
#    --topk_column_num 8 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"


## 1114 text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1120
#echo "predict probability for each schema item in the eval set"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1120" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_en_1120.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_en_1122.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "roberta"

#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_en_1122.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_en_1122.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"


################### macro zh 0 10 20 50 100 200 550 #############################
## text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_0
#echo "predict probability for each schema item in the eval set with macro 0"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_0" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_0.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 0"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_0.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_0.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"
#
#
### text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_10
#echo "predict probability for each schema item in the eval set with macro 10"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_10" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_10.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 10"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_10.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_10.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"
#
#
### text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_20
#echo "predict probability for each schema item in the eval set with macro 20"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_20" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_20.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 20"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_20.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_20.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"
#
#
### text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_50
#echo "predict probability for each schema item in the eval set with macro 50"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_50" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_50.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 50"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_50.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_50.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"
#
#
### text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_100
#echo "predict probability for each schema item in the eval set with macro 100"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_100" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_100.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 100"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_100.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_100.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"
#
#
### text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_200
#echo "predict probability for each schema item in the eval set with macro 200"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_200" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_200.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 200"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_200.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_200.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"


### text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1122_macro_550
#echo "predict probability for each schema item in the eval set with macro 550"
## predict probability for each schema item in the eval set
#python schema_item_classifier_ccks.py \
#    --batch_size 32 \
#    --device "0" \
#    --seed 42 \
#    --save_path "./models/text2sql_schema_item_classifier_ccks_chinese_bert_v1_ccks_1120" \
#    --dev_filepath "./data/preprocessed_data/preprocessed_dev_ccks_v1_1124_macro.json" \
#    --output_filepath "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_550.json" \
#    --use_contents \
#    --add_fk_info \
#    --mode "eval" \
#    --base_model "bert"
#
#echo "generate text2sql development dataset with macro 550"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1124_macro_550.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_1124_macro_550.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"


#input_template="./models/[input_file_name]"
#intermedia_template="./data/preprocessed_data/dev_with_probs_[output_file_name]"
#output_template="./data/preprocessed_data/dev_ccks_t3c7_[input_file_name].json"
#files=(
#  "text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_100"
#  "text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_200"
#  "text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_10"
#  "text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_0"
#  "text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_20"
#  "text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_50"
#)
#
#for file in "${files[@]}"
#do
#    # 替换文件名中的关键字
#    input_file_name="${file}"
#    output_file_name="ccks_instruction_${file}"
#
#    # 替换模板中的关键字
#    input_path="${input_template/\[input_file_name\]/$input_file_name}"
#    intermedia_path="${intermedia_template/\[output_file_name\]/$output_file_name}"
#    output_path="${output_template/\[input_file_name\]/$input_file_name}"
#    echo $input_path
#    echo $intermedia_path
#    echo $output_path
#    # 打印生成的命令
#    echo "Processing $file"
#    # predict probability for each schema item in the eval set
#    python schema_item_classifier_ccks.py \
#        --batch_size 32 \
#        --device "0" \
#        --seed 42 \
#        --save_path "$input_path" \
#        --dev_filepath "./data/preprocessed_data/preprocessed_train_ccks_en_v1_1124_macro.json" \
#        --output_filepath "$intermedia_path" \
#        --use_contents \
#        --add_fk_info \
#        --mode "eval" \
#        --base_model "roberta"
#
#    echo "generate text2sql development dataset with macro 550"
#    # generate text2sql development dataset
#    python text2sql_data_generator_ccks.py \
#        --input_dataset_path "$intermedia_path" \
#        --output_dataset_path "$output_path" \
#        --topk_table_num 3 \
#        --topk_column_num 7 \
#        --mode "eval" \
#        --add_fk_info \
#        --target_type "sql"
#done
#



#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_generator_picard_tokenizer.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1101.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_v1_tokenizer.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"
#
#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_generator_picard_tokenizer.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_en_1122.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_en_tokenizer.json" \
#    --topk_table_num 3 \
#    --topk_column_num 7 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"


#echo "generate text2sql development dataset"
## generate text2sql development dataset
#python text2sql_data_generator_ccks.py \
#    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_en_1122.json" \
#    --output_dataset_path "./data/preprocessed_data/dev_ccks_t3c7_en_1122.json" \
#    --topk_table_num 100 \
#    --topk_column_num 10 \
#    --mode "eval" \
#    --add_fk_info \
#    --target_type "sql"

echo "generate text2sql development dataset"
# generate text2sql development dataset
python text2sql_data_generator_ccks.py \
    --input_dataset_path "./data/preprocessed_data/dev_with_probs_ccks_v1_1101.json" \
    --output_dataset_path "./data/preprocessed_data/dev_ccks_stock_t3c7_v1_1101_with_skeleton.json" \
    --topk_table_num 100 \
    --topk_column_num 10 \
    --mode "eval" \
    --add_fk_info \
    --target_type "sql" \
    --output_skeleton


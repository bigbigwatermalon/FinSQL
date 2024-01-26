set -e
#export OPENAI_API_KEY=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
export OPENAI_API_KEY=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

# cot data
python src/data_augmentation.py \
--init_input_tokens 0 \
--init_completion_tokens 0 \
--start_idx 0 \
--input_template instruction_cot_spider_1,instruction_cot_spider_2,instruction_cot_spider_3 \
--fail_data_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
--output_template normal_sql_output_template \
--input_dataset_path "../Parallel_Cross_Encoder/preprocessed_data/preprocessed_train_en.json" \
--output_dataset_path "../Parallel_Cross_Encoder/preprocessed_data/cot_train_en.json" \
--task_type "cot" \
--db_dir "../dataset/database_en" \
--fs_example "financial_cot_generation_en" \

# synonymous data
python src/data_augmentation.py \
--init_input_tokens 0 \
--init_completion_tokens 0 \
--start_idx 0 \
--input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
--fail_data_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
--output_template normal_sql_output_template \
--input_dataset_path "../Parallel_Cross_Encoder/preprocessed_data/preprocessed_train_en.json" \
--output_dataset_path "../Parallel_Cross_Encoder/preprocessed_data/synonymous_train_en.json" \
--task_type "synonymous" \
--db_dir "../dataset/database_en" \
--fs_example "spider_synonymous" \

echo "generate data for evaluation"
python src/data_augmentation.py \
--input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
--output_template skeleton_output_template \
--input_dataset_path "../Parallel_Cross_Encoder/preprocessed_data/preprocessed_train_en.json" \
--output_dataset_path "../Parallel_Cross_Encoder/preprocessed_data/skeleton_train_en.json" \
--task_type "skeleton"



#python src/given_sql_generate_cot_spider.py \
#--start_idx 249 \
#--init_input_tokens 78664 \
#--init_completion_tokens 37615 \

#python src/given_sql_generate_cot_spider.py \
#--input_dataset_path "preprocessed_data/preprocessed_train_spider.json" \
#--task_type "synonymous" \
#--output_dataset_path "preprocessed_data/spider_synonymous_train.json"

#python src/given_sql_generate_cot_spider.py \
#--input_dataset_path "preprocessed_data/preprocessed_train_spider.json" \
#--task_type "skeleton" \
#--output_dataset_path "preprocessed_data/spider_skeleton_train.json" \
#--seed 2144

#python src/given_sql_generate_cot_spider.py \
#--input_dataset_path "preprocessed_data/preprocessed_train_spider.json" \
#--task_type "instruction" \
#--output_dataset_path "preprocessed_data/spider_instruction_train.json" \
#--seed 3366



### test
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_cot_spider_1,instruction_cot_spider_2,instruction_cot_spider_3 \
#--fail_data_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_cot_train.json" \
#--task_type "cot" \


### test
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_synonymous_train.json" \
#--task_type "synonymous" \

### test
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_cot_spider_1,instruction_cot_spider_2 \
#--fail_data_template instruction_spider_1,instruction_spider_2 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_instruction_train.json" \
#--task_type "instruction"


### test
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2 \
#--output_template skeleton_output_template \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_skeleton_train.json" \
#--task_type "skeleton"


### test
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/resdsql_dev_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_instruction_dev.json" \
#--task_type "instruction"
#
### test
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
#--output_template  skeleton_output_template \
#--input_dataset_path "preprocessed_data/resdsql_dev_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_skeleton_dev.json" \
#--task_type "skeleton"


### instruction natsql
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_spider_natsql_1,instruction_spider_natsql_2,instruction_spider_natsql_3 \
#--output_template  natsql_output_template \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_natsql_train.json" \
#--task_type "natsql"

### instruction natsql_skeleton
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template instruction_skeleton_spider_natsql_1,instruction_skeleton_spider_natsql_2,instruction_skeleton_spider_natsql_3 \
#--output_template  natsql_skeleton_output_template \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_natsql_skeleton_train.json" \
#--task_type "natsql_skeleton"

### instruction natsql_to_sql
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template natsql_to_sql_input_prompt \
#--output_template  natsql_to_sql_output_prompt \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_natsql_to_sql_train.json" \
#--task_type "natsql_to_sql"

### instruction sql_to_natsql
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--input_template sql_to_natsql_input_prompt \
#--output_template  sql_to_natsql_output_prompt \
#--input_dataset_path "preprocessed_data/resdsql_train_spider_natsql.json" \
#--output_dataset_path "preprocessed_data/spider_sql_to_natsql_train.json" \
#--task_type "sql_to_natsql"


## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template  normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_train_v1.json" \
#--task_type "instruction" \
##--start_idx 980

## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template  normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold.json" \
#--task_type "instruction"

## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template  normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_split_t3c7.json" \
#--output_dataset_path "preprocessed_data/ccks_cot_dev.json" \
#--task_type "instruction"

## ccks skeleton
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template  skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_v1.json" \
#--task_type "skeleton" \
#--start_idx 3961

## ccks skeleton
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template  skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_split_t3c7.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_dev.json" \
#--task_type "skeleton"

### ccks cot
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 0 \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--fail_data_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_cot_train_v1.json" \
#--task_type "cot" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "cspider" \

### ccks synonymous
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 3961 \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_synonymous_train_v1.json" \
#--task_type "synonymous" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "cspider" \




## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_no_fks_zh_1,instruction_no_fks_zh_2,instruction_no_fks_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_split_t3c7.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_no_fks_train.json" \
#--task_type "instruction_no_fks"
#
## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_no_fks_zh_1,instruction_no_fks_zh_2,instruction_no_fks_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_split_t3c7.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_no_fks_dev.json" \
#--task_type "instruction_no_fks"

## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_split_t3c7.json" \
#--output_dataset_path "preprocessed_data/hs_instruction_0911_v0.3.json" \
#--task_type "instruction"

## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template  normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_cot_dev_gold.json" \
#--task_type "instruction"
#
## ccks instruction sql
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template  normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_dev_gold.json" \
#--task_type "instruction"


## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold_v1.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_cot_dev_gold_v1.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_dev_gold_v1.json" \
#--task_type "instruction"


## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_golden.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold_v1_golden.json" \
#--task_type "instruction"


## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1_nr0.5.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_train_nr0.5.json" \
#--task_type "instruction"

## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1_nr0.5.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_nr0.5.json" \
#--task_type "skeleton"


## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_nr0.0.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold_v1_t3c7_nr0.0.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_nr0.2.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold_v1_t3c7_nr0.2.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_nr0.5.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold_v1_t3c7_nr0.5.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_nr0.8.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_gold_v1_t3c7_nr0.8.json" \
#--task_type "instruction"


### test api
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 0 \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--fail_data_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/test.json" \
#--task_type "cot" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "cspider" \


### ccks cot 10.29
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 280 \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--fail_data_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/1030_t.json" \
#--task_type "cot" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "financial_cot_generation" \


### ccks cot 10.29
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 0 \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--fail_data_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1.json" \
#--output_dataset_path "preprocessed_data/ccks_cot_train_v1_1029_no_gold_sql.json" \
#--task_type "cot" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "financial_cot_generation" \



## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_v1_1101.json" \
#--task_type "skeleton"

## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_macro_v1_1101.json" \
#--task_type "skeleton"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_stock_v1_1101.json" \
#--task_type "skeleton"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_fund_v1_1101.json" \
#--task_type "skeleton"


## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_train_v1_1101.json" \
#--task_type "skeleton"

## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_train_macro_v1.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_train_stock_v1.json" \
#--task_type "instruction"
#
## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_train_fund_v1.json" \
#--task_type "instruction"


#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_instruction_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_cot_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_dev_v1_1101.json" \
#--task_type "instruction"
#
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_stock_instruction_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_stock_cot_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_stock_skeleton_dev_v1_1101.json" \
#--task_type "instruction"
#
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_macro_instruction_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_macro_cot_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_macro_skeleton_dev_v1_1101.json" \
#--task_type "instruction"
#
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_zh_1,instruction_zh_2,instruction_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_fund_instruction_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template cot_zh_1,cot_zh_2,cot_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_fund_cot_dev_v1_1101.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template normal_sql_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_fund_skeleton_dev_v1_1101.json" \
#--task_type "instruction"

### ccks en cot 11.10
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 0 \
#--input_template instruction_cot_spider_1,instruction_cot_spider_2,instruction_cot_spider_3 \
#--fail_data_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/train_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_cot_train_v1_1110.json" \
#--task_type "cot" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "financial_cot_generation_en" \

## ccks en synonymous 11.10
#python src/given_sql_generate_cot_spider.py \
#--init_input_tokens 0 \
#--init_completion_tokens 0 \
#--start_idx 0 \
#--input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--fail_data_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/train_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_synonymous_train_v1_1110.json" \
#--task_type "synonymous" \
#--db_dir "datasets/ccks_nl2sql/ccks2022_sqlitedb" \
#--fs_example "spider_synonymous" \

#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
#--output_template skeleton_output_template \
#--input_dataset_path "preprocessed_data/train_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_skeleton_train_v1_1110.json" \
#--task_type "skeleton"

#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/train_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_instruction_train_v1_1110.json" \
#--task_type "instruction"

#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
#--output_template skeleton_output_template \
#--input_dataset_path "preprocessed_data/dev_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_skeleton_dev_v1_1110.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/dev_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_instruction_dev_v1_1110.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_cot_spider_1,instruction_cot_spider_2,instruction_cot_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/dev_ccks_en_t3c7_v1_1110.json" \
#--output_dataset_path "preprocessed_data/ccks_en_cot_dev_v1_1110.json" \
#--task_type "instruction"

## hs instruction
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_v1_1101.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_stock_skeleton_dev_v1_1101.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_macro_skeleton_dev_v1_1101.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/dev_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_fund_skeleton_dev_v1_1101.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_stock_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_stock_v1_1101.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_macro_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_macro_v1_1101.json" \
#--task_type "skeleton"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#--output_template skeleton_output_template_zh \
#--input_dataset_path "preprocessed_data/train_ccks_fund_t3c7_v1_1101.json" \
#--output_dataset_path "preprocessed_data/ccks_skeleton_train_fund_v1_1101.json" \
#--task_type "skeleton"


#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
#--output_template skeleton_output_template \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_en_1122.json" \
#--output_dataset_path "preprocessed_data/ccks_en_skeleton_dev_v1_1122.json" \
#--task_type "skeleton"

#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_en_1122.json" \
#--output_dataset_path "preprocessed_data/ccks_en_instruction_dev_v1_1122.json" \
#--task_type "instruction"
#
#echo "generate data for evaluation"
#python src/given_sql_generate_cot_spider.py \
#--input_template instruction_cot_spider_1,instruction_cot_spider_2,instruction_cot_spider_3 \
#--output_template normal_sql_output_template \
#--input_dataset_path "preprocessed_data/dev_ccks_t3c7_en_1122.json" \
#--output_dataset_path "preprocessed_data/ccks_en_cot_dev_v1_1122.json" \
#--task_type "instruction"

## 定义输入输出路径模板
#input_template="preprocessed_data/[input_file_name]"
#output_template="preprocessed_data/[output_file_name]"
#
#files=(
#    "dev_ccks_t3c7_1124_macro_10.json"
#    "dev_ccks_t3c7_1124_macro_0.json"
#    "dev_ccks_t3c7_1124_macro_100.json"
#    "dev_ccks_t3c7_1124_macro_50.json"
#    "dev_ccks_t3c7_1124_macro_550.json"
#    "dev_ccks_t3c7_1124_macro_200.json"
#    "dev_ccks_t3c7_1124_macro_20.json"
#)
#
#for file in "${files[@]}"
#do
#    # 替换文件名中的关键字
#    input_file_name="${file}"
#    output_file_name="ccks_skeleton_zh_${file}"
#
#    # 替换模板中的关键字
#    input_path="${input_template/\[input_file_name\]/$input_file_name}"
#    output_path="${output_template/\[output_file_name\]/$output_file_name}"
#    echo $input_path
#    echo $output_path
#    # 打印生成的命令
#    echo "Processing $file"
#    python src/given_sql_generate_cot_spider.py \
#    --input_template skeleton_zh_1,skeleton_zh_2,skeleton_zh_3 \
#    --output_template normal_sql_output_template \
#    --input_dataset_path "$input_path" \
#    --output_dataset_path "$output_path" \
#    --task_type "instruction"
#
##    python src/given_sql_generate_cot_spider.py \
##    --input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
##    --output_template normal_sql_output_template \
##    --input_dataset_path "$input_path" \
##    --output_dataset_path "$output_path" \
##    --task_type "instruction"
#done


## 定义输入输出路径模板
#input_template="preprocessed_data/[input_file_name]"
#output_template="preprocessed_data/[output_file_name]"
#
#files=(
#    "dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_200.json"
#    "dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_20.json"
#    "dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_0.json"
#    "dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_10.json"
#    "dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_100.json"
#    "dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_50.json"
#)
#
#for file in "${files[@]}"
#do
#    # 替换文件名中的关键字
#    input_file_name="${file}"
#    output_file_name="ccks_skeleton_en_${file}"
#
#    # 替换模板中的关键字
#    input_path="${input_template/\[input_file_name\]/$input_file_name}"
#    output_path="${output_template/\[output_file_name\]/$output_file_name}"
#    echo $input_path
#    echo $output_path
#    # 打印生成的命令
#    echo "Processing $file"
#    python src/given_sql_generate_cot_spider.py \
#    --input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
#    --output_template normal_sql_output_template \
#    --input_dataset_path "$input_path" \
#    --output_dataset_path "$output_path" \
#    --task_type "instruction"
#
##    python src/given_sql_generate_cot_spider.py \
##    --input_template instruction_spider_1,instruction_spider_2,instruction_spider_3 \
##    --output_template normal_sql_output_template \
##    --input_dataset_path "$input_path" \
##    --output_dataset_path "$output_path" \
##    --task_type "instruction"
#done

#python src/given_sql_generate_cot_spider.py \
#  --input_template instruction_skeleton_spider_1,instruction_skeleton_spider_2,instruction_skeleton_spider_3 \
#  --output_template normal_sql_output_template \
#  --input_dataset_path ./preprocessed_data/dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_550 \
#  --output_dataset_path  ./preprocessed_data/ccks_skeleton_en_dev_ccks_t3c7_text2sql_schema_item_classifier_roberta-large_ccks_english_v1_1123_macro_500.json\
#  --task_type "instruction"





##
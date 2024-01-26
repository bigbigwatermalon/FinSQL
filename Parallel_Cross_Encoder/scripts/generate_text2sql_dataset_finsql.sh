set -e


echo "predict probability for each schema item in the eval set"
# predict probability for each schema item in the eval set
python schema_item_classifier_finsql.py \
    --batch_size 32 \
    --device "0" \
    --seed 42 \
    --save_path "./models/text2sql_schema_item_classifier_roberta-large_ccks_english" \
    --dev_filepath "./preprocessed_data/preprocessed_dev_en.json" \
    --output_filepath "./preprocessed_data/dev_with_probs_en.json" \
    --use_contents \
    --add_fk_info \
    --mode "eval" \
    --base_model "roberta"

# generate text2sql eval dataset with noise_rate 0.2
python text2sql_data_generator_finsql.py \
    --input_dataset_path "./preprocessed_data/dev_with_probs_en.json" \
    --output_dataset_path "./preprocessed_data/dev_en_t3c7.json" \
    --topk_table_num 3 \
    --topk_column_num 7 \
    --mode "eval" \
    --noise_rate 0.2 \
    --add_fk_info \
    --target_type "sql" \
    --output_skeleton


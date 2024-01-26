
mkdir -p preprocessed_data
# preprocess train dataset
python preprocessing_finsql.py \
    --mode "train" \
    --table_path "../dataset/BULL-en/tables.json" \
    --input_dataset_path "../dataset/BULL-en/train.json" \
    --output_dataset_path "./preprocessed_data/preprocessed_train_en.json" \
    --db_path "../dataset/database_en" \
    --target_type "sql"

# preprocess dev dataset
python preprocessing_finsql.py \
    --mode "eval" \
    --table_path "../dataset/BULL-en/tables.json" \
    --input_dataset_path "../dataset/BULL-en/dev.json" \
    --output_dataset_path "./preprocessed_data/preprocessed_dev_en.json" \
    --db_path "../dataset/database_en" \
    --target_type "sql"



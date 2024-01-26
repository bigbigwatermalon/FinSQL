# This directory contains the code for the Parallel Cross Encoder method.
## The process of training and testing the model is as follows:
First preprocess the dataset: 
```shell
bash scripts/preprocessing_finsql.sh
```

Then train the Cross-Encoder model:
```shell
bash scripts/train_text2sql_schema_item_classifier_finsql.sh
```

At last, use the Cross-Encoder model to predict the dev set:
```shell
bash scripts/generate_text2sql_dataset_finsql.sh
```


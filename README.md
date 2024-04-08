# FinSQL: Model-Agnostic LLMs-based Text-to-SQL Framework for Financial Analysis
<center>
<img src="resources/BULL_ICON.png" alt="bull_icon" style="width:200px;" />
</center>
This repository contains the code and dataset for the paper FinSQL: Model-Agnostic LLMs-based Text-to-SQL Framework for Financial Analysis.

Before we start, we need to download the dataset and the database from [Google Drive](https://drive.google.com/file/d/1OtyFdH9cs-6bEVj8yKK4Zt53N52L_dBH/view?usp=sharing) and put them in the directory `dataset/`

Then the file structure should be like this:
```shell
. tree           
├── BULL-cn
├── BULL-en
├── README.md
├── database_cn
├── database_en
└── get_dev.py

```

Later, we need to preprocess the dataset

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

After we preprossing the dataset, we perform hybrid data augmentation: 

```shell
bash scripts/hybrid_augmentation.sh 
```

Then we start to train the LLM model: 

```shell
bash ds_sft.sh  
```


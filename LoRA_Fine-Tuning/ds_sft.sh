#!/bin/bash -l
#SBATCH -J sft
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -p a40
#SBATCH --gpus-per-node=1
#SBATCH --cpus-per-task=32


source /share/home/22251293/miniconda3/etc/profile.d/conda.sh
conda activate llama_peft


export GPUS_PER_NODE=1
export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=9901
echo $SLURM_JOBID
echo $GPUS_PER_NODE
echo $SLURM_NNODES
echo $SLURM_PROCID
echo $MASTER_ADDR
echo $MASTER_PORT
#exit
#srun --jobid $SLURM_JOBID bash -c 'python -m torch.distributed.run \
# --nproc_per_node $GPUS_PER_NODE --nnodes $SLURM_NNODES --node_rank $SLURM_PROCID \
# --master_addr $MASTER_ADDR --master_port $MASTER_PORT \
#src/train_bash.py \
#  --stage sft \
#  --model_name_or_path models/Baichuan2_13B \
#  --do_train \
#  --dataset ccks_cot_train_v1_ccks_fund,ccks_skeleton_train_v1_ccks_fund,ccks_synonymous_train_v1_ccks_fund,ccks_cot_train_v1_ccks_stock,ccks_skeleton_train_v1_ccks_stock,ccks_synonymous_train_v1_ccks_stock \
#  --finetuning_type lora \
#  --output_dir checkpoints/1114_Baichuan2_13B_ccks_cot_train_v1_ccks_fund_ccks_skeleton_train_v1_ccks_fund_ccks_synonymous_train_v1_ccks_fund_ccks_cot_train_v1_ccks_stock_ccks_skeleton_train_v1_ccks_stock_ccks_synonymous_train_v1_ccks_stock_8_epochs_qkv_all_targets_lora_1nodes \
#  --overwrite_cache \
#  --per_device_train_batch_size 4 \
#  --gradient_accumulation_steps 4 \
#  --lr_scheduler_type cosine \
#  --logging_steps 10 \
#  --save_steps 1000 \
#  --learning_rate 5e-5 \
#  --num_train_epochs 8.0 \
#  --plot_loss \
#  --fp16 \
#  --template vanilla \
#  --lora_target q_proj,k_proj,v_proj,W_pack,o_proj,gate_proj,up_proj,down_proj \
#  --deepspeed configures/deepspeed.json '
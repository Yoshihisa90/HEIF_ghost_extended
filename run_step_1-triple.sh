#!/bin/bash
#SBATCH -J encode_second

#SBATCH --mem=2G                                            # RAM requirements
#SBATCH --ntasks=1                                          # Tasks requirements
#SBATCH --cpus-per-task=1                                   # CPUs (i.e. cores) per task
#SBATCH --nodes=1                                           # Number of nodes (i.e. how many servers)

#SBATCH --mail-user=yoshihisa.furushita@unifi.it            # Email address of job owner
#SBATCH --output=logs/encode_second_%j_%N_%x_%A_%a.log              # Log file (regular output)
#SBATCH --error=logs/encode_second_%j_%N_%x_%A_%a.log               # Log file (error output)

#SBATCH --array=0-149

HEIC2HEVC=/data/lesc/staff/yoshihisa/Documents/heic2hevc/heic2hevc
INPUT_DIR=/Prove/Yoshihisa/HEIF_ghost/HEIF_IMAGES_LIBHEIF/HEIF_images_triple_largeQP2
OUTPUT_DIR=/Prove/Yoshihisa/HEIF_ghost/HEIF_IMAGES_265/HEIF_images_triple_largeQP2_265

source "/data/lesc/staff/yoshihisa/anaconda3/etc/profile.d/conda.sh"

./1-perform_encoding.py -heic "$HEIC2HEVC" -i "$INPUT_DIR" -o "$OUTPUT_DIR" run-triple ${SLURM_ARRAY_TASK_ID}

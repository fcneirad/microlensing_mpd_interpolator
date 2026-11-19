#!/bin/bash
#
#SBATCH --job-name=imf_doubles_mpd_19
#SBATCH --output=/home/fneira/output/imf_with_doubles/batch19_%A_%a.out
#SBATCH --error=/home/fneira/output/imf_with_doubles/batch19_%A_%a.err
#
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=8G
#SBATCH --gres=gpu
#
#SBATCH --array=0-1556
#SBATCH --export=ALL

mapfile -t myarray < input_files_list.txt

module load cuda/11.7.0
module load gcc/11.3.0
module load jsoncpp/1.9.5
module load cfitsio/4.2.0

# Argument is the path where the input_cpp.json is located
srun /home/fneira/jobs/imf_with_doubles/generate_mpd.sh ${myarray[29583+$SLURM_ARRAY_TASK_ID]}
#!/bin/bash
echo -e "Job started on $(date)\nSLURM_JOB_ID:SLURM_ARRAY_TASK_ID = $SLURM_JOB_ID:$SLURM_ARRAY_TASK_ID\nSLURM_NPROCS = $SLURM_NPROCS\nSLURM_CPUS_PER_TASK = $SLURM_CPUS_PER_TASK"
echo "working for $1 s ...";
yes > /dev/null &
ypid=$!
#srun yes > /dev/null &
#ypid2=$!
sleep "$1"
echo "killing job $ypid ..."
{ kill $ypid && wait $ypid; } 2>/dev/null
#echo "killing job $ypid2 ..."
#{ kill $ypid2 && wait $ypid2; } 2>/dev/null
echo -e "Job ended on $(date)"

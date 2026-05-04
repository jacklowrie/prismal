# High Performance Computing (HPC)

This directory contains job files to run on Purdue RCAC clusters.
We have access to Gilbreth.

## Jobs

- `chkenv.sub`: Example job file, shows how to load the conda env. More of a
  "hello, world!".
- `run_cafie.sub`: Runs the CAFIE algorithm on a test subset of 20 prompts using
  `google/gemma-3-1b`.

## running jobs

run with `sbatch <jobfile>`. Check status with `squeue -u <username>`.

## Writing job files

convention is `<job_name>.sub`, where `sub` is short for submit.

### Gilbreth

On Gilbreth, the partition, memory, nodes, gpus-per-node, and account seem to be
required. Time defaults to 30min, but specifying is smart (shorter jobs might
jump the queue, longer jobs need the spec).

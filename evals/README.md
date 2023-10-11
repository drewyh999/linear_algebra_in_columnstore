# Evaluation python scripts
Required python packages:
- PyMonetDB
- MatplotLib
- Numpy
- Pandas

## Comparing modified pipeline and original pipeline
The file `tranpose_pipeline_perf_eval.py` evaluates the clock time for a MonetDB pipeline to execute a relatively 
complex query for 1000 times. You can first checkout to the `forebear` branch and then run the script, after that checkout
to main branch then run again to test the difference of execution time.

## Comparing matrix multiplication performance and Numpy 
The file `mmu_perf_evals.py` calculates the square of a matrix in two different approaches, 
first one is extract the data from MonetDB then calculate using Numpy, second is to use the mmu and tra operation implemented

## Measure the transpose operation performance
The file `transpose_perf_eval.py` measures clock time of transpose operation with different size of relation
> CAVEAT: As the implementation has not really sort out the BAT garbage collection, the Maximum amount of 
rows of the operand of the transpose is around 1 million. The MonetDB will stop responding and complain too many
open files in the system after

## Gradient descent computation
The file `gradient_descent_eval.py` creates a procedure that computes gradient descent in linear regression and calls it 
to examine the correctness of the result also measures the performance
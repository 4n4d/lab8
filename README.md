# Lab 8: parallell beräkning av primtal
In this lab you will make two implementations of testing for primality, a serial implementation and a threaded implementation. You will then compare the two.

## Method
You can choose any method you like, but for simplicity you might want to look at Eratosthenes sieve.

## Serial implementation
Implement a straightforward test for primality for a number taken as an argument to your program. The output should be "prime" or "composite". 

## Threaded implementation
Next implement a threaded version of the same method as above! Use the Python module multiprocessing.

Investigate what speedup you can get on a multi-core computer (which most computers today are!) using your two implementations! 


## To present
* Code for a serial implementation of primality testing.
* Code for a threaded implementation of the same method as in 1.
* A graph showing the speedup as a function of problem size (the input number).


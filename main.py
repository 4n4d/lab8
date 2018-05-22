from multiprocessing import Process, Value, Array
import math
import time
import matplotlib.pyplot as plt

def serialIsPrime(n):
  # input integer n
  # output "prime" if n is prime, else "composite"

  # serial implementation using Eratosthenes sieve
  # i.e. create a list of primes up until n

  if not isinstance(n, int):
    raise SyntaxError

  if n < 1:
    raise SyntaxError 
  
  A = [True for i in range(n+1)]
  A[0] = False
  A[1] = False

  # generate a list that indicates if i is a prime or not by the sieve principle
  for i in range(2, int(math.ceil(math.sqrt(n)))+1):
    if A[i] == True:
      j = 2
      while j*i <= n:
        A[i*j] = False
        if i*j == n:    
          break
        j = j + 1
  
  if A[n] == False:
    return "composite"
  return "prime"

def sub_multiIsPrime(A, n, i, Rets):
  # inputs: A = shared value (Array), integer n, i = prime, Rets = shared value (short~)

  # This subroutine checks multiples of the prime i until i*j > n
  # It sets Rets = 1 iff i*j = n, i.e. n is a multiple of a prime and thus a composite number
  j = 2
  while j*i <= n:
    A[j*i] = 0
    if j*i == n:
      Rets=1
    j = j+1
  
def multiIsPrime(n,cores):
  # input integer n, integer cores
  # output "prime" if n is prime, else "composite"

  # cores is the number of concurrent processes that is allowed to run
  
  # multithreaded implementation using Eratosthenes sieve
  # idea: create one thread per prime less than ceil(sqrt(n))
  # for each such process, update the list of primes/composites

  # errorchecking
  if not isinstance(n, int):
    raise SyntaxError

  if n < 1:
    raise SyntaxError

  if not isinstance(cores, int):
    raise SyntaxError

  if cores < 1:
    raise SyntaxError

  # A is an array of size n+1 (i.e. from 0 to n)
  # Sets all values of A to 1 (where A[i]==1 means that i is a prime after the function has been fully executed)
  A = Array('h', n+1)
  for i in range(2,n+1):
    A[i] = 1 # all values >=2 are assumed to be prime
  A[0] = 0 # 0 is not a prime
  A[1] = 0 # 1 is not a prime

  pList = [] # this list will contain all the subprocesses that are initiated

  Rets = Value('h') # this is a shared value that is sent to the subroutine, when Rets == 1 it follows that n is a composite number
  Rets = 0 # this will always be 0 unless a process sets it to 1, then this process will end

  # loop from 2 to sqrt(n) 
  for i in range(2, int(math.ceil(math.sqrt(n)))+1):

    # we do not start a new subprocess if the current number of subprocesses equals "cores"
    # this while-statement will run until pList is smaller than cores, pList is reduced when a subprocess is finished
    while len(pList) == cores:
      
      # loop through the processes to find finished processes
      # we loop through the list backwards, this is so that we don't have to recalculate the index if any element of the list is deleted
      for c in range(cores-1, -1, -1):

        if not pList[c].is_alive():
          # we know that pList[c] has finished running

          if Rets == 1: # we can therefore check if Rets has been updated to 1 (this could have been done by any subprocess, but as soon Rets = 1 we know we can finish regardless
            return "composite"

          # if Rets != 1, delete the finished subprocess from the list to make room for a new subprocess
          del pList[c]

    # When we have reached this point, we know that there is room to append a new subprocess
    # If A[i] is a prime (== 1) start a new process
    # Occasionally, like for A[4], the subprocess for the prime 2 has not yet updated A[2*2]=0, such that a subprocess that checks for multiples of 4 is also started
    # this problem is just a waste of resources and should not cause any errors in the output.
    if A[i] == 1:
      # append the new process to pList
      pList.append(Process(target = sub_multiIsPrime, args=(A, n, i, Rets)))
      # start the last process
      pList[-1].start()


      
  # go through any remaining processes and make sure they finish processing
  for p in pList:
    p.join()

  # return the result
  if A[n] == 1:
    return "prime"
  return "composite"

  


def compositeTest():
  t0 = time.time()
  print multiIsPrime(100000, 4)
  print time.time() - t0

  t0 = time.time()
  print serialIsPrime(100000)
  print time.time() - t0



def primeTest():
  t0 = time.time()
  print multiIsPrime(32416190039,4)
  print time.time() - t0

  t0 = time.time()
  print serialIsPrime(32416190039)
  print time.time() - t0




def timeTest():
    
  t0 = time.time()
  print multiIsPrime(1000000, 4)     # ca 32.9 sekunder (10 milj)
  print time.time() - t0

  t0 = time.time()
  print serialIsPrime(1000000)       # ca 4.5 sekunder (10 milj)
  print time.time() - t0
                                      # dvs. ratio 32.9/4.5 = 7.3
                                      # ser ut som att det konvergerar
                                      # mot samma tid?
                                      # storsta skillnaden i alg. ar
                                      # att den inte slutar om den
                                      # hittar...
    



def plotTest(n, cores, cores2):
  TimesS = [0 for i in range(0, n+1)]
  TimesP = [0 for i in range(0, n+1)]
  TimesP2 = [0 for i in range(0, n+1)]

  for i in range(2, n+1):
    t0 = time.time()
    serialIsPrime(i)
    TimesS[i] = time.time() - t0

    t0 = time.time()
    multiIsPrime(i, cores)
    TimesP[i] = time.time() - t0

    t0 = time.time()
    multiIsPrime(i, cores2)
    TimesP2[i] = time.time() - t0
    


  line1 = plt.plot(range(2, n+1), TimesS[2:])
  line2 = plt.plot(range(2, n+1), TimesP[2:])
  line3 = plt.plot(range(2, n+1), TimesP2[2:])
  plt.legend(['Serial',
              'Multiprocessing '+ str(cores) +' cores',
              'Multiprocessing '+ str(cores2) +' cores'])
  plt.show()

  for i in range(2, n+1):
    TimesP[i] = TimesP[i]/(TimesS[i]*1.0)
    TimesP2[i] = TimesP2[i]/(TimesS[i]*1.0)

  plt.plot(range(2, n+1), TimesP[2:])
  plt.plot(range(2, n+1), TimesP2[2:])
  plt.legend(['Multiprocessing '+ str(cores) +' cores',
              'Multiprocessing '+ str(cores2) +' cores'])
  plt.show()



  
if __name__ == '__main__':
  n = 100
  cores = 4
  cores2 = 2
#  timeTest()
#  plotTest(n, cores, cores2)
#  primeTest()
  compositeTest()
#

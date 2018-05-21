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

def sub_multiIsPrime(A, n, i):
  # input Array, integer n, variable to be checked
  j = 2
  while j*i <= n:
    A[j*i] = 0
    j = j+1
  
def multiIsPrime(n):
  # input integer n
  # output "prime" if n is prime, else "composite"

  # multithreaded implementation using Eratosthenes sieve
  # idea: create one thread per integer less than ceil(sqrt(n))
  # for each such process, update the list of primes/composites

  if not isinstance(n, int):
    raise SyntaxError

  if n < 1:
    raise SyntaxError

  A = Array('h', n+1)
  for i in range(2,n+1):
    A[i] = 1
  A[0] = 0
  A[1] = 0
  pList = []
  j = 0
  
  for i in range(2, int(math.ceil(math.sqrt(n)))+1):
    if A[i] == 1:
      pList.append(Process(target = sub_multiIsPrime, args=(A, n, i)))
      pList[j].start()
      j = j + 1

  for p in pList:
    p.join()
      
  if A[n] == 1:
    return "prime"
  return "composite"
  #A = [True for i in range(n+1)]
  #A[0] = False
  #A[1] = False

  
  



if __name__ == '__main__':
  n = 10
  TimesS = [0 for i in range(0, n+1)]
  TimesP = [0 for i in range(0, n+1)]

#  print multiIsPrime(n)

  
  for i in range(2, n+1):
    t0 = time.time()
    serialIsPrime(i)
    TimesS[i] = time.time() - t0

    #if multiIsPrime(i) == "prime":
    #  print str(i) + ": is prime"

    t0 = time.time()
    multiIsPrime(i)
    TimesP[i] = time.time() - t0

#if serialIsPrime(i) == "prime":
#  print str(i) + ": " +  serialIsPrime(i)

#  for i in range(2, n+1):
#    print str(i) + ": " + str(TimesS[i]) + " secs."

  plt.plot(range(2, n+1), TimesS[2:])
  plt.plot(range(2, n+1), TimesP[2:])
  plt.show()

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
  # input Array, integer n, variable to be checked
  j = 2
  while j*i <= n:
    A[j*i] = 0
    if j*i == n:
      Rets=1
    j = j+1
  
def multiIsPrime(n,cores):
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

  Rets = Value('h')
  Rets = 0
  
  for i in range(2, int(math.ceil(math.sqrt(n)))+1):
    #if A[i] == 1:
    while len(pList) == cores:
      # loop through the processes to find finished processes
      for c in range(cores-1, -1, -1):
        if not pList[c].is_alive():
          if Rets == 1:
            return "composite"
#          print "deletes " + str(c)
#          print A[0:5]
          #if A[n] == 1:
          #  break
          del pList[c]
          j = j - 1

    if A[i] == 1:
#      print "sends: " + str(i) + " to process " + str(j)
      pList.append(Process(target = sub_multiIsPrime, args=(A, n, i, Rets)))
      pList[j].start()
      j = j + 1

  for p in pList:
    p.join()
      
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
  print multiIsPrime(10000000, 4)     # ca 32.9 sekunder (10 milj)
  print time.time() - t0

  t0 = time.time()
  print serialIsPrime(10000000)       # ca 4.5 sekunder (10 milj)
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
  plotTest(n, cores, cores2)
#  primeTest()
#  compositeTest()
#

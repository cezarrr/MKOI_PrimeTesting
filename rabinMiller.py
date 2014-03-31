__author__ = 'CJank'

import math
import random

def countNumberOfTestsWithEps(exponent, prob=4):
    """
    Zwraca najmniejsza liczbe k spelniajaca warunek 4**k>10**exponent

    Oznacza to, iz dla testu Rabina-Millera po wykonaniu k prob
    mamy p-stwo pierwszosci rozniace sie od 1 o mniej niz eps=10**(-exponent)

    Uwaga: tu exponent powinien byc dodatni!
    """

    k = math.log(10**exponent,4)
    k = math.ceil(k)
    return int(k)

def countEpsExpFromNumberOfTests(k, prob=4):
    """
    Zwraca taki wykladnik positiveExponent, ze 4**k>10**positiveExponent

    Oznacza to, iz dla testu Rabina-Millera po wykonaniu k prob
    mamy p-stwo pierwszosci rozniace sie od 1 o mniej niz eps=10**(-positiveExponent)
    """
    positiveExponent = math.log10(4**k)
    positiveExponent = math.floor(positiveExponent)
    return int(positiveExponent)


def findGreatestPowerOfTwo(n):
    """
    Znajduje liczby s,q takie, ze n-1==2**s * q, gdzie q nie dzieli sie przez 2
    s jest to najwieksza liczba, spelniajaca takie rownanie
    """
    s=0
    m = n-1
    endPoint = int(math.floor(math.sqrt(m)))

    for currS in xrange(endPoint,0,-1):
        q,modResult = divmod(m,2**currS)
        if(modResult==0):
            s=currS
            break
    return s,q


def testPrimalityLoop(n,witness,s,q):
    """
    Pojedynczy test dla liczby n i swiadka witness oraz liczb s i q takich,
    ze  n-1==2**s * q, gdzie q nie dzieli sie przez 2

    Zwraca True, gdy przypuszczamy pierwszosc
    Zwraca False, gdy potwierdzilismy zlozonosc
    """

    x = pow(witness,q,n) #potega modulo - duzo szybsza niz w**q % n
    if(x==1 or x == n-1):
        return True
    for r in xrange(1,s,1): #test Millera dla swiadka witness (s jest rozlacznie)
        x = pow(x,2,n)
        if(x==1):
             #poniewaz kwadratem 1 jest 1 to liczba jest zlozona
            return False #i wiemy to juz teraz - bez dalszych prob
        if(x==n-1):
            return True #kolejna glowna petla


    return False #jesli nigdzie nie wystapila reszta n-1

def rabinMillerNaive(n, k):
    """
    Wykonuje test sprawdzania pierwszosci liczby n (k razy)

    Swiadkowie sa wybierani losowo

    Wyjatki sa rzucane w wypadku wybrania blednej liczby
    """
    n = int(n) #wprost wskazujemy na int
    if (n<2):
        raise Exception("Number less then 3")
    if (n==2): #sytuacja wyjatkowa
        return True
    if (n%2==0):
        return False
    if (k>(n-3)):
        raise Exception("Too many iterations of test: k>n-3") #jesli jest mniej potencjalnych swiadkow niz iteracji testu

    probPrime = True
    witnessSet = set()
    s,q = findGreatestPowerOfTwo(n)

    #GLOWNA PETLA
    for currK in xrange(k): #wykonujemy k-razy
        while (True): #wykonujemy, az znajdziemy swiadka
            witness=random.randrange(2,n-2)
            if(witness not in witnessSet):
                witnessSet.add(witness)
                break


        res=testPrimalityLoop(n,witness,s,q)
        if(res):
            continue #jesli nie potwierdzilismy zlozonosci, to glowna petla
        else:
            return False #jesli udowodnilismy zlozonosc

    #jesli nigdzie nie znalezlismy dowodu, ze nie jest zlozona
    #zwracamy wynik, iz jest prawdopodobnie pierwsza
    return True


def rabinMillerForLargeNumbers(n,optK=10):
    """
    Wykonuje test sprawdzania pierwszosci liczby n

    Swiadkowie sa wybierani tak, aby potwierdzic z pewnoscia pierwszosc lub zlozonosc liczby n<341550071728321
    Swiadkowie dla odpowiednich n sa wybierani wedlug klucza z http://primes.utm.edu/prove/prove2_3.html

    Jesli liczba  n>341550071728321 uruchamiany jest test naiwny z optK powtorzeniami (swiadkami)

    Wyjatki sa rzucane w wypadku wybrania blednej liczby
    """
    n = int(n) #wprost wskazujemy na int
    if (n<2):
        raise Exception("Number less then 3")
    if (n==2): #sytuacja wyjatkowa
        return True
    if (n%2==0):
        return False
    if (optK>(n-3)):
        raise Exception("Too many iterations of test: k>n-3") #jesli jest mniej potencjalnych swiadkow niz iteracji testu



    if(n>=341550071728321): #jesli liczba jest wieksza od udowodnionej
        return rabinMillerNaive(n,optK)

    witnessSetToTry=set()

    #znane liczby
    if(n<1373653):
        witnessSetToTry = (2,3)
    elif(n<25326001):
        witnessSetToTry = (2,3,5)
    elif(n<118670087467):
        witnessSetToTry = (2, 3, 5, 7)
    elif(n<2152302898747):
        witnessSetToTry = (2, 3, 5, 7, 11)
    elif(n<3474749660383):
        witnessSetToTry = (2, 3, 5, 7, 11, 13)
    elif(n<341550071728321):
        witnessSetToTry = (2, 3, 5, 7, 11, 13, 17)

    #znane wyjatki od tej reguly
    if (n==3215031751):
        return False

    s,q = findGreatestPowerOfTwo(n)
    for w in witnessSetToTry:
        if (testPrimalityLoop(n,w,s,q)==False):
            return False

    return True

if __name__ == "__main__":
    """
    Testy
    """
    print (countNumberOfTestsWithEps(30)) #powinno byc 50
    print (countEpsExpFromNumberOfTests(50)) #30 - analogia do testu powyzej
    print(findGreatestPowerOfTwo(49)) #(4,3), bo 2**4==16, a 16*3 == 49-1
    print(findGreatestPowerOfTwo(289)) #(5,9), bo 2**5==32, a 32*9 == 289-1
    print(findGreatestPowerOfTwo(129)) #(7,1), bo 2**7==128==129-1

    print("\nTesty pierwszosci")
    numberOfIterations=10
    numbertToTest = [101,6277,7919, 341,561,2047,8911, 3215031751, 5394826801]
    print("\nRabin Miller z wybranymi swiadkami")
    for numb in numbertToTest:
        print(str(numb)+" jest pierwsza? "+str(rabinMillerForLargeNumbers(numb,numberOfIterations)))
    print("\nRabin Miller naiwny (losowi swiadkowie)")
    for numb in numbertToTest:
        testResult=rabinMillerNaive(numb,numberOfIterations)
        print(str(numb)+" jest pierwsza? "+str(testResult)),
        if(testResult):
            print("   Osiagniety epsilon na poziomie 10**-"+\
            str(countNumberOfTestsWithEps(numberOfIterations)))
        else: print ""

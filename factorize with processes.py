import math
import concurrent.futures
from time import time
from multiprocessing import cpu_count


def factorize(*args):
    res = []

    def func(n):
        return [i for i in range(1, int(n/2+1)) if n % i == 0] + [n]

    for c in args:
        res.append(func(c))

    return res


t_start = time()
a, b, c, d = factorize(128, 255, 99999, 10651060)

print('----------------------------------------------')
print(f'Time without processes = {time() - t_start}')
print('----------------------------------------------')


PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

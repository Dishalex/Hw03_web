from time import time

def func(n):
    return [1] + [i for i in range(2 + (n % 2), int(n/2 + 1)) if n % i == 0] + [n]


def factorize(*args):
    res = []
    for c in args:
        res.append(func(c))

    return res



if __name__ == "__main__":        
    t_start = time()
    a, b, c, d, *e  = factorize(128, 255, 99999, 10651060, 106510601, 106510602, 106510603)
    print(f'Time without processes = {time() - t_start}')
    print('----------------------------------------------')
    
    print(a, b, c, d, *e, sep='\n')
    
    
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


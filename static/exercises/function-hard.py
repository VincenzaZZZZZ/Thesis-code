def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def primes_below(n):
    primes = []
    for p in range(2, n):
        if is_prime(p):
            primes += [p]
    return primes

def prime_factors(n):
    factors = []
    for prime in primes_below(n):
        while n % prime == 0:
            factors += [prime]
            n //= prime
    return factors

num = int(input("Please enter an integer: "))

print("The number %d can calculated by the following multiplication of prime numbers:" % num)

product = ""
for factor in prime_factors(num):
    product += " * " + str(factor)

print(product[3:])
-- IN?
isin :: Integer -> [Integer] -> Bool
isin e l
    | null l = False
    | e == l!!0 = True
    | otherwise = isin e (tail l)

-- DIVISORS
divisors :: Integer -> [Integer]
divisors u = [v | v <- [1 .. u], mod u v == 0]

-- PRIME
prime :: Integer -> Bool
prime x = divisors x == [1, x]

-- Dr. Mota's isPrime
isPrime :: Integer -> Bool
isPrime n
    | n <= 1 = False
    | n == 2 = True
    | otherwise = null [k | k <- [2 .. n-1], mod n k == 0]

-- Mota's Greatest common divisor
gcd2 :: Integer -> Integer -> Integer
gcd2 a b
    | b == 0 = a
    | a < b = gcd b a
    | otherwise = gcd b (a `mod` b)

-- GCD
-- ngcd :: Integer -> Integer -> Integer
-- ngcd a b
--     | 

-- COPRIME
coprime :: Integer -> Integer -> Bool
coprime c d = gcd c d == 1

-- Mota's Co-Prime
-- coprime2 :: Integer -> Integer -> Bool
-- coprime2 a b
--     | Main.gcd a b == 1 = True
--     | otherwise = False

-- Mota's totienPhi
totienPhi :: Integer -> Int
totienPhi m = length [ r | r <- [1 .. m], coprime m r ]

-- PRIMEFACTORS
primeFactors :: Integer -> [Integer]
primeFactors h = [i | i <- divisors h, prime i]


-- Mota's NDIV (how many times one number divides another, like, exponent-style)
ndiv a b
    | mod a b /= 0 = 0
    | otherwise = 1 + ndiv ( div a b ) b

-- Mota's PrimeFactorsMult
primeFactorsMult :: Integer -> [ (Integer, Integer) ]
primeFactorsMult n = [ (p, ndiv n p) | p <- primeFactors n ]

-- primesRange
primesRange :: Integer -> Integer -> [Integer]
primesRange b e = [p | p <- [b .. e], prime p]

-- GOLDBACH'S CONJECTURE
goldbach :: Integer -> [ (Integer, Integer) ]
goldbach x = [(a, b) | mod x 2 == 0, b <- primesRange 2 x, a <- primesRange 2 x, a + b == x, a >= b]

-- Mota's Goldbach
moldbach :: Integer -> [(Integer, Integer)]
moldbach n = [ (p1, p2) | n `mod` 2 == 0, p1 <- [2 .. n-1], isPrime p1, p2 <- [p1 .. n-p1], isPrime p2, p1 + p2 == n ]

-- GOLDBACH LIST
-- goldbachList :: [Integer] -> [Integer] -> [Integer [(Integer, Integer)]]
goldbachList r = [(i, l) | i <- r, l <- goldbach i]

main = print((moldbach 2048))

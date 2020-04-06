-- I to tha izz-O yeah make it work like in and out
-- "Actions happening in sequence"
-- Pure functions don't like interacting with the outside world,
-- so Haskell made up a special "IO" type that's allowed to git durrrrty
-- These shits have side effects bro, like shitting on the output console
-- I/O actions could also "contain" a return value
-- So you wanna do it write, you use putStr
-- putStr :: String -> IO()
-- putStrLn :: String -> IO()
-- But then a read do it otherwayround
-- getLine :: IO String

-- What a Main is?
main = do
    putStr "What's your name? "
    name <- getLine
    putStrLn ("Nice to eat you, " ++ name ++ ".")
 -- Remember how '=' isn't the assignment operator
 -- '<-' is for assignment, like R's "gets"
 -- Curly braces can be used, if you're a bitch

-- Lists are a thing
-- Can be built w/ enumerations, like [a .. z]
-- which is the list (a, b, c, ..., x, y, z)
-- You can set it up with a patternj, such as
-- [1, 3 .. 10]
-- [1, 3, 5, 7, 9]
-- or put functions in it like
-- [n, n+p .. z] (or whatever)
-- It can even be infinite - [0..] would be all the natural numbers
-- so if you wanted a "while True" style operation, you could use a
-- counter that just basically NEVER ENDS FOREVER
-- Because "delayed interpretation" or something
-- Also works with letters - ['a' .. 'z']

-- Haskell also has list comprehensions
ex = [2, 4, 7]
xe = [ 2*n | n <- ex ]
-- so "[<expression> | <get variable> <- <from list>]"
-- Can include conditions
xev = [ 2*n | n <- ex, even n]
-- ... would give you 2*n for only those n vals in ex which are even
-- [ <expression> | <get variable> <- <from list>, <if condition> ]

import Data.Char
digits :: [Char] -> [Char]
digits s = [c | c <- s, isDigit c]
maing = print(digits "sap1en5") -- returns 15

-- check this shit out
ix = [(i,j) | i <- [1..5], even i, j <- [i..5]]
-- LOOK AT THAT LAST RANGE, IT STARTS WITH AN "i"
-- IT IS A CASCA DE BANANA
-- THAT MEANS YOU WILL FAIL TO NOTICE IT AND SLIP
-- AND POSSIBLY DIE
-- But actually it's working like a nested loop, so you reevaluate i each time

xbarf = [x | xs <- [[(3,4)], [(5, 4), (3, 2)]], (3, x) <- xs]
-- Shit cray
-- x = [4, 2] for some reason

-- DIVISORS
divisors u = [v | v <- [0 .. u], mod u v == 0]]

-- MAP
another_map f l = [f r | r <- l]

-- PRIME
prime x = divisors x == [1, x]

-- now [x | x <- [0 .. 100], prime x] returns
-- [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
-- like a Goddamn boss

-- Haskell can also do it lists with a thing he call "filter" - 
-- it's like map, but just for keeping some elements
filtre l f = [k | k <- l, f k]
-- now I can be all like
filtre [0 .. 100] prime
-- and get that same list from before of primes what are
-- [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
-- But I guess note that 'map' and 'filter' are already built in,
-- so rewriting them doesn't make you especially clever
-- still tho


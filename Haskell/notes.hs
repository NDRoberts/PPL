x = 5
-- You cannot declare a variable twice in Haskell; it just is what it is
-- x = "Manoots" -- This throws an error if uncommented

-- = is the "value-naming operator", not so much the assignment operator
-- '--' is the start of a comment bee tee dubs
{- This is what a block comment looks like 
   Like if I wanted to have a lot of lines in a comment
   Like, a lot maybe
   More than this
   Yeah this looks good -}
l1 = [1, 2, 3]
l2 = [4, 5, 6]
l3 = l1 ++ l2 -- This concatenates two lists
k = l1!!0 -- This gives us list l1, object at index 0

l = head l3 -- just the first element of l3
m = tail l3 -- everything but the head of l3

{- Haskell loves higher-order functions.
   "::" reads as "has type"
   f :: X -> Y
   means "f takes X and returns Y"
   like "sin :: float -> float" 
   So we calls this a 'type definition' of a function: -}
inc :: Integer -> Integer
inc x = x + 1

add :: (Integer, Integer) -> Integer
add x = fst x + snd x
-- x refers to the whole LHS of the definition; "fst x" means "first x", "snd x" means "second x"
-- Yeah it's as stupid as you think it is

main = print(inc(4), add((5, 4)))

-- Now there's some shit about curried form?  Like, what?

add' :: Integer -> Integer -> Integer
add' x y = x + y
-- TF does this even mean, "serializing the arguments"

-- Pattern matching also is good betimes
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)
-- Such patterns, recurse me jolly wompus

-- But also there is "guards"?
factorial :: Integer -> Integer
factorial n
   | n == 0 = 1
   | otherwise = n * factorial(n - 1)
-- You can make it like a IF-ELSE guy

-- These type definitions of functions are optional by the way
-- Just thought you might like to know

{- So here's the story with currying
   We are gonna make like it's just a wacky notation
   Like, instead of a function taking "(a, b)" as input,
   we can say it takes "a -> b" instead
   But it basically is the same right
   See
   Because reasons
   I mean obviously it is not that
   Like, at all
   But for now IDGAF
-}
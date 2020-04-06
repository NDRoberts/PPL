import Data.List

-- MYLAST
myLast l = l !! (length l)

-- SecondTwoLast!?
secondToLast l = (myLast . myLast) l

-- elementAt
elementAt l k = l!!(k-1)

-- myLength
myLength l
    | null l = 0
    | otherwise = myLength (tail l) + 1

-- myReverse
myReverse :: [Integer] -> [Integer]
myReverse l
    | (not.null) l = (last l):(myReverse (init l))
    | otherwise = []

-- Middle (as in not first or last)
middle w = drop 0 (drop ((length w) - 1) w)

-- isPalindrome werd
--     | length werd <= 1 = True
--     | first werd /= last werd = False
--     | otherwise = isPalindrome (middle werd)

-- Mota's myAll
-- mallm p lst = and [ p el | el <- lst ]

-- Doin' a thing in parallel
-- Note that this requires a package that YOU DON'T KNOW ABOUT
-- pears a b = [(i, j) | i <- a | j <- b]


main = do
    let myList = [ 1, 3 .. 11]
    print(middle myList)
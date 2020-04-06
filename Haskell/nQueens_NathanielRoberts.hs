import Data.List

type Seq = [Char]
type Board = [Seq]

-- TESTING GUY SO I DON'T HAVE TO RETYPE EVERY DANG TIME
test = [ ['a','b','c','d'],
         ['e','f','g','h'],
         ['i','j','k','l'],
         ['m','n','o','p'] ]
badBoard = [ ['Q','Q','Q','Q'],
             ['Q','Q','Q','Q'],
             ['Q','Q','Q','Q'],
             ['Q','Q','Q','Q'] ]

splitUp l n
    | length l > 0 = (take n l):splitUp (drop n l) n
    | otherwise = []

getCols b = [l !! n | n <- [0 .. (length b) - 1], l <- b]

-- TODOne: setup
setup :: Int -> Board
setup n = take n (repeat (take n (repeat '-')))

-- TODOne: rows
rows :: Board -> Int
rows b = length b

-- TODOne: cols
cols :: Board -> Int
cols b
    | length (maximum b) == length (minimum b) = length (b !! 0)
    | otherwise = 0

-- TODOne: size
size :: Board -> Int
size b
    | rows b == cols b = length b
    | otherwise = 0

-- TODOne: queensSeq
queensSeq :: Seq -> Int
queensSeq s = sum [1 | c <- s, c == 'Q']

-- TODOne: queensBoard
queensBoard :: Board -> Int
queensBoard b = sum [queensSeq s | s <- b]

-- TODOne: seqValid
seqValid :: Seq -> Bool
seqValid s = queensSeq s <= 1

-- TODOne: rowsValid
rowsValid :: Board -> Bool
rowsValid b = all (==True) [seqValid s | s <- b]

-- TODOne: colsValid
colsValid :: Board -> Bool
colsValid b = all (==True) [seqValid s | s <- (splitUp (getCols b) (length b))]

-- TODOne: diagonals
diagonals :: Board -> Int
diagonals b = (size b) * 2 - 1

-- TODOne: allMainDiagIndices
-- singleMainDiagIndices :: Board -> Int -> [ (Int, Int) ]
-- singleMainDiagIndices b i = [ (x, y) | x <- [0 .. (size b)-1], y <- [0 .. (size b)-1], (x - y) == (diagonals b) - (size b) - i]
allMainDiagIndices :: Board -> [[ (Int, Int) ]]
allMainDiagIndices b = [ [ (x, y) | x <- [0 .. (size b) - 1], y <- [0 .. (size b) - 1], (x - y) == (diagonals b) - (size b) - i] | i <- [0 .. diagonals b - 1] ]

-- TODOne: mainDiag
mainDiag :: Board -> [Seq]
mainDiag b = [ [b !! fst x !! snd x | x <- l ] | l <- (allMainDiagIndices b) ]

-- TODOne: allSecDiagIndices
allSecDiagIndices :: Board -> [[ (Int, Int) ]]
allSecDiagIndices b = [ [ (x, y) | y <- [0 .. (size b) - 1], x <- [0 .. (size b) - 1], x + y == i] | i <- [0 .. diagonals b - 1] ]

-- TODOne: secDiag
secDiag :: Board -> [Seq]
secDiag b = [ [b !! fst x !! snd x | x <- l ] | l <- (allSecDiagIndices b) ]

-- TODOne: diagsValid
diagsValid :: Board -> Bool
diagsValid b = all (==True) ([seqValid m | m <- mainDiag b] ++ [seqValid n | n <- secDiag b])

-- TODOne: valid
valid :: Board -> Bool
valid b = rowsValid b && colsValid b && diagsValid b

-- TODOne: solved
solved :: Board -> Bool
solved b = valid b && queensBoard b == size b

-- Part 4
-- TODOne: setQueenAt
setQueenAt :: Board -> Int -> [Board]
setQueenAt b i = [
    [b !! r | r <- [0 .. (i - 1)]] ++ [ [b !! i !! p | p <- [0 .. n-1]] ++ ['Q'] ++ [b !! i !! q | q <- [n+1 .. (size b) - 1], q < (size b)] ] ++ [b !! s | s <- [(i + 1) .. (size b) - 1] ] | n <- [0 .. (size b) - 1]]

-- TODOne?: nextRow
nextRow :: Board -> Int
nextRow b = ([n | n <- [0 .. (size b) - 1], queensSeq (b !! n) < 1] ++ [-1]) !! 0

-- TODOne-ish: solve
solve :: Board -> [Board]
solve b = [q | q <- permutations [(setQueenAt b 0) !! n !! 0 | n <- [0 .. (size b) - 1]], solved q == True]
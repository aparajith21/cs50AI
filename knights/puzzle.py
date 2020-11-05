from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

#Input to knowledge:
#A is a knight or a knave. If A is a knight, then it isn't a knave, and if A is a knave, it isn't a knight. From what A says, if A is a knight, then A is a knight and a knave, and if A is a knave, then A is not both, a knight and a knave.
knowledge0 = And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight)), Implication(AKnight, And(AKnight, AKnave)), Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

#Input to knowledge:
#A is a knight or a knave. If A is a knight, then it isn't a knave, and if A is a knave, it isn't a knight. Same applies to B. Based on what A says, if A is a knave, then B is not a knave and if A is a knight, then A and B are both knaves.
knowledge1 = And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight)),Or(BKnight, BKnave), Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight)), Implication(AKnave, Not(BKnave)), Implication(AKnight, And(AKnave, BKnave))
    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

#Input to knowledge:
#A is a knight or a knave. If A is a knight, then it isn't a knave, and if A is a knave, it isn't a knight. Same applies to B. Based on what A says, if A is a knight, then A and B are both knights or both knaves and if A is a knave, then A is a knave and B is a knight or A is a knight and B is a knave.
# Based on what B says, if B is a knight, then B is a knight and A is a knave or A is a knight and B is a knave. If B is a knave, then A and B are both knights or A and B are both knaves.
knowledge2 = And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight)),Or(BKnight, BKnave), Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight)), Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), Implication(AKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave))), Implication(BKnight, Or(And(BKnight, AKnave), And(AKnight, BKnave))), Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
    
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

#Input to knowledge:
# A is a knight or a knave. If A is a knight, then it isn't a knave, and if A is a knave, it isn't a knight. Same applies to B and C.
# If A is a knight, then A is a knight or a knave, and if A is a knave, then A is not a knight or a knave. If B is a knight then A is a knave and A is a knight. If B is a knight, then C is a knave. If C is a knight, then A is a knight. If C is a knave, then A is a knave. 
knowledge3 = And(Or(AKnight, AKnave), Implication(AKnight, Not(AKnave)), Implication(AKnave, Not(AKnight)), Or(BKnight, BKnave), Implication(BKnight, Not(BKnave)), Implication(BKnave, Not(BKnight)), Or(CKnight, CKnave), Implication(CKnight, Not(CKnave)), Implication(CKnave, Not(CKnight)), Implication(AKnight, Or(AKnight, AKnave)), Implication(AKnave, Not(Or(AKnight, AKnave))), Implication(BKnight, Biconditional(AKnave, AKnight)), Implication(BKnight, CKnave), Implication(CKnight, AKnight), Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

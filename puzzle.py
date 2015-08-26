#!/usr/bin/env python3

import random

weights = [2] * 12
which = random.randrange(1, 13)
heavier = random.randrange(0, 2) == 0
weights[which - 1] = 1.5 + heavier

for turn in range(3):
    left = [int(x.strip()) for x in input("Enter marbles to weigh in left side of balance, space-separated\n").split(" ")]
    right = [int(x.strip()) for x in input("Enter marbles to weigh in right side of balance, space-separated\n").split(" ")]

    left_weight = sum([weights[i - 1] for i in left])
    right_weight = sum([weights[i - 1] for i in right])

    if left_weight > right_weight:
        print("Left side is heavier!")
    elif left_weight < right_weight:
        print("Right side is heavier!")
    else:
        print("Sides are equal!")

    print()

guess = int(input("Which marble? "))
heavier_guess = input("Heavier or lighter? ").lower() == "heavier"

if guess == which and heavier_guess == heavier:
    print("Correct!")
else:
    print("Incorrect!")



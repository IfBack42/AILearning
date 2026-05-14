import random
score_person = 0
score_com = 0
i = 0
while i < 5:
    your_choice = int(input("玩家选择那个方向射门:0-左路/1-右路/2-中路:"))
    if 0 <= your_choice <= 2:
        print(f"You have chose:{your_choice}")
        com_choice = random.randint(0, 2)
        print(f"computer has chose {com_choice}")
        if your_choice == com_choice:
            score_com += 1
            print("computer win a score")
            print("-" * 20)
        else:
            score_person += 1
            print("you win a score")
            print("-" * 20)
    else:
        print("夏季吧踢我让你飞起来")
        break
    i += 1
print(f"your final score is :{score_person}")
print(f"computer's final score is :{score_com}")
if score_person > score_com:
    print("you win")
else:
    print("you lose")


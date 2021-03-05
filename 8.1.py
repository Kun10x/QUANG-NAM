from random import randint
player_score = 0
computer_score = 0
def main():
	global player_score, computer_score
	player = input("Select: Rock, Paper, Scissor?:")
	computer = randint(0,2)

	if computer == 0:
		computer = "rock"
	if computer == 1:
		computer = "raper"
	if computer == 2:
		computer = "scissor"
	print("___")
	print("You choose:" + player)
	print("computer chooses:" + computer)
	print("___")
	if player == computer:
		print("Draw")
	else:
		if player == "rock":
			if computer =="scissor":
				print("Lose")
				computer_score +=1
				return False
			else:
				print("Win")
				player_score +=1
				return True
		elif player == "paper":
			if computer =="scissor":
				print("Lose")
				computer_score +=1
				return False
			else:
				print("Win")
				player_score +=1
				return True
		elif player == "scissor":
			if computer =="rock":
				print("Lose")
				computer_score +=1
			else:
				print("Win")
				player_score +=1
				return True
		else:
			print("Try Again")
			main()

def main2():
	for i in range(5):
		main()
	print("Total player_score:", player_score, "\nTotal computer_score:", computer_score)
	if player_score > computer_score:
		print("YOU WINNNNNNNNN")
	elif player_score == computer_score:
		print("Draw")
	else:
		print("YOU LOSE :(((")

main2()

import requests
import time
from os import system, name 
from pprint import pprint
condition = 'y'

def print_wait():
	wait_symbols = [' ','—','\\','|','/','—','\\','|','/','—','\\','|','/',' ']
	for i in wait_symbols:
		print(i, end='\r')
		time.sleep(0.1)

def get_moves(pokemon, poke_data):
	print('\nWelcome to the Pokémon Move Library!\nNow getting information about ' + pokemon.title() + '\'s moves.')
	print_wait()

	#Get move list
	poke_moves = [x['move']['name'] for x in poke_data['moves']]
	new_poke_moves = []

	#Create nice-looking list for user selection
	for i in range(0, len(poke_moves)):
		move = str(i) + ': ' + poke_moves[i]
		new_poke_moves.append(move.title())

	#Get URL for move
	print(*new_poke_moves, sep = '\n')
	user_move = int(input('\nWhat move do you want to learn more about? (Select number from the list above): '))

	#Add a little suspense by making the computer "think"
	print('\nThank you. Now getting information for ' + poke_moves[user_move].title() + '. ')
	print_wait()

	move_url = poke_data['moves'][user_move]['move']['url']
	#---------------------------------------------------#

	#---------------------------------------------------#
	#Access move API
	move_res = requests.get(move_url)
	move_data = move_res.json()

	#Get pertinent info about the move
	move_accuracy = str(move_data['accuracy'])
	move_type = move_data['type']['name']
	move_power = str(move_data['power'])

	print('Type: ' + move_type.title() + '\nPower: ' + move_power + '\nAccuracy: ' + move_accuracy + '\n')

def clear(): 
	# for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def get_type(pokemon, poke_data):
	types_nice = []
	print('Getting information about ' + pokemon.title() + '\'s type.')
	print_wait()

	# Function for getting information about a specific Pokémon Type
	def type_information(pokemon, user_type_url):

		# Get type information from API
		type_data = requests.get(user_type_url).json()
		this_type = type_data['name']

		# Get double_damage_from types
		double_damage_from = []
		for i in type_data['damage_relations']['double_damage_from']:
			double_damage_from.append(i['name'])

		# Get "resistant to" types
		half_damage_from = []
		for i in type_data['damage_relations']['half_damage_from']:
			half_damage_from.append(i['name'])

		# Get "double damage to" types
		double_damage_to = []
		for i in type_data['damage_relations']['double_damage_to']:
			double_damage_to.append(i['name'])

		half_damage_to = []
		for i in type_data['damage_relations']['half_damage_to']:
			half_damage_to.append(i['name'])

		clear()
		print(this_type.title() + ' is:')
		print('• Super-effective against: ' + ', '.join(double_damage_to))
		print('• Weak against: ' + ', '.join(half_damage_to))
		print('• Susceptible to attacks from: ' + ', '.join(double_damage_from))
		print('• Resistant to attacks from: ' + ', '.join(half_damage_from))

	#Get types of Pokémon and create a list
	#with each list item being a 2-item list with the type and API URL for that type
	for i in poke_data['types']:
		i_type = [i['type']['name'],i['type']['url']]
		types_nice.append(i_type)
		#insert friction here

	# Present information to user and ask if they want type matchup information
	if len(types_nice) == 1: # if a single-type Pokémon
		print(pokemon.title() + '\'s type is ' + types_nice[0][0].title() + '.')
		type_continue = input('Would you like to see information about this type? (y/n): ')
		user_type_url = types_nice[0][1]
		type_information(pokemon, user_type_url)

	else: # if a multi-type Pokémon
		# print out types for the user and allow them to make a selection
		printable_types = []
		for i in types_nice:
			printable_types.append(i[0])
		print(pokemon.title() + ' has ' + str(len(types_nice)) + ' types. They are ' + ' and '.join(printable_types) + '.')
		print('Which type would you like to learn about?')
		x = 0
		for i in types_nice:
			print(str(x) + ': '+ i[0].title())
			x += 1
		user_type = int(input('Choose the number of the type that you wish to learn about: '))
		user_type_url = types_nice[user_type][1]
		type_information(pokemon, user_type_url)



print('Thank you for using the Comprehensive Pokémon Information Service.')

while condition == 'y':
	#Initial user input
	clear()
	pokemon = input('Input your desired Pokémon: ')

	#Get data
	poke_res = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon.lower())
	poke_data = poke_res.json()

	print('What would you like to investigate?\n1. Type Matchups\n2. Evolution Information\n3. Move Sets')
	selection = int(input('Choose your option: '))
	
	#User selects their desired information request
	if selection == 1: #Type Matchup
		clear()
		get_type(pokemon, poke_data)
		condition = input('Would you like to continue? (y/n): ')

	elif selection == 2: #Evolution Information
		clear()
		print('\nDevelopment in Progress')
		condition = input('Would you like to continue? (y/n): ')

	elif selection == 3: #Move Sets
		clear()
		get_moves(pokemon, poke_data)
		condition = input('Would you like to continue? (y/n): ')

	else:
		clear()
		print('You have entered an invalid selection. Please try again.\n')

print('Thank you for using the Comprehensive Pokémon Information Service. Have a nice day!')
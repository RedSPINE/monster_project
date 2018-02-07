# !/usr/bin/env python
# -----------------------------------------------
__author__ = "Duc Minh TRAN, Tao Duy Chuan LE"
__version__ = "0.0.1"
# -----------------------------------------------

import math
import generation as gen
import random

# HAND VITESSE (TOUR/Second)
VITESSE_SECONDHAND = 1. / 60
VITESSE_MINUTEHAND = 1. / 3600
VITESSE_HOURHAND = 1. / 43200

# POINTS FOR CONNECTIONS
GEAR_Z_GEAR = 5
GEAR_XY_GEAR = 5
GEAR_Z_HAND = 15
SPRING_Z_BARREL = 50
FORK_XY_ESCAPE_WHEEL = 50
BALANCEWHEEL_XY_FORK = 50
BARREL_XY_GEAR = 50
SPRING_Z_BALANCEWHEEL = 50
GEAR_XY_ESCAPE_WHEEL = 20
# INITIAL VITESSE
VITESSE_INITIAL = 1/60

wanted_pieces = {
	"Barrel" : 1, 
	"Fork" : 1, 
	"EscapeWheel" : 1, 
	"BalanceWheel" : 1,
	"Spring" : 2,
	"Hand" : 3
}

COMPONENT_COST = 3
UNIQUE = 50

#NUMBER OF GENERATIONS:
NUMBER_GENERATIONS = 1000
NUMBER_CROSSING = 100

class Connection():
    """
    __init__() functions as the class constructor
    """
    def __init__(self, name=None, point=0):
        self.name = name
        self.point = point


valid_connections = []


def input_database():
	"""
	Function allows to create a list (more like database) of possible connections in a clock, and give a value to all of them
	"""

	valid_connections.append(Connection(["Gear", "Gear", gen.Z_CONNECTION], GEAR_Z_GEAR))

	valid_connections.append(Connection(["Gear", "Gear", gen.XY_CONNECTION], GEAR_XY_GEAR))

	valid_connections.append(Connection(["Gear", "Hand", gen.Z_CONNECTION], GEAR_Z_HAND))
	valid_connections.append(Connection(["Hand", "Gear", gen.Z_CONNECTION], GEAR_Z_HAND))

	valid_connections.append(Connection(["Fork", "EscapeWheel", gen.XY_CONNECTION], FORK_XY_ESCAPE_WHEEL))
	valid_connections.append(Connection(["EscapeWheel", "Fork", gen.XY_CONNECTION], FORK_XY_ESCAPE_WHEEL))

	valid_connections.append(Connection(["BalanceWheel","Fork", gen.XY_CONNECTION], BALANCEWHEEL_XY_FORK))
	valid_connections.append(Connection(["Fork", "BalanceWheel", gen.XY_CONNECTION], BALANCEWHEEL_XY_FORK))

	valid_connections.append(Connection(["EscapeWheel", "Gear", gen.XY_CONNECTION],GEAR_XY_ESCAPE_WHEEL))
	valid_connections.append(Connection(["Gear", "EscapeWheel", gen.XY_CONNECTION], GEAR_XY_ESCAPE_WHEEL))

	valid_connections.append(Connection(["Spring", "Barrel", gen.Z_CONNECTION], SPRING_Z_BARREL))
	valid_connections.append(Connection(["Barrel", "Spring", gen.Z_CONNECTION], SPRING_Z_BARREL))

	valid_connections.append(Connection(["Spring", "BalanceWheel", gen.Z_CONNECTION], SPRING_Z_BALANCEWHEEL))
	valid_connections.append(Connection(["BalanceWheel", "Spring", gen.Z_CONNECTION], SPRING_Z_BALANCEWHEEL))

	valid_connections.append(Connection(["Barrel", "Gear", gen.XY_CONNECTION], BARREL_XY_GEAR))
	valid_connections.append(Connection(["Gear", "Barrel", gen.XY_CONNECTION], BARREL_XY_GEAR))


def find_connections(piece, connection_list):
	# Used by group connections, returns every connection for a given piece, always put the chosen piece before in the connection trinome
	connections = []
	for i in range(len(connection_list)):
		if piece in connection_list[i]:
			if piece == connection_list[i][1]:
				connection_list[i][0], connection_list[i][1] = connection_list[i][1], connection_list[i][0]
			connections += [connection_list[i]]
	return connections


def group_connections(clock):
	# Returns a big list of connections, redundant, ordered by piece
	connection_list = gen.list_connections(clock)
	cn_group = []
	for piece in clock[1:]:
		cn_group += [find_connections(piece, connection_list)]
	return cn_group


def find_chains(connection_list):
	chains = []
	for cn in connection_list:
		chain = [cn]
		piece0 = cn[0]
		piece1 = cn[1]
		end_flag = False
		while not end_flag:
			end_flag = True
			for cn1 in connection_list:
				used_pieces = [x for c in chain for x in c]
				if (piece0 in cn1 or piece1 in cn1) and (not (piece0 in cn1 and piece1 in cn1)) and (not cn1 in chain): # <=> piece0 in cn1 XOR piece1 in cn1
					chain += [cn1]
					piece0 = cn1[0]	
					piece1 = cn1[1]
					end_flag = False
		chains += [chain]
	return chains


def gears_XY_connection(obj1,obj2):
	""" 
	2 gears connected by teeths,if gear1 spins will train gear 2 to spin
	"""
	if (obj1.y_position == obj2.y_position) and (obj2.x_position == obj1.x_position) and distance_between_objs(obj1, obj2) < PIN_DISTANCE and (obj1.is_rotate() or obj2.is_rotate()):
		obj2.rotates = True
		obj2.speed = gear1.speed * gear1.nb_teeth / gear2.nb_teeth


def objects_Z_connection(obj1,obj2):
	"""
	If 2 objects in the same axe, obj1 will train vitesse to obj2
	"""
	if obj1.z_position == obj2.z_position :
		if obj1.is_rotate():
			obj2.rotates = True
			obj2.speed = obj1.speed


def is_rotate(obj):
	if obj.speed != 0:
		return True
	return False


def initial_clock_run(clock):
	# INPUT : LIST OF OBJECTS OF A CLOCK
	# OUTPUT : IF THE CLOCK RUNS< INITIALIZE THE MOVEMENT OF ESCAPE WHEEL.
	connection_list = gen.list_connections(clock)
	if does_clock_run(connection_list):
		for i in range(1, len(clock)):
			if clock[i].__class__.__name__ == "EscapeWheel":
				clock[i].speed = VITESSE_INITIAL


def is_in_connectdata(connection):
	# INPUT : A list type [object, object, type of connection]
	# OUTPUT : A Point correspond with the connection in valid_connections, 0 if the input connection doesn't appear in valid_connections
	x = [connection[0].__class__.__name__, connection[1].__class__.__name__, connection[2]]
	for i in range(len(valid_connections)):
		# THIS STEP COMPARES NAME OF OBJECT1, NAME OF OBJECT2, TYPE OF CONNECTION
		if (x[0]==(valid_connections[i].name)[0]) and (x[1]==(valid_connections[i].name)[1]) and (x[2]==(valid_connections[i].name)[2]):
			return valid_connections[i].point

	return (-15)


def fitness(clock):
	"""
	INPUT : A LIST OF CONNECTION OF A CLOCK
	OUTPUT: FITNESS SCORE OF THAT CLOCK
	This part gives score based on connections in a clock that appears in valid_connections
	"""
	connection_list = gen.list_connections(clock)
	groups = group_connections(clock)
	score = 0

	# Each component reduces the fitness score
	score = score - (COMPONENT_COST * (len(clock) - 1)) 

	# For each unique piece, give point only if it has one occurence in the watch
	for name in wanted_pieces:
		nb_of_this_piece = 0
		for piece in clock[1:]:
			if piece.__class__.__name__ == name :
				nb_of_this_piece += 1
		if nb_of_this_piece == wanted_pieces[name]:
			score += UNIQUE


	# For each valid connection, give points based on the connection value
	for cn in connection_list:
		score += is_in_connectdata(cn)
	
	# If a component owns three or more horizontal connexion, it blocks the whole system
	for piece_cn in groups:
		nb_xy_cn = 0
		nb_z_cn = 0
		for bloc in piece_cn:
			if bloc[2] == gen.XY_CONNECTION:
				nb_xy_cn += 1
			elif bloc[2] == gen.Z_CONNECTION:
				nb_z_cn += 1
		if nb_xy_cn <= 2:
			score += 1
		else: 
			score -= 100

	''' # EVALUATE THE CLOCK WHEN IT RUNS
	if (does_clock_run(connection_list)):
		initial_clock_runs(clock)
		# AWARD FOR RUNNING CLOCK
		score += 100.0
		# CHECK FOR EACH CONNECTION OF RUNNING CLOCK
		for cn in connection_list:
			print("Tick Tock Tick Tock Tick Tock")
			x = [cn[0].__class__.__name__,cn[1].__class__.__name__,cn[2]]
			if ((x[0]=="Hand") and (x[1]=="Gear") and (x[2]==XY_CONNECTION)):
				# IF 2 GEARS CONNECT HORIZONTALLY THEN THE OTHER GEAR WILL SPIN
				gears_XY_connection(cn[0], cn[1])
			if ((x[0]=="Hand") and (x[1]=="Gear") and (x[2]==Z_CONNECTION)) or ((x[1]=="Hand") and (x[0]=="Gear") and (x[2]==Z_CONNECTION)) or ((x[0]=="Gear") and (x[1]=="Gear") and (x[2]==Z_CONNECTION)):
				# IF A GEAR AND A HAND CONNECT VERTICALLY THAN THE HAND WILL SPIN
				objects_Z_connection(cn[0], cn[1])

			if (cn[1] == gen.Hand):
				hand = cn[1]
			if (cn[0] == gen.Hand):
				hand = cn[0]
			"""
			EVALUATE CLOCK
			"""
			if (hand.speed < 1./30) and (hand.speed > 1./90): 
				# IN THIS CASE THE HAND MAYBE THE SECOND HAND, A ROUND WILL TAKE BETWEEN 30s AND 90S
				SEC_SCORE = 1 - abs((abs(hand.speed) - VITESSE_SECONDHAND) / VITESSE_SECONDHAND)
				SCORE_HAND = SEC_SCORE
			elif (hand.speed < 1./1800) and (hand.speed > 1./5400):
				# IN THIS CASE THE HAND MAYBE THE MINUTE HAND, A ROUND WILL TAKE BETWEEN 1800s( 30 minutes) to 5400s (90 minutes).
				MIN_SCORE = 1 - abs((abs(hand.speed) - VITESSE_MINUTEHAND) / VITESSE_MINUTEHAND)
				SCORE_HAND = 60 * MIN_SCORE
			elif (hand.speed < 1./21600) and (hand.speed > 1./64800):
				# IN THIS CASE THE HAND MAYBE THE HOUR HAND, A ROUND WILL TAKE BETWEEN 21600S (12H) TO 64800(36H).
				HOU_SCORE = 1 - abs((abs(hand.speed) - VITESSE_HOURHAND) / VITESSE_HOURHAND)
				SCORE_HAND = 3600 * HOU_SCORE
			else : 
				SCORE_HAND = 0
			score += SCORE_HAND '''

	return score


"""
The hands are important, the more accurately a hand hand tells time, the better fitness score it gets
Hourhand > Minute Hand > Second Hand by priority ( we must know what hours, then what minute, then what second)
"""


def fitness_population(population):
	list_fitness = []
	for clock in population:
		list_fitness += [fitness(clock)]
	return list_fitness


def average_fitness(population):
	sum_fitness = 0
	for clock in population:
		sum_fitness += fitness(clock)
	return sum_fitness/len(population)


def evolve(population):

	for i in range(NUMBER_CROSSING):
		"""
		Randomly choose 3 clocks from the population
		Remove the one with the lowest fitness score
		Mate (evolve) the other two to create a new baby clock
		Add the new baby clock to the population
		"""

		# Chose 3 monsters
		obj1 = population.pop(random.randrange(len(population)))
		obj2 = population.pop(random.randrange(len(population)))
		obj3 = population.pop(random.randrange(len(population)))

		# Find the weakest, and remove it
		a = fitness(obj1)
		b = fitness(obj2)
		c = fitness(obj3)
		if a == min(a,b,c):
			destroyed_clock = obj1
			dad_clock = obj2
			mom_clock = obj3
		elif b == min(a,b,c):
			destroyed_clock = obj2
			dad_clock = obj1
			mom_clock = obj3
		else:
			destroyed_clock = obj3
			dad_clock = obj2
			mom_clock = obj1

		# Mate the 2 strongest and give the baby to the population
		baby_clock = gen.mate(dad_clock,mom_clock, random.randint(0, 100000))

		population.append(dad_clock)
		population.append(mom_clock)
		population.append(baby_clock)
		
def average_number_of_components(population):
	sum_components = 0
	for monster in population:
		sum_components += len(monster)-1
	sum_components /= len(population)
	return sum_components

def natural_selection(population):
	i=0
	while(i<NUMBER_GENERATIONS-1):
		i+=1
		print("Generation n°", i+1, ":", average_fitness(population), "Nbr pieces : ", average_number_of_components(population), " Best Fitness : ", fitness(best_clock(population)))
		evolve(population)


def best_clock(population):
	#RETURN THE BEST CLOCK
	best = population[0]
	for clock in population:
		if fitness(clock) > fitness(best) :
			best = clock
	return best

def display_clock(clock):
	connection_list = gen.list_connections(clock)
	for i in range(0,len(connection_list)):
		print (connection_list[i][0].__class__.__name__,connection_list[i][1].__class__.__name__,connection_list[i][2])

if __name__ == '__main__':
	"""
		Test
	"""
	print(" ------------------------------------------------------- ")
	input_database()
	population = gen.generate(100,3,100)
	natural_selection(population)

	best = best_clock(population)
	print("Best fitness : ", fitness(best))
	for piece in gen.classes :
		counter = 0
		for part in best[1:]:
			if isinstance(part, piece):
				counter+=1
		print("Number of ", piece, " : ", counter)
	print("------ connections ------")
	print(gen.list_connections(best))


	''' for i in range(len(valid_connections)) :
		print(i, " : ", valid_connections[i].name, " -> ", valid_connections[i].point)
	print( "   ",1 - abs((abs(1./60) - VITESSE_SECONDHAND) / VITESSE_SECONDHAND))
	print( "   ",1 - abs((abs(1/.60) - VITESSE_MINUTEHAND) / VITESSE_MINUTEHAND))
	print( "   ",1 - abs((abs(1./60) - VITESSE_HOURHAND) / VITESSE_HOURHAND))
	 '''

import lcm
class Fractions:
	"""
	All you need about Fractions in Maths
	"""
	def __init__(self):
		super().__init__()
	def how_to_write(self):
		return  "Type method is:\nStretch|Shrine\nExample:\n2|4\nIts look like:\n 2\n---\n 4\nWhole num is 1 in this Example:\n   2\n1 ---\n   4"
	def fraction_to_float(self, fraction:str, whole_num:int=0):
		"""
		This function converts a normal Fraction (1|2):
		
		Into a Float (Decimal):
		0.5

		First thing you must type the Fraction and Whole number (If is exist)
		"""
		# Normal Fractions Solving without algorithm
		# if fraction == '1|2'

		stretch = fraction.split('|')[0]
		shrine = fraction.split('|')[1]
		if not shrine == 10 or not shrine == 100 or not shrine == 1000:
			num = 1
			while True:
				new_shrine = int(shrine) * num
				new_stretch = int(stretch) * num
				if new_shrine == 10 or new_shrine == 100 or new_shrine == 1000:
					shrine = new_shrine
					stretch = new_stretch
					break
				else:
					num += 1
			return f"{whole_num}.{stretch}"
		else:
			return f"{whole_num}.{stretch}"
	def float_to_fraction(self, num:float):
		"""
		This function converts a float (Demical) Number into a Normal Fraction

		First you must type the float number only
		"""
		stretch = str(num).split('.')[0]
		shrine = str(num).split('.')[1]
		if len(shrine) == 1: return f"{shrine}|10\nAnd the whole number is {stretch}"
		elif len(shrine) == 2: return f"{shrine}|100\nAnd the whole number is {stretch}"
		elif len(shrine) == 3: return f"{shrine}|1000\nAnd the whole number is {stretch}"
	def abbreviation_fraction(self, fraction:str):
		"""
		This Function Abbreviation Fractions by divide num/shrine and num/stretch
		Example:

		2|4 = 1|2
		"""
		stretch = fraction.split('|')[0]
		shrine = fraction.split('|')[1]
		num = 2
		while True:
			if str(int(stretch)/num).split('.')[1] == '0' and str(int(shrine)/num).split('.')[1] == '0':
				new_stretch = int(int(stretch) / num)
				new_shrine = int(int(shrine) / num)
				return f"{new_stretch}|{new_shrine}"
			else:
				num += 1
	def multiple_fractions(self, fraction_1:str, fraction_2:str):
		"""
		Simple function to multiple two Fractions and Shortened if possible
		"""
		stretch_1 = fraction_1.split('|')[0]
		shrine_1 = fraction_1.split('|')[1]
		stretch_2 = fraction_2.split('|')[0]
		shrine_2 = fraction_2.split('|')[1]
		answer = f'{int(stretch_1)*int(stretch_2)}|{int(shrine_1)*int(shrine_2)}'
		try:
			return f"{answer} = {Fractions().abbreviation_fraction(answer)}"
		except:
			return answer
	def divide_fractions(self, fraction_1:str, fraction_2:str):
		"""
		A function to divide two Fractions and Shortened if possible
		"""
		stretch_1 = fraction_1.split('|')[0]
		shrine_1 = fraction_1.split('|')[1]
		stretch_2 = fraction_2.split('|')[0]
		shrine_2 = fraction_2.split('|')[1]
		answer = f"{int(stretch_1)*int(shrine_2)}|{int(shrine_1)*int(stretch_2)}"
		try:
			return f"{answer} = {Fractions().abbreviation_fraction(answer)}"
		except:
			return answer
	def fractional_number_to_normal_fraction(self, fraction:str, whole_number:int):
		"""
		This function helps you to convert a Fractional number (a normal Fraction with a whole_number) Into a Normal Fraction (without whole number)
		"""
		if whole_number == '0':
			return "The whole number must be at minimum 1 or more"
		else:
			stretch = fraction.split('|')[0]
			shrine = fraction.split('|')[1]
			return f"{int(whole_number)*int(shrine)+int(stretch)}|{shrine}"
	def addition_fractions(self, fraction_1:str, fraction_2:str):
		"""
		Function collect two fractions. Example:
		1|4 + 1|4 = 2|4
		"""
		stretch_1 = fraction_1.split('|')[0]
		shrine_1 = fraction_1.split('|')[1]
		stretch_2 = fraction_2.split('|')[0]
		shrine_2 = fraction_2.split('|')[1]
		new_shrine = lcm.lcm(int(shrine_1), int(shrine_2))
		new_stretch_1 = int(int(new_shrine / int(shrine_1)) * stretch_1)
		new_stretch_2 = int(int(new_shrine / int(shrine_2)) * stretch_2)
		try:
			e = self.abbreviation_fraction(f"{new_stretch_1 + new_stretch_2}|{new_shrine}")
			return f"{new_stretch_1 + new_stretch_2}|{new_shrine} = {e}"
		except:
			return f"{new_stretch_1 + new_stretch_2}|{new_shrine}"
	def subtract_fractions(self, fraction_1:str, fraction_2:str):
		"""
		Function Subtracts two fractions. Example:
		3|4 - 2|4 = 1|4
		"""
		stretch_1 = fraction_1.split('|')[0]
		shrine_1 = fraction_1.split('|')[1]
		stretch_2 = fraction_2.split('|')[0]
		shrine_2 = fraction_2.split('|')[1]
		new_shrine = lcm.lcm(int(shrine_1), int(shrine_2))
		new_stretch_1 = int(int(new_shrine / int(shrine_1)) * stretch_1)
		new_stretch_2 = int(int(new_shrine / int(shrine_2)) * stretch_2)
		try:
			e = self.abbreviation_fraction(f"{new_stretch_1 - new_stretch_2}|{new_shrine}")
			return f"{new_stretch_1 - new_stretch_2}|{new_shrine} = {e}"
		except:
			return f"{new_stretch_1 - new_stretch_2}|{new_shrine}"

class Maths:
	def __init__(self):
		super().__init__()
	def sqrt(self, number:int):
		"""
		Very simple algorithm to return the sqrt of the number
		Example:
		4 = 2 (2*2)
		25 = 5 (5*5)
		"""
		num = 1
		while True:
			if (num*num) == number: return num
			else: num += 1
			if num == 10000: return "The number is over 10000"
	def cube(self, number:int):
		"""
		Very simple algorithm to return the cube of the number
		Example:
		27 = 3 (3*3*3)
		"""
		num = 1
		while True:
			if (num*num*num) == number: return num
			else: num += 1
			if num == 10000: return "The number is over 10000"

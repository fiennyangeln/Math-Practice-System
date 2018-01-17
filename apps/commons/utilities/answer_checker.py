from . import answer_formatter, expression_checker
from . import trigonometry_prove_checker
#from . import plane_geometry_prove_checker
#from . import text_similarity_checker

#Check user answer
'''
Usage:
1. correct_answer
   - The answer defined in the database
   - Must be specified using dictionary (i.e. {"answer":"type_answer_here", "important_step":"type_important_step_here"}
   - Answer and important step must be specified using string, e.g. "\sin{a}"
   - Multiple answer should be separated using delimiter "|", e.g. "\sin{a}|\cos{b}"
   - The key "important_step" should only be specified if check_step==True
   - Does not support multiple important step, except for plane geometry proof
2. user_answer
   - The answer defined in the database
   - Must be specified using dictionary (i.e. {"answer":"type_answer_here"}
   - Answer and important step must be specified using string, e.g. "\sin{a}"
   - Multiple answer should be separated using delimiter "|", e.g. "\sin{a}|\cos{b}"
   - The key "important_step" should only be specified if check_step==True
   - Does not support multiple important step
3. topic
   - The topic of the answer
   - Optional variable, default="Unknown"
4. answer_type
   - The type of the answer
   - Possible values: "Numeric", "Expression", "Prove", "Sketch", "Text"
   - Optional variable, default="Expression"
5. switchable
   - Whether the answer can be written in any order
   - Optional variable, default=False
6. check_step
   - Whether the assessor need to perform additional step checking
   ---------------------------------------------------------------------------------
   *********************************** IMPORTANT ***********************************
   - If opted as True, it will check the steps specified by the user, and there must be only one correct answer
   - Otherwise, it will perform multiple answer check, i.e. the number of given correct answer must match the number of user answer
   ---------------------------------------------------------------------------------
   - If opted as True, "important_step" must be specified in the correct_answer as well as user_answer
   - Optional variable, default=False

Returns correctness of answer(True or False), and the number of wrong step (-1 if neither applicable nor not found)
'''


def check(correct_answer, user_answer, topic="Unknown", answer_type="Expression", switchable=True, check_step=False):
	#Numeric answer will be assessed in the same way as expression.
	#In this case, check_step is not applicable
	if answer_type == "Numeric":
		answer_type = "Expression"
		check_step = False
	important_step = None
	if check_step or answer_type == "Prove":
        #TODO : why does check_step is always false
		important_step = correct_answer['important_step']
	correct_answer = correct_answer['answer']
	correct_answer = answer_formatter.split_answer(correct_answer)
	user_answer = user_answer['answer']
	user_answer = answer_formatter.split_answer(user_answer)
	#Trigonometric identities proving
	if topic.lower() == "trigonometry" and answer_type == "Prove":
		if len(correct_answer) != 1:
			return False,-1
	if topic.lower() == "trigonometry" and answer_type == "Prove":
		if len(correct_answer) != 1:
			#Invalid input
			return False, -1
		else:
			correct_answer = correct_answer[0]
			result, step = trigonometry_prove_checker.check(correct_answer, user_answer, important_step)
			return result, step
	#Plane geometry proving
	elif topic.lower() == "plane geometry": # and answer_type == "Prove":
        #CHANGED : DEFAULT result = plane_geometry_prove_checker.check(correct_answer, user_answer)
		result = False
		return result, -1
	#Text similarity matching
	elif answer_type == "Text":
		# TODO: Code here
		#CHANGED : DEFAULT result = text_similarity_checker.check(correct_answer, user_answer)
		result = False
		return result, -1
	#Sketch
	elif answer_type == "Sketch":
		##TODO: Code here
		return False, -1
	else: #Default is expression matching
		if len(user_answer) < 2:
			#Cannot perform step checking
			check_step = False
		if check_step:
			#Check step by step
			#User answer should be the list of step
			#Number of correct answer given must equal to 1
			if len(correct_answer) != 1:
				#Error input, consider as false
				return False, -1
			correct_answer = correct_answer[0]
			#Check each step
			for i in range(len(user_answer)):
				result = expression_checker.check(correct_answer, user_answer[i])
				if result == False:
					return False, i
			#No error detected, then correct
			return True, -1
		else:
			#Check multiple answer
			#User answer is the list of answer from different part
			#Number of correct answer given must equal to the number of user answer
			if len(correct_answer) != len(user_answer):
				#Error input, consider as false
				return False, -1
			# Check each answer
			if not switchable:
				#Answer must be in the correct order
				for i in range(len(user_answer)):
					result = expression_checker.check(correct_answer[i], user_answer[i])
					if result == False:
						return False, i
				# No error detected, then correct
				return True, -1
			else:
				#Answer can be in any order
				#Duplicated answer should be removed
				correct_answer = list(set(correct_answer))
				user_answer = list(set(user_answer))
				counter = 0
				for x in correct_answer:
					for y in user_answer:
						result = expression_checker.check(x, y)
						if result == True:
							counter = counter + 1
				if len(correct_answer) == counter:
					return True, -1
				else:
					return False, -1

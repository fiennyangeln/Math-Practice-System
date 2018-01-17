from . import expression_checker
from . import answer_transformer
from . import answer_formatter

"""
Check the correctness of trigonometric proving correctness.
Approach:
1. Check the value of each step.
2. Perform additional checking (features need to be improved in order to improve accuracy).
"""


def check(correct_answer, user_answer, important_step=None):
    step = 1
    for step_answer in user_answer:
        correct = expression_checker.check(correct_answer, step_answer)
        if not correct:
            return False, step
        step += 1
    # Perform additional check
    succeed_additional_check = trigonometry_proving_additional_check(
        correct_answer, user_answer, important_step)
    if succeed_additional_check:
        return True, -1
    else:
        return False, -1


"""
Perform additional checking after value matching each step.
"""
def trigonometry_proving_additional_check(correct_answer, user_answer, important_step=None):

    # Check whether the last step equals to the RHS
    last_step = user_answer[len(user_answer) - 1]
    # Last step check if disabled due to inflexibility
    # if check_last_step(correct_answer, last_step) == False:
    #    return False  # Last step does not equal to RHS
    # Check whether the user specify the key step
    if check_important_step_existence(user_answer, important_step) == False:
        return False  # Important step not found
    #******************* ADD MORE ADDITIONAL CHECK HERE *******************

    # Lastly, no error found
    return True

"""
One of the additional checking.
Check the last step o
"""


def check_last_step(correct_answer, user_last_step):
    correct_answer_transformed = answer_transformer.transform_latex_to_sympy(
        correct_answer, mode="Mathquill only")
    user_last_step_transformed = answer_transformer.transform_latex_to_sympy(
        user_last_step, mode="Mathquill only")
    if correct_answer_transformed != user_last_step_transformed:
        return False
    else:
        return True

"""
One of the additional checking.
Check the existence of the important/core step.
Approach: Break each expression (step) into list of term. Then compare the value of every term.
"""


def check_important_step_existence(user_answer, important_step):
    if important_step == None:
        # Important step not specified, not a user fault. Consider as True.
        return True
    important_step = answer_transformer.transform_latex_to_sympy(
        important_step, mode="Mathquill only")
    important_step_split = answer_formatter.split_term(important_step)
    for answer in user_answer:
        answer = answer_transformer.transform_latex_to_sympy(
            answer, mode="Mathquill only")
        user_answer_split = answer_formatter.split_term(answer)
        if len(user_answer_split) != len(important_step_split):
            # This answer must not include the important step, since the number
            # of term is different
            continue
        else:
            # Remove duplicate
            user_answer_split = list(set(user_answer_split))
            important_step_split = list(set(important_step_split))
            counter = 0
            for x in important_step_split:
                for y in user_answer_split:
                    result = expression_checker.check(x, y)
                    if result == True:
                        counter = counter + 1
                        break
            if len(important_step_split) == counter:
                return True
    # Core step not found
    return False

from webmodels.models import *


def get_topics(request):
    """
    Return a list of topics based on current education level
    """
    t_topics = None
    try:
        if 'edu_id' in request.session:
            t_topics = Topic.objects.filter(
                education_level_id=(
                    request.session['edu_id'])).order_by('-order').reverse()
        else:
            t_topics = Topic.objects.all()
    except Exception as exp:
        print(exp)
    else:
        return t_topics

def retrieve_questions(concepts, difficulty_degree, num_questions):
    #  Convert all to floating value before filtering
    difficulty_degree = float(difficulty_degree)
    lower_bound = difficulty_degree - 1.0

    return Question.objects.filter(
        concept__in=concepts,
        float_difficulty_level__gt=lower_bound,
        float_difficulty_level__lt=difficulty_degree,
        question_type=1,
        checked=True,
        is_correct=True).order_by('?')[:num_questions]

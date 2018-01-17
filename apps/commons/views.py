from django.shortcuts import render
import re,json
from webmodels.models import *
from django.http import HttpResponse
from apps.commons.utilities import answer_checker
class ApiViews():
    def check_answer(request):
        result=dict()
        result['result']=False
        print("reach the api views")
        if request.method == 'POST':
            data = json.loads(request.body.decode("UTF-8"))
            if (data['type'] == 'q'):
                question_id = data['id']
                question = Question.objects.get(pk=question_id)
                # data that is needed
                model_answer_content = question.answer
                topic = question.concept.topic.name
                answer_type = question.respone_type

            else:
                answerpart_id = data['id']
                answer_part = AnswerPart.objects.get(pk=answerpart_id)
                subpart_no = data['subpart_no']
                # data that is needed
                topic = answer_part.question.concept.topic.name
                if subpart_no == 0 :
                    model_answer_content = answer_part.part_content
                    answer_type = asnwer_part.part_respone_type
                elif subpart_no == 1 :
                    model_answer_content = answer_part.subpart_name_1
                    answer_type = answer_part.respone_type_1
                elif subpart_no == 2 :
                    model_answer_content = answer_part.subpart_name_2
                    answer_type = answer_part.respone_type_2
                elif subpart_no == 3 :
                    model_answer_content = answer_part.subpart_name_3
                    answer_type = answer_part.respone_type_3
                else:
                    model_answer_content = answer_part.subpart_name_4
                    answer_type = answer_part.respone_type_4

            answer = data['answer']
            # name inconsistency
            if answer_type == "Numerical":
                answer_type = "Numerical"
            elif answer_type == "EXPRESSION":
                answer_type = "Expression"

            # answer initially also contain the question equation, so we need to separate it
            # example answer_content = '$\\frac{dy}{dx}$ = \"15x^4-6x^2+4\"'
            # after the process will return only the one after equal sign
            model_answer_list = extract_answers(model_answer_content)

            # for trigon proof there might be important_step
            if topic == "Trigonometry" and answer_type == "Prove":
                if len(model_answer_list) == 1:
                    correct_answer = {'answer': model_answer_list[0]}
                else:
                    correct_answer = {
                        'answer': model_answer_list[0],
                        'important_step': model_answer_list[1]}
            else:
                model_answer = "|".join(model_answer_list)
                correct_answer = {'answer': model_answer}
            user_answer = {'answer': answer}
            # TODO: Process wrong step
            answer_correctness, wrong_step = answer_checker.check(
                correct_answer, user_answer, topic=topic, answer_type=answer_type)
            if data['type'] == 'q':
                result['type'] = 'q'
                result['id'] = question_id
            else:
                result['type'] = 'a'
                result['id'] = answerpart_id
                result['subpart_no'] = subpart_no
            result['result'] = answer_correctness
        response = json.dumps(result)
        return HttpResponse(
            response,
            content_type='application/json')

def format_answer_box(question):
    if question.answer != " ":
        formatted_answer = substitute_answer_with_box(question.id, None, question.respone_type, question.answer, topic=question.concept.topic.name, has_subpart=False)
        setattr(question, "answer", formatted_answer)
    else:
        answer_parts = question.answerpart_set.all()
        for answer in answer_parts:
            answer.part_content = substitute_answer_with_box(answer.id, 0, answer.part_respone_type, answer.part_content, topic=question.concept.topic.name)
            if answer.subpart_name_1 == "i":
                answer.subpart_content_1 = substitute_answer_with_box(answer.id, 1, answer.respone_type_1, answer.subpart_content_1, topic=question.concept.topic.name)
            if answer.subpart_name_2 == "ii":
                answer.subpart_content_2 = substitute_answer_with_box(answer.id, 2, answer.respone_type_2, answer.subpart_content_2, topic=question.concept.topic.name)
            if answer.subpart_name_3 == "iii":
                answer.subpart_content_3 = substitute_answer_with_box(answer.id, 3, answer.respone_type_3, answer.subpart_content_3, topic=question.concept.topic.name)
            if answer.subpart_name_4 == "iv":
                answer.subpart_content_4 = substitute_answer_with_box(answer.id, 4, answer.respone_type_4, answer.subpart_content_4, topic=question.concept.topic.name)
        # Error: 'Question' object does not support item assignment
        # question['answer_parts'] = answer_parts
        setattr(question, "answer_parts", answer_parts)
        try:
            print(answer_parts[0].part_content)
        except IndexError:
            pass
    return question


def substitute_answer_with_box(answerpart_id, subpart_no, answer_type, original_answer, topic="Unknown", has_subpart=True):
    if not has_subpart:
        subpart_no = 'q'
    # Count the number of input in each part
    answer_count = len(re.findall(r'(["])(?:(?=(\\?))\2.)*?\1', original_answer))
    # Remove all answer
    content = re.sub(r'(["])(?:(?=(\\?))\2.)*?\1', '""', original_answer)
    if answer_type == "Prove" and topic == "Plane Geometry":
        output_HTML_tag = '<center><div id="answer_container-' + str(answerpart_id) + "-" + str(subpart_no) + '">'
        output_HTML_tag += "<span></span>"
        output_HTML_tag += '<span style="min-width:120px; min-height:25px;" id="answer-' + str(answerpart_id) + "-" + str(subpart_no) + \
                          "-" + str(0) + '"></span>'
        output_HTML_tag += '<input type="hidden" name="answer-' + str(answerpart_id) + "-" + \
                           str(subpart_no) + '"' + 'id="hidden_answer-' + str(answerpart_id) + "-" + \
                           str(subpart_no) + "-" + str(0) + '" >'
        output_HTML_tag += '</div>'
        output_HTML_tag += '<div id="answer_button_container-' + str(answerpart_id) + "-" + str(subpart_no) + '">'
        output_HTML_tag += '<div class="col-md-6">'
        output_HTML_tag += '<a style="float:right" href="#" class="btn btn-default" onclick="add_step(' + str(
            answerpart_id) + ','
        if subpart_no == 'q':
            output_HTML_tag += "'q'"
        else:
            output_HTML_tag += str(subpart_no)
        output_HTML_tag += ')" >Add Steps</a>'
        output_HTML_tag += '<div class="col-md-6">'
        output_HTML_tag += '<a style="float:left" href="#" class="btn btn-default" onclick="remove_step(' + str(answerpart_id) + ','
        if subpart_no == 'q':
            output_HTML_tag += "'q'"
        else:
            output_HTML_tag += str(subpart_no)
        output_HTML_tag += ')" >Remove Steps</a>'
        output_HTML_tag += '</div></div></center>'
        content = output_HTML_tag
    elif answer_type == "Prove" and topic == "Trigonometry":
        lhs_question = 'LHS' + '$ = $'
        output_HTML_tag = '<div class="row"><div id="col-md-6">'
        output_HTML_tag += lhs_question
        output_HTML_tag += '</div><div id="col-md-6"><div id="answer_container-' + str(answerpart_id) + "-" + str(subpart_no) + '">'
        output_HTML_tag += "<span>= </span>"
        output_HTML_tag += '<span style="min-width:120px; min-height:25px;" id="answer-' + str(answerpart_id) + "-" + str(subpart_no) + \
                          "-" + str(0) + '"></span>'
        output_HTML_tag += '<input type="hidden" name="answer-' + str(answerpart_id) + "-" + \
                           str(subpart_no) + '"' + 'id="hidden_answer-' + str(answerpart_id) + "-" + \
                           str(subpart_no) + "-" + str(0) + '" >'
        output_HTML_tag += '</div>'
        output_HTML_tag += '<div id="answer_button_container-' + str(answerpart_id) + "-" + str(subpart_no) + '">'
        output_HTML_tag += '<div class="col-md-6">'
        output_HTML_tag += '<a style="float:right" href="#" class="btn btn-default" onclick="add_step(' + str(answerpart_id) + ','
        if subpart_no == 'q':
            output_HTML_tag += "'q'"
        else:
            output_HTML_tag += str(subpart_no)
        output_HTML_tag += ')" >Add Steps</a>'
        output_HTML_tag += '</div><div class="col-md-6">'
        output_HTML_tag += '<a style="float:left" href="#" class="btn btn-default" onclick="remove_step(' + str(answerpart_id) + ','
        if subpart_no == 'q':
            output_HTML_tag += "'q'"
        else:
            output_HTML_tag += str(subpart_no)
        output_HTML_tag += ')" >Remove Steps</a>'
        output_HTML_tag += '</div></div></div></div>'
        content = output_HTML_tag
    elif answer_type == "Numberic" or answer_type == "EXPRESSION" or answer_type == "Text" or answer_type == "Numerical" or answer_type == "Expression":
        for i in range(answer_count):
            # Construct HTML tag
            if answer_type == "Numberic" or answer_type == "EXPRESSION" or answer_type == "Expression" or answer_type == "Numerical":
                output_HTML_tag = '<span id="answer-' + str(answerpart_id)   + "-" + str(subpart_no) + \
                    "-" + str(i) + '"></span>'
                output_HTML_tag += '<input type="hidden" name="answer-' + str(answerpart_id) + "-" + \
                    str(subpart_no) + '"' + 'id="hidden_answer-' + str(answerpart_id) + "-" + \
                    str(subpart_no) + "-" + str(i) + '" >'
                # Substitute the answer with HTML tag (process each sub_part one by one)
                content = re.sub(r'""', output_HTML_tag, content, 1)
            elif answer_type == "Text":
                output_HTML_tag = '<input type="text" name="answer-' + str(answerpart_id) + "-" + \
                    str(subpart_no) + '"' + 'id="hidden_answer-' + str(answerpart_id) + "-" + str(subpart_no) + "-" + \
                    str(i) + '" >'
                # Substitute the answer with HTML tag (process each sub_part one by one)
                content = re.sub(r'""', output_HTML_tag, content, 1)
    else:

        output_HTML_tag = "Unknown error" + answer_type
        # Substitute the answer with HTML tag (process each sub_part one by one)
        content = output_HTML_tag
    return content

def extract_answers(content):
    """Extract answer fields in a string and return a list"""
    fields = re.findall(r'"(.*?)"', content)
    return fields

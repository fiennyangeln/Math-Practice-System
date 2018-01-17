from django.shortcuts import render
import re,json
from django.http import HttpResponse
class ApiViews():
    def check_answer(request):
        result=dict()
        result['result']=True
        response = json.dumps(result)
        return HttpResponse(response,content_type='application/json')

# Create your views here.
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

function check_answer(id, subpart_no, has_part)
{
  var answer = {};
  if (has_part === false) {
        var answer_component_list = document.getElementsByName("answer-" + id + "-" + "q");
        var answer_list = [];

        for (var i = 0; i < answer_component_list.length; i++) {
            answer_list.push(answer_component_list[i].value);
        }
        answer_list = answer_list.join("|");
        answer['type'] = 'q';
        answer['id'] = id;
        answer['answer'] = answer_list;
  } else {
        var answer_component_list = document.getElementsByName("answer-" + id + "-" + subpart_no);
        var answer_list = [];

        for (var i = 0; i < answer_component_list.length; i++) {
            answer_list.push(answer_component_list[i].value);
        }
        answer_list = answer_list.join("|");
        answer['type'] = 'a';
        answer['id'] = id;
        answer['subpart_no'] = subpart_no;
        answer['answer'] = answer_list;
  }

  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
    });

$.ajax('/api/check_answer/', {
      type : 'POST',
      contentType : 'application/json',
      data : JSON.stringify(answer),
      success: function(data) {
        var JSONresult = JSON.parse(JSON.stringify(data));
        var type = JSONresult['type'];
        var id = JSONresult['id'];
                var subpart_no = JSONresult['subpart_no'];
        var result = JSONresult['result'];
        if (type === 'q') {
          display_answer_result(id, subpart_no, result, false);
                } else {
          display_answer_result(id, subpart_no, result);
                }

      },
      error: function(data, status, error) {
      }
  });
};
function clear_answer()
{
  console.log("clearing");
  $('#hidden-1').val('');
  $('#hidden-2').val('');
};
function display_answer_result(id, subpart_no, result, has_part) {
    reset_answer_result(id, subpart_no, has_part);
    if (has_part === false) {
        var answer_result_component = document.getElementById("answer_result-q-" + id);
    } else {
        var answer_result_component = document.getElementById("answer_result-" + id + "-" + subpart_no);
    }
    if (result) {
        answer_result_component.innerHTML = "Right";
    } else {
        answer_result_component.innerHTML = "Wrong";
    }
};


function display_error(error){
  console.log(error);
};

function reset_answer_result(id, subpart_no, has_part) {
    if (has_part === false) {
        var answer_result_component = document.getElementById("answer_result-q-" + id);
        answer_result_component.innerHTML = "";
    } else {
        var answer_result_component = document.getElementById("answer_result-" + id + "-" + subpart_no);
        answer_result_component.innerHTML = "";
    }

 };

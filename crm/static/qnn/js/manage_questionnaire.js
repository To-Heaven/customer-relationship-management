var index = 1;

// 事件委派，用于添加问题
$("#add_question").click(function () {
    var question_str = `<li >
                    <div class="per_question" question_id="">
                            <span class="glyphicon glyphicon-remove pull-right delete_choice" aria-hidden="true"></span>
                        <div class="col-md-12">
                            <div class="col-md-1">
                                问题内容:&nbsp;
                            </div>
                            <div class="col-md-10">
                                <input type="text" name="content" value="" class="form-control content" maxlength="256" required="" id="">
                            </div>
                        </div>

                        <div class="col-md-12">
                            <div class="col-md-1">
                                问题类型:&nbsp;
                            </div>
                            <div class="col-md-3">
                               <select name="question_type" class="form-control question_type" required="" id="">
                                  <option value="">---------</option>
                                  <option value="1">单选</option>
                                  <option value="2">多选</option>                 
                                  <option value="3">打分</option> 
                                  <option value="4">建议</option>
                                </select>
                            </div>
                            <div class="col-md-1 hide">
                                <button class="btn  btn-default add_option">+添加选项</button>
                            </div>
                            <ul class="choice_list list-unstyled">
                            </ul>
                     </div>
                     </div>
</li>`;
    $(".question_area ol").append(question_str);
});

$("#submit_question").click(function () {
    var data = [];

    $.each($(".question_area .per_question"), function () {
        var per_question_data = {
            id: $(this).attr('question_id'),
            content: $(this).find('.content').val(),
            question_type: $(this).find('.question_type').val()
        };

        if (per_question_data['question_type'] == 1 || per_question_data['question_type'] == 2){
            per_question_data["choices"] = [];
            $.each($(this).find('.per_choice'), function () {
                var per_choice = {
                    id: $(this).attr('choice_id')
                };
                var input_list = $(this).find('input');
                per_choice['title'] = $(input_list[0]).val();
                per_choice['score'] = $(input_list[1]).val();

                per_question_data["choices"].push(per_choice);
            });
        }
        data.push(per_question_data)
    });
    console.log(data);

    $.ajax({
        url: $(':hidden').val(),
        type: 'post',
        headers: {
            'X-CSRFToken': $("[name='csrfmiddlewaretoken']").val()
        },
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function (data) {
            data = JSON.parse(data);
            console.log(data)
            // if (data['success']) {
            //     window.location.href = data['location_href'];
            // }
        }
    })
});


// 事件委派，用于添加选项
$(".question_area").on('click', ".add_option", function () {
    var option_str = `<li>
                        <div choice_id="" class="per_choice">
                            <div class="col-md-12">
                                <div class="col-md-4">
                                    <div class="col-md-3">
                                        选项:
                                    </div>
                                     <div class="col-md-8">
                                         <input type="text" name="title" value="" class="form-control" maxlength="32" required="" id="">
                                     </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="col-md-3">
                                         分值:
                                    </div>
                                     <div class="col-md-8">
                                         <input type="text" name="score" value="" class="form-control" required="" id="">
                                     </div>
                                </div>
                                <div class="col-md-2 text-center">
                                       <span class="glyphicon glyphicon-remove delete_choice" aria-hidden="true"></span>
                                 </div>
                            </div>
                        </div>
                    </li>`;
    $(this).parent().next().append(option_str)
});


// 事件委派，用于隐藏和显示选项添加按钮
$(".question_area").on('change', '.question_type', function () {
    if ($(this).val() == '1' || $(this).val() == '2') {
        $(this).parent().next().removeClass('hide')
    } else {
        $(this).parent().next().addClass('hide');
        $(this).parent().next().next().empty();
    }
});

// 事件委派，用于删除单选/多选的选项
$(".question_area").on('click', ".delete_choice", function () {
    $(this).parent().parent().remove();
});


// 事件委派，删除问题以及保证每一个问题的标题按顺序排列
$(".question_area").on('click', ".delete_question", function () {
    $(this).parent().parent().remove();
});


// Ajax提交问卷数据

/*
{
    1: {
            question_content: "xxx";    // 内容
            question_type: "1"      // id
            option: {
                choice: score;
                choice: score;
                choice: score;
            }
        }
    2: {
        .....
    }
}
*/



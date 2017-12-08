$("#add_questionnaire").click(function () {
    $(".form-group span").text('');
    $(".form-group span").parent().removeClass('has-error');

    var formData = new FormData();

    formData.append('title', $("#id_title").val());
    formData.append('description', $("#id_description").val());
    formData.append('department', $("#id_department").val());
    formData.append('csrfmiddlewaretoken', $("[name='csrfmiddlewaretoken']").val());
    $.ajax({
        url: '/add_questionnaire/',
        type: 'post',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            data = JSON.parse(data);
            if (data.success) {
                window.location.href = data.location_href;
            } else {
                for (var key in data.error_msg) {
                    $("#" + key).text(data.error_msg[key][0]);
                    $("#" + key).parent().addClass('has-error');
                }
            }
        }
    });
});
from django.shortcuts import render, HttpResponse
from django.forms import fields, widgets
from django.core.exceptions import ValidationError

from json import dumps, loads

from questionnaire_app.forms import LoginForm, QuestionnaireForm, QuestionModelForm, ChoiceModelForm, Form
from questionnaire_app import models


def login(request):
    if request.method == 'GET':
        form = LoginForm(request=request)
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':  # 登陆验证开始
        form = LoginForm(request=request, data=request.POST)
        if not form.is_valid():  # 验证信息格式错误
            data = {'form_errors': form.errors}
            return HttpResponse(dumps(data))

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        employee_queryset = models.Employee.objects.filter(username=username, password=password)
        admin_queryset = models.Admin.objects.filter(username=username, password=password)
        if employee_queryset:
            request.session["user_id"] = employee_queryset[0].id
            request.session["username"] = employee_queryset[0].username
            request.session["role"] = 'employee'
            data = {'success': True, "location_href": '/questionnaire/list_questionnaire/'}
        elif admin_queryset:
            request.session["role"] = 'admin'
            request.session["user_id"] = admin_queryset[0].id
            data = {'success': True, "location_href": '/questionnaire/list_questionnaire/'}
        else:
            form.add_error(field='password', error="用户名或密码错误")
            data = {'success': False}
        return HttpResponse(dumps(data))


def list_questionnaire(request):
    questionnaires = models.Questionnaire.objects.all()
    return render(request, 'list_questionnaire.html', {"questionnaires": questionnaires})


def add_questionnaire(request):
    if request.method == 'GET':  # <QueryDict: {'title': ['a'], 'description': ['a'], 'department': ['1,2,3'], 'csrfmiddlewaretoken': ['i8zX0WNbHd2hXEhODp695S4HtaknnBZXhxzSJAeA8sYDLEBaQAVOJIEeiE6tFnxd']}>
        form = QuestionnaireForm()
        departments = models.Department.objects.all()
        return render(request, 'add_questionnaire.html', {"form": form, "departments": departments})
    elif request.method == 'POST':
        form = QuestionnaireForm(data=request.POST)
        if form.is_valid():
            department_ids = [int(i) for i in request.POST.getlist('department')[0].split(',')]  # ['1,2,3']
            if department_ids:
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                user_id = request.session.get('user_id')
                questionnaire_list = [
                    models.Questionnaire(title=title, description=description, admin_id=user_id,
                                         department_id=department_id)
                    for department_id in department_ids
                ]
                models.Questionnaire.objects.bulk_create(questionnaire_list)
                data = {"success": True, 'location_href': '/list_questionnaire/'}
                return HttpResponse(dumps(data))
            else:
                form.add_error(field='department', error='至少选择一个部门')
                data = {'success': False, "error_msg": form.errors}
                return HttpResponse(dumps(data))
        else:
            data = {'success': False, "error_msg": form.errors}
            return HttpResponse(dumps(data))


def manage_questionnaire(request, questionnaire_id=None):
    """ 处理管理员编辑问卷的请求并生成响应
    Args:
        request: 当前请求对象
        questionnaire_id: 要编辑的问卷的id
    Return:
        response响应
    """

    if request.method == 'GET':
        questions = models.Question.objects.filter(questionnaire_id=questionnaire_id)
        print(questions)
        if not questions:
            form = QuestionModelForm()
            return render(request, 'manage_questionnaire.html',
                          {"question_list": {"form": form, "question": None},
                           "questionnaire_id": questionnaire_id})
        else:
            def generator_question_model_form(args):
                question_list = []
                for question in questions:
                    if question.question_type in (1, 2):
                        def generator_option_model_form(question):
                            choices = models.Choice.objects.filter(question=question)
                            yield from [{"form": ChoiceModelForm(instance=choice), "choice": choice} for choice in
                                        choices]

                        question_list.append({"form": QuestionModelForm(instance=question),
                                              "question": question, "option_class": "",
                                              "options": generator_option_model_form(question)})
                    else:
                        question_list.append({"form": QuestionModelForm(instance=question),
                                              "question": question, "option_class": "hide", "options": None})
                yield from question_list

            return render(request, 'manage_questionnaire.html',
                          {"question_list": generator_question_model_form(questions),
                           "questionnaire_id": questionnaire_id})
    else:
        data = loads(request.body.decode('utf-8'))
        for question in data:
            question_id = question.get('id')
            content = question.get('content').strip()
            question_type = question.get('question_type').strip()
            if content and question_type:  # 如果内容和问题类型不为空
                if question_id:  # 问题已存在
                    models.Question.objects.filter(questionnaire_id=questionnaire_id).update(content=content,
                                                                                             question_type=question_type)
                    question_obj = models.Question.objects.filter(questionnaire_id=questionnaire_id).first()
                else:  # 问题为新建问题
                    question_obj = models.Question.objects.create(questionnaire_id=questionnaire_id,
                                                                  content=content, question_type=question_type)
                if question_type in ('1', '2'):
                    choices = question.get('choices')
                    if choices:  # 如果设置了选项
                        for choice in choices:
                            choice_id = choice.get('id')
                            title = choice.get('title')
                            score = choice.get('score')
                            if title and score:  # 如果选项和分值不为空
                                if choice_id:  # 修改choice
                                    print('in ')
                                    models.Choice.objects.filter(question=question_obj).update(title=title, score=score)
                                else:  # 新建的choice
                                    print('in else')
                                    models.Choice.objects.create(title=title, score=score, question=question_obj)
                            else:  # 如果选项和分值为空
                                return HttpResponse(dumps({"success": False, "error": '选项和分值不能为空'}))

                    else:  # 如果没有设置选项
                        return HttpResponse(dumps({"success": False, "error": '你没有设置选项'}))
            else:  # 如果内容和问题类型为空
                return HttpResponse(dumps({"success": False, "error": '内容和问题类型不能为空'}))
        else:
            return HttpResponse(dumps({"success": True, "location_href": '/list_questionnaire/'}))


'''
[
    {
        'id': '1',
        'content': 'aaaa',
        'question_type': '1',
        'choices': [
            {
                'id': '1',
                'title': 'a',
                'score': '1'
            },
            {
                'id': '2',
                'title': 'b',
                'score': '2'
            }
        ]
    },
    {
        'id': '2',
        'content': 'ssss',
        'question_type': '2',
        'choices': [
            {
                'id': '3',
                'title': 'a',
                'score': '1'
            },
            {
                'id': '4',
                'title': 'v',
                'score': '2'
            }
        ]
    },
    {
        'id': '3',
        'content': 'aaasssss',
        'question_type': '3'
    }
]
'''


def show_score(request, department_id=None, quesionnaire_id=None):
    pass


def get_questionnaire_page(request, department_id, questionnaire_id):
    employee_id = request.session.get('user_id')
    print(employee_id)
    employee = models.Employee.objects.filter(department_id=department_id, id=employee_id)

    if not employee:
        return HttpResponse('不是本部门员工不能参与问卷')

    answer = models.Answer.objects.filter(employee_id=employee_id, question__questionnaire_id=questionnaire_id)
    if answer:
        return HttpResponse('你已经参与过问卷啦')

    def my_validator(value):
        if len(value) < 15:
            raise ValidationError('建议不能低于15字哦')

    questions = models.Question.objects.filter(questionnaire_id=questionnaire_id)
    field_dict = {}
    for question in questions:
        if question.question_type == 1:
            field_dict[f'choice_id_{question.id}'] = fields.ChoiceField(
                label=question.content,
                widget=widgets.RadioSelect(attrs={"class": 'list-unstyled'}),
                choices=models.Choice.objects.filter(question_id=question.id).values_list('id', 'title')
            )
        elif question.question_type == 2:
            field_dict[f'choice_id_{question.id}'] = fields.ChoiceField(
                label=question.content,
                widget=widgets.RadioSelect(attrs={"class": 'list-unstyled'}),
                choices=models.Choice.objects.filter(question_id=question.id).values_list('id', 'title')
            )
        elif question.question_type == 3:
            field_dict[f'val_{question.id}'] = fields.ChoiceField(
                label=question.content,
                error_messages={'required': '必填内容'},
                widget=widgets.RadioSelect(attrs={'class': 'list-unstyled'}),
                choices=[(i, i) for i in range(1, 11)]
            )
        else:
            field_dict[f'content_{question.id}'] = fields.CharField(
                label=question.content,
                error_messages={"required": '不能为空'},
                widget=widgets.Textarea(attrs={"class": 'form-control'}),
                validators=[my_validator, ]
            )
    QuestionForm = type('QuestionForm', (Form, ), field_dict)

    if request.method == 'GET':
        form = QuestionForm()
        return render(request, 'questionnaire.html', {"questions": questions, "form": form})
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            answer_objs = []
            for field, value in form.cleaned_data.items():
                key, question_id = field.rsplit('_', 1)
                answer_dict = {'employee_id': employee_id, 'question_id': question_id, key: value}
                answer_objs.append(models.Answer(**answer_dict))
            models.Answer.objects.bulk_create(answer_objs)
            return HttpResponse("谢谢参与")
        else:
            render(request, 'questionnaire.html', {"form": form})


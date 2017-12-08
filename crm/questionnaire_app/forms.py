from django.forms import Form, ModelForm
from django.forms import fields
from django.forms import widgets

from questionnaire_app import models


class BaseInfoForm(Form):
    """ 基本用户信息form组件类

    """
    username = fields.CharField(required=True,
                                error_messages={'required': '用户名不能为空'},
                                widget=widgets.TextInput(attrs={'placeholder': '用户名',
                                                                'class': 'form-control',
                                                                'aria-describedby': "username"}))

    password = fields.CharField(required=True,
                                error_messages={'required': '密码不能为空'},
                                widget=widgets.PasswordInput(attrs={'placeholder': '密码',
                                                                    'class': 'form-control',
                                                                    'aria-describedby': "password"}))


class LoginForm(BaseInfoForm):
    """
        用于用户登陆的form组件类
    """
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


class QuestionnaireForm(Form):
    title = fields.CharField(max_length=32, required=True,
                             error_messages={'required': '标题不能为空'},
                             widget=widgets.TextInput(attrs={'class': 'form-control',
                                                             'aria-describedby': 'title'}))

    description = fields.CharField(max_length=512, required=True,
                                   error_messages={'required': '问卷描述不能为空'},
                                   widget=widgets.Textarea(attrs={'class': 'form-control',
                                                                  'cols': 50, 'rows': 5,
                                                                  'aria-describedby': 'description'}))

class QuestionModelForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ['content', 'question_type']
        widgets = {
            'content': widgets.TextInput(attrs={'class': 'form-control content'}),
            'question_type': widgets.Select(attrs={'class': 'form-control question_type'})
        }

class ChoiceModelForm(ModelForm):
    class Meta:
        model = models.Choice
        fields = ['title', 'score']
        widgets = {
            'title': widgets.TextInput(attrs={'class': 'form-control'}),
            'score': widgets.TextInput(attrs={'class': 'form-control'})
        }
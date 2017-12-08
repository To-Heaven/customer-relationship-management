# 投票系统模型


## 设计表
- 本应用是一个CRM项目中的投票应用，主要是用来实现公司内部的问卷调查。因此表面性的逻辑设计也是基于这个实际情况，整个models.py中总共设计了7张表，分别如下
	- Department部门表
	- Employee员工表
	- Admin管理员表
	- Questionnaire问卷表
	- Question问题表
	- Choice选项表
	- Answer答案表

- 下面对每张表结构简单介绍


#### 问卷表
- 问卷表与管理员表、问卷表与部门表均设置了多对一的关联关系，因为一个管理员用户可以创建多个调查问卷，一个部分可以接受多个调查问卷

#### 问题表
- 每一个问卷中都设置了多个问题，因此将问题表与问卷表多对一关联。问卷调查中常见的问题有四种分类，即单选题、多选题、评分题以及建议。并且考虑到这四种类型基本上是固定的，所以在创建模型类的时候，使用了`choices`来代替一张表，这样可以加快查询速度。
- 在问题表中，除了上述字段之外，还设置了问题内容字段，用来存放问题题干。

#### 选项表
- 对于选择题（包括单选题和多选题）来说，每一个question都对应了若干个选项，因此将选项表与问题表进行多对一关联，每一个选项都有对应的分值，比如"满意"对应"10"，"一般"对应"6"等等，因此在选项表中除了上述字段之外还应包括每一个选项的标题和对应的分值


#### 答案表
- 答案表中存放了员工调查问卷的结果，每一个答案都与一个问题对应，一个员工对一个问卷可以有多个答案(因为问卷中有多个题目)，并且还要保证每一个用户对同一个问题只能回答一次，因此将员工与每一个问题进行联合唯一。


#### Admin管理员表
- 管理员可以用来创建问卷，除了用户名以及登录密码之外，在管理员表中没有设置其他字段，管理员登录之后创建的问卷会与其关联

#### Employee
- 员工表与部门表多对一关联，这里没有考虑一人身兼数职的情况。

#### Department部门表
- 部门表内只有一个字段，部门名称


#### 流程分析
- 下面对一个完整的问卷流程进行分析，确保模型设计能够满足调查问卷中的功能
	1. admin登陆账户，进入主页面，点击添加问卷按钮，进入增加问卷页面
	2. 问卷页面中填好问卷的标题、描述以及调查对象之后，传递给后端，后端将这一条记录存放在问卷表中。页面跳转到所有问卷的一个表格排列页面
	3. 接着用户点击编辑按钮，进入指定问卷的编辑页面，在该页面中添加问题，并选择问题类型，如果是选择题就需要添加选项和设置对应的分值，创建完毕之后整个页面上的数据会发送给服务端，服务端根据问题的类型、问题的内容以及被编辑的问卷创建一条记录保存至问题表，如果该问题是一个选择题会通过该选择题的选项、对应的分值以及刚创建的问题对象生成一条选项记录至选项表。
	4.  
	5. 员工登陆账号，进入问卷调查填写页面之后，填写对应的题目，提交后会根据员工对象、问题对象以及答案的内容创建一个答案对象保存至答案表中，每一个答案都对应着一个问题，而每一个问题有对应着一个问卷对象，因此可以实现将员工提交的答案与对应的问卷间接的关联

## 代码

```python
from django.db import models


class Department(models.Model):
    """ 部门表
    普通字段:
        id, dep_name
    """

    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=16, blank=True, verbose_name='部门名称')

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name_plural = '部门表'


class Employee(models.Model):
    """ 用户信息表
    普通字段:
        id, username, password
    关联字段:
        department(多对一, to=Department.id)
    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')

    department = models.ForeignKey(to='Department', to_field='id', verbose_name='部门')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户表'


class Admin(models.Model):
    """ 管理员表
    普通字段:
        username, password
    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=32, verbose_name='密码')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '管理员表'


class Questionnaire(models.Model):
    """ 问卷表
    普通字段:
        id, title, description
    关联字段:
        department(一对一, to=BanJi.id)
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='问卷标题')
    description = models.CharField(max_length=512, verbose_name='问卷描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    admin = models.ForeignKey(to='Admin', to_field='id', verbose_name='创建人')
    department = models.ForeignKey(to='Department', to_field='id', verbose_name='接受调查的部门')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '问卷表'


class Question(models.Model):
    """ 问题表
    普通字段:
        id, question_type, content
    关联字段:
        questionnaire(多对一, to=Questionnaire.id)
    """

    id = models.AutoField(primary_key=True)
    question_type_choices = [
        (1, "单选"),
        (2, "多选"),
        (3, "打分"),
        (4, "建议"),
    ]
    question_type = models.IntegerField(choices=question_type_choices, verbose_name='问题类型')
    content = models.CharField(max_length=256, verbose_name='问题内容')

    questionnaire = models.ForeignKey(to='Questionnaire', to_field='id', verbose_name='所属问卷')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '问题表'


class Choice(models.Model):
    """ 问题选项表
    普通字段:
        id, 标题, 选项值
    关联字段:
        question(多对一， to=Question.id)
    """

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='选项标题')
    score = models.IntegerField(verbose_name='选项分数')
    # choice_value = models.CharField(max_length=128, verbose_name='选项值')  # 存放json字符串

    question = models.ForeignKey(to='Question', to_field='id', verbose_name='所属问题')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '问题选项表'


class Answer(models.Model):
    """ 答案表
    普通字段:
        id, content(json)
    关联字段:
        employee(多对一, to=User.id)
        question(多对一, to=Question.id)
    """

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=512, verbose_name='答案内容')
    answer_time = models.DateTimeField(auto_now_add=True, verbose_name='回答时间')

    val = models.IntegerField(verbose_name='分数')
    employee = models.ForeignKey(to='Employee', to_field='id', verbose_name='回答员工')
    question = models.ForeignKey(to='Question', to_field='id', verbose_name='对应问题')

    def __str__(self):
        return self.content

    class Meta:
        unique_together = (('employee', 'question'),)
        verbose_name_plural = '答案表'
```
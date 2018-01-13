from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Question(models.Model):
    content = RichTextField()
    solution = RichTextField()
    answer = RichTextField(default="Test")
    def __str__(self):
        return u'%s. %s' %(self.id,self.content)

class EducationLevel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Topic(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1000)
    order = models.PositiveIntegerField(null=True, blank=True)

    education_level = models.ForeignKey(
        EducationLevel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Concept(models.Model):
    """
    List of concepts in each topic. Examples:
        Quadratic Equations & inequalities has:
            Symmetric properties of the roots of a quadratic equation
        ...
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    description = RichTextUploadingField()
    order = models.PositiveIntegerField(null=True, blank=True, default=1)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Paper(models.Model):
    """
    List of paper
    """

    def __str__(self):
        return str(self.country) + " - " + str(self.title) + " - " +\
            str(self.year) + " | " + str(self.paper_number)

    country = models.CharField(max_length=100, default="Singapore")
    title = models.CharField(max_length=500, default="")
    year = models.IntegerField(default=2000)
    paper_number = models.IntegerField(default=1)

    education_level = models.ForeignKey(
        EducationLevel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class KeyPoint(models.Model):
    """
    List of key points associate with specific concept
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    content = RichTextUploadingField()

    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    """
    List of Tag
    """
    name = models.CharField(max_length=255)

    description = models.TextField(default="")
    new_description = RichTextUploadingField(default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    """
    List of questions
    """

    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default="EX")
    used_for = models.CharField(
        max_length=2,
        choices=USED_FOR,
        default="ON")
    mark = models.IntegerField(default=0)
    difficulty_level = models.CharField(
        max_length=1,
        choices=DIFFICULTIES,
        default="1")
    float_difficulty_level = models.FloatField(default=0.5)
    respone_type = models.CharField(
        max_length=10,
        choices=RESPONSE_TYPES,
        default="4")
    content = RichTextUploadingField()
    textual_content = RichTextUploadingField(default="")
    description = RichTextUploadingField(default="")
    solution = RichTextUploadingField()

    answer = RichTextField(default="Test")
    number_views = models.PositiveIntegerField(default=0)
    checked = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='uploads/',
                               default='static/img/no_image.png')

    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    keypoint = models.ForeignKey(KeyPoint, on_delete=models.CASCADE,
                                 null=True, blank=True)
    paper = models.ForeignKey(
        Paper, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    lastCheckedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_answers(self):
        return AnswerQuestion.objects.filter(question=self)

    class AnswerPart(models.Model):
        """
        List of AnswerPart
        """
        part_name = models.CharField(max_length=1, choices=PARTS)
        part_content = RichTextField()
        part_respone_type = models.CharField(
            max_length=10,
            choices=RESPONSE_TYPES,
            default="4")
        subpart_name_1 = models.CharField(max_length=10, null=True, blank=True)
        subpart_content_1 = RichTextField(null=True, blank=True)
        respone_type_1 = models.CharField(
            max_length=10,
            choices=RESPONSE_TYPES,
            default="4", null=True, blank=True)
        subpart_name_2 = models.CharField(max_length=10, null=True, blank=True)
        subpart_content_2 = RichTextField(null=True, blank=True)
        respone_type_2 = models.CharField(
            max_length=10,
            choices=RESPONSE_TYPES,
            default="4", null=True, blank=True)
        subpart_name_3 = models.CharField(max_length=10, null=True, blank=True)
        subpart_content_3 = RichTextField(null=True, blank=True)
        respone_type_3 = models.CharField(
            max_length=10,
            choices=RESPONSE_TYPES,
            default="4", null=True, blank=True)
        subpart_name_4 = models.CharField(max_length=10, null=True, blank=True)
        subpart_content_4 = RichTextField(null=True, blank=True)
        respone_type_4 = models.CharField(
            max_length=10,
            choices=RESPONSE_TYPES,
            default="4", null=True, blank=True)

        question = models.ForeignKey(Question, on_delete=models.CASCADE)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    class AnswerQuestion(models.Model):
        """
        List of answers of question by user
        """
        content = RichTextUploadingField()

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        question = models.ForeignKey(Question, on_delete=models.CASCADE)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    class Formula(models.Model):
        """
        List of formula
        """

        def __str__(self):
            return self.name

        name = models.CharField(max_length=200, default="")
        content = models.TextField()
        status = models.BooleanField(default=False)
        inorder_term = models.TextField(max_length=1024, null=True, blank=True)
        sorted_term = models.TextField(max_length=1024, null=True, blank=True)
        structure_term = models.TextField(max_length=1024, null=True, blank=True)
        constant_term = models.TextField(max_length=1024, null=True, blank=True)
        variable_term = models.TextField(max_length=1024, null=True, blank=True)
        is_used = models.BooleanField(default=True)

        question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class FormulaIndex(models.Model):
        """
        List of Formula Indices
        """
        indexkey = models.CharField(primary_key=True, max_length=255)
        formulas = models.ManyToManyField(Formula)
        df = models.PositiveIntegerField('frequency', default=1, blank=True)

    class AskedQuestion(models.Model):
        """
        List of questions asked by students
        """
        title = models.CharField(max_length=200, default="")
        content = RichTextUploadingField(default='')
        number_views = models.PositiveIntegerField(default=0)
        tags = models.ManyToManyField(Tag)

        topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def get_answers(self):
            return AnswerAskedQuestion.objects.filter(asked_question=self)

    class AnswerAskedQuestion(models.Model):
        """
        List of answers of question by user
        """
        content = RichTextUploadingField()

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        asked_question = models.ForeignKey(AskedQuestion, on_delete=models.CASCADE)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

    class PaperTest(models.Model):
        """
        List of PaperTest
        """
        name = models.CharField(max_length=255)
        total_completion_time = models.IntegerField(default=60)
        difficulty_degree = models.CharField(max_length=1,
                                             choices=DIFFICULTIES,
                                             default="3")
        average_difficulty_degree = models.FloatField(default=1.0)
        number_of_questions = models.IntegerField(default=5)
        marks = models.IntegerField(default=0)

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        questions = models.ManyToManyField(Question)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return self.name
class PracticeSubmission(models.Model):
    """
    List of Submission per Practice Test by each student
    """
    total_marks = models.IntegerField(default=0)

    paper_test = models.ForeignKey(PaperTest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PracticeSubmissionDetail(models.Model):
    """
    List of answer record of PracticeSubmission
    """
    answer = RichTextField(default="")
    answer_result = models.BooleanField(default=True)

    part_name_a = RichTextField(default="")
    part_name_a_result = models.BooleanField(default=True)
    subpart_name_a_1 = RichTextField(default="")
    subpart_name_a_1_result = models.BooleanField(default=True)
    subpart_name_a_2 = RichTextField(default="")
    subpart_name_a_2_result = models.BooleanField(default=True)
    subpart_name_a_3 = RichTextField(default="")
    subpart_name_a_3_result = models.BooleanField(default=True)
    subpart_name_a_4 = RichTextField(default="")
    subpart_name_a_4_result = models.BooleanField(default=True)

    part_name_b = RichTextField(default="")
    part_name_b_result = models.BooleanField(default=True)
    subpart_name_b_1 = RichTextField(default="")
    subpart_name_b_1_result = models.BooleanField(default=True)
    subpart_name_b_2 = RichTextField(default="")
    subpart_name_b_2_result = models.BooleanField(default=True)
    subpart_name_b_3 = RichTextField(default="")
    subpart_name_b_3_result = models.BooleanField(default=True)
    subpart_name_b_4 = RichTextField(default="")
    subpart_name_b_4_result = models.BooleanField(default=True)

    part_name_c = RichTextField(default="")
    part_name_c_result = models.BooleanField(default=True)
    subpart_name_c_1 = RichTextField(default="")
    subpart_name_c_1_result = models.BooleanField(default=True)
    subpart_name_c_2 = RichTextField(default="")
    subpart_name_c_2_result = models.BooleanField(default=True)
    subpart_name_c_3 = RichTextField(default="")
    subpart_name_c_3_result = models.BooleanField(default=True)
    subpart_name_c_4 = RichTextField(default="")
    subpart_name_c_4_result = models.BooleanField(default=True)

    part_name_d = RichTextField(default="")
    part_name_d_result = models.BooleanField(default=True)
    subpart_name_d_1 = RichTextField(default="")
    subpart_name_d_1_result = models.BooleanField(default=True)
    subpart_name_d_2 = RichTextField(default="")
    subpart_name_d_2_result = models.BooleanField(default=True)
    subpart_name_d_3 = RichTextField(default="")
    subpart_name_d_3_result = models.BooleanField(default=True)
    subpart_name_d_4 = RichTextField(default="")
    subpart_name_d_4_result = models.BooleanField(default=True)

    marks = models.IntegerField(default=0)
    is_tried = models.BooleanField(default=False)

    practice_submission = models.ForeignKey(
        PracticeSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPermission(models.Model):
    is_teacher = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Quiz(models.Model):
    """
    List of Quiz
    """

    def __str__(self):
        return self.title

    title = models.CharField(max_length=500, default="")
    description = models.TextField(max_length=1000)
    total_completion_time = models.IntegerField(default=60)
    total_marks = models.IntegerField(default=0)

    questions = models.ManyToManyField(Question)
    education_level = models.ForeignKey(
        EducationLevel, on_delete=models.CASCADE, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuizListQuestion(models.Model):
    mark = models.IntegerField(default=0)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class QuizSubmission(models.Model):
    total_marks = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(default=datetime.now())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuizSubmissionDetail(models.Model):
    final_result = models.BooleanField(default=False)

    answer = RichTextField(default="")
    answer_result = models.BooleanField(default=True)

    part_name_a = RichTextField(default="")
    part_name_a_result = models.BooleanField(default=True)
    part_name_b = RichTextField(default="")
    part_name_b_result = models.BooleanField(default=True)
    part_name_c = RichTextField(default="")
    part_name_c_result = models.BooleanField(default=True)
    part_name_d = RichTextField(default="")
    part_name_d_result = models.BooleanField(default=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_submission = models.ForeignKey(QuizSubmission,
                                        on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PaperFormat(models.Model):
    paper_type = models.CharField(
        choices=PAPER_TYPES,
        default="Sec1",
        max_length=50)
    paper_level = models.CharField(
        choices=PAPER_LEVELS,
        default="Sec1",
        max_length=50)
    paper_number = models.CharField(
        choices=PAPER_NUMBERS,
        default="Sec1",
        max_length=50)
    number_of_questions = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("paper_type", "paper_level", "paper_number")


class PaperFormatQuestion(models.Model):
    mark = models.IntegerField(default=0)

    paper_format = models.ForeignKey(PaperFormat, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MathPaper(models.Model):
    number_views = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_format = models.ForeignKey(PaperFormat, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MathPaperQuestion(models.Model):
    math_paper = models.ForeignKey(MathPaper, on_delete=models.CASCADE)
    paper_format_question = models.ForeignKey(PaperFormatQuestion,
                                              on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

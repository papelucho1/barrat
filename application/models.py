from django.db import models

# Create your models here.

#clase persona, quien realiza el test
class User(models.Model):
    name = models.CharField(max_length=250) 

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


#evaluacion de la persona
class Feedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)  # 0: Created, 1: Updated (or expired), 2: Finished
    temp_answer = models.CharField(max_length=200, null=True)  # Ajax update


    impulsiveness_total = models.IntegerField(null=True)
    impulsiveness_attentional = models.IntegerField(null=True)
    impulsiveness_non_planning =models.IntegerField(null=True)
    impulsiveness_motor = models.IntegerField(null=True)
    #un usuario puede tener varios feedback
    user = models.ManyToManyField(User)

class Profile(models.Model):

    head_comment = models.CharField(max_length=250, primary_key=True)
    comment = models.CharField(max_length=500)
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

"""
class Profile_total(models.Model):   

    self_control = models.CharField(max_length=250)
    comment = models.CharField(max_length=500)
    value_impulsiveness = models.IntegerField()
    #depende del test
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Profile_median(models.Model):

    type_impulsiveness = models.CharField(max_length=200)
    comment = models.CharField(max_length=500)
    value_sub_impulsiveness = models.DecimalField(max_digits=2, decimal_places=1)
    #depende del test
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
"""

class Question(models.Model):
    id_question = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=250) 
    question_type = models.CharField(max_length=1)

    test = models.ForeignKey(Test, on_delete= models.CASCADE)


class Answer(models.Model):
    
    answer_text = models.CharField(max_length=30, null= True)
    value = models.IntegerField()
    #clave foránea pregunta
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
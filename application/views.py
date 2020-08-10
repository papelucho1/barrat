from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

import traceback
# Create your views here.
from .models import * 
import json

def index(request):
   return render( request , "BARRAT/index.html")


def showQuestions(request,test_id ):
    try: 
        test = Test.objects.get(pk = test_id)
    except(KeyError, Test.DoesNotExist):
        raise Http404
    else:    
        new_test = Feedback()
        new_test.save()   
        new_test.user.add(User.objects.get(id=1))
        
        request.session['has_started'] = True
        request.session['Test'] = 'BARRAT'
        request.session['ID_TEST'] = new_test.id

        questions = Question.objects.all()
        answers = Answer.objects.all()


        context = {
            'questions' : questions,
            'answers'   : answers,
            'last_question' : Question.objects.last(),
        }
        
        return render(request ,'BARRAT/content.html',context )


    
def saveAnswers(request):
    try:
        owner = User.objects.get(pk=1)
        answer_id = request.session['ID_TEST']
        this_answer = Feedback.objects.get(pk=answer_id)        

    except (KeyError, Feedback.DoesNotExist):
        raise Http404

    else:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
                  
            #print("asdfas : ",asdf)
            #print(Question.objects.first().id_question)
            #print(Question.objects.last().id_question)

            #----depurar
            #------------
            impul_attentional = 0
            impul_non_planning  = 0
            impul_motor  = 0  
            try:                
                for i in range(Question.objects.first().id_question , Question.objects.last().id_question + 1 ):
                    selectedChoice = request.POST["radio_"+ str(i)]
                    
                    
                    ans = Answer.objects.get(pk=selectedChoice) 


                    quest = ans.id_question
                    print("-----------")
                    print("quest.id_question -> ", quest.id_question)
                    print("quest.question_type -> ", quest.question_type)
                    print("ans.value -> ", ans.value)
                   
                       
                    quest = Question.objects.get(pk= quest.id_question)
                    
                    #no planned
                    if quest.question_type == "1":    
                        impul_non_planning += ans.value    
                        print ("non planned")               
                    #motora
                    elif quest.question_type == "2":
                        impul_motor += ans.value
                        print ("non motora")   
                    #cognitiva
                    elif quest.question_type == "3":
                        impul_attentional += ans.value
                        print ("non cognitiva")   
                    print("-----------")

                
                                                    
                print("after for")    
                impul_total = impul_motor + impul_non_planning + impul_attentional
                print("impul_total -> ", impul_total)
                
                this_answer.impulsiveness_attentional = impul_attentional
                this_answer.impulsiveness_motor = impul_motor
                this_answer.impulsiveness_non_planning = impul_non_planning
                this_answer.impulsiveness_total = impul_total
                this_answer.status = 2
                this_answer.save()

                this_answer.user.add(owner)
                print("save feedback")    

                
                return HttpResponseRedirect(reverse('BARRAT_cert', args=(this_answer.id,)))
            except Exception as e:
                print (type(e))
                trace_back = traceback.format_exc()
                message = str(e)+ " " + str(trace_back)
                print (message)
                raise Http404
            
        else:
            raise Http404




def BARRAT_certificate(request,id_feedback):
    try: 
        feedback = Feedback.objects.get(pk=id_feedback)
    except(KeyError, feedback.DoesNotExist):
        raise Http404
    else:
        if feedback.status == 2:
            user = feedback.user.all().last()

            #punta
          

            #getSubProfile = Profile_median.objects.get()
            #getTotalProfile = Profile_total.objects.get()
            
            #total            
            #alto 0-51
            if feedback.impulsiveness_total in range(29,51):    
                print("here in (29,51): ")            
                getTotalProfile= Profile.objects.get(pk="Alto")
                print(getTotalProfile.comment)
                         
                print()
            #normal 52-73
            if feedback.impulsiveness_total in range(52, 73):
                print("here in (52, 73): ")
                getTotalProfile= Profile.objects.get(pk="Normal")
                
                
               
            #bajo 74 +
            if feedback.impulsiveness_total in range(74, 121):
                print("here in (74, 121) ")
                getTotalProfile= Profile.objects.get(pk="Bajo")
                
               
            

            #subescala
            #Cognitiva 
            if feedback.impulsiveness_attentional <= 9.5:
                attentionalComment = "Adecuado"
            else:
                getProfileMedian = Profile.objects.get(pk="Cognitiva")
                attentionalComment =  getProfileMedian.comment
               
            #Motora
            if feedback.impulsiveness_motor <= 9.5:
                motorComment = "Adecuado"
            else:
                getProfileMedian = Profile.objects.get(pk="Motora")
                motorComment = getProfileMedian.comment

            #No Planificada 
            if feedback.impulsiveness_non_planning <= 14:
                non_PlanningComment = "Adecuado"           
            else:
                getProfileMedian = Profile.objects.get(pk="No Planificada")
                non_PlanningComment = getProfileMedian.comment

           
            print("getTotalProfile: ",getTotalProfile)
            commentTotal = getTotalProfile.comment
            headCommentTotal = getTotalProfile.head_comment
            print(" commentTotal: ",commentTotal)
            context = {
                'feedback': feedback,
                'person': user,
                'commentTotal' : commentTotal,
                'headCommentTotal' : headCommentTotal,
                

                #type of impulsive
                'attentionalComment': attentionalComment,
                'motorComment' : motorComment,
                'non_PlanningComment': non_PlanningComment,
                
               
                #common:
                "user": feedback.user,
                'date': feedback.created_at,
                "status": "Finalizado"
            }

                       
            return render(request, 'certificate/body_BARRAT_certificate.html', context)
        else:
            raise Http404





def ajaxSave(request):
    if request.is_ajax() and request.POST:
        # modificar request session get
        if request.session.get('has_started', True) and request.session.get('Test', 'BARRAT'):
            ans_id = request.session['ID_TEST']
            temp_ans = request.POST.get('answers')
            answer = Feedback.objects.get(pk=ans_id)
            answer.temp_answer = temp_ans
            answer.status = 1
            answer.save()
        # GUARDAR EN LA DB
        data = {"message": "Progreso guardado"}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404
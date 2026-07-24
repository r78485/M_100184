from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import QuestionBank
from .forms import (
    BaseQuestionForm, BanglaQuestionForm, 
    EnglishQuestionForm, MathQuestionForm, ScienceQuestionForm
)

def create_subject_question(request, subject_name):
    subject_code = subject_name.upper()
    
    # বিষয়ভিত্তিক ফর্ম ম্যাপিং
    form_map = {
        'BANGLA': (BanglaQuestionForm, 'বাংলা'),
        'ENGLISH': (EnglishQuestionForm, 'ইংরেজি'),
        'MATH': (MathQuestionForm, 'গণিত'),
        'SCIENCE': (ScienceQuestionForm, 'বিজ্ঞান'),
    }

    if subject_code not in form_map:
        return render(request, '404.html')

    SpecificForm, display_name = form_map[subject_code]

    if request.method == 'POST':
        base_form = BaseQuestionForm(request.POST)
        specific_form = SpecificForm(request.POST, request.FILES)

        if base_form.is_valid() and specific_form.is_valid():
            base_q = base_form.save(commit=False)
            base_q.subject = subject_code
            base_q.save()

            spec_q = specific_form.save(commit=False)
            spec_q.base_question = base_q
            spec_q.save()

            return redirect(reverse('question_success', kwargs={'question_id': base_q.id}))
    else:
        base_form = BaseQuestionForm()
        specific_form = SpecificForm()

    context = {
        'subject_code': subject_code,
        'display_name': display_name,
        'base_form': base_form,
        'specific_form': specific_form,
    }
    return render(request, 'create_manual_question.html', context)


def question_success(request, question_id):
    question = get_object_or_404(QuestionBank, id=question_id)
    
    specific_detail = None
    if question.subject == 'BANGLA' and hasattr(question, 'bangla_detail'):
        specific_detail = question.bangla_detail
    elif question.subject == 'ENGLISH' and hasattr(question, 'english_detail'):
        specific_detail = question.english_detail
    elif question.subject == 'MATH' and hasattr(question, 'math_detail'):
        specific_detail = question.math_detail
    elif question.subject == 'SCIENCE' and hasattr(question, 'science_detail'):
        specific_detail = question.science_detail

    context = {
        'question': question,
        'specific_detail': specific_detail,
    }
    return render(request, 'question_success.html', context)

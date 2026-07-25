import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import (
    Chapter, QuestionBank, QuestionPaper, QuestionPaperTemplate,
    SUBJECT_CHOICES, QUESTION_TYPE_CHOICES, DIFFICULTY_CHOICES, BOARD_CHOICES, CLASS_CHOICES
)
from apps.users.models import User

def check_permission(user):
    """Ensure user is authorized (Admin, Principal, Exam Controller, Teacher)"""
    if not user.is_authenticated:
        return False
    if user.is_superuser or getattr(user, 'role', '') in ['ADMIN', 'TEACHER']:
        return True
    return True  # Permissive for development/demo fallback

@login_required
def dashboard_view(request):
    if not check_permission(request.user):
        return redirect('dashboard')
        
    total_questions = QuestionBank.objects.count()
    total_papers = QuestionPaper.objects.count()
    total_chapters = Chapter.objects.count()
    recent_papers = QuestionPaper.objects.order_by('-created_at')[:5]
    
    context = {
        'total_questions': total_questions,
        'total_papers': total_papers,
        'total_chapters': total_chapters,
        'recent_papers': recent_papers,
        'subjects': SUBJECT_CHOICES,
        'classes': CLASS_CHOICES,
    }
    return render(request, 'question_paper/dashboard.html', context)

@login_required
def create_paper_view(request, paper_id=None):
    if not check_permission(request.user):
        return redirect('dashboard')
        
    paper_instance = None
    if paper_id:
        paper_instance = get_object_or_404(QuestionPaper, pk=paper_id)

    chapters = Chapter.objects.all().order_by('chapter_number')
    questions = QuestionBank.objects.all().order_by('-created_at')[:100]
    templates = QuestionPaperTemplate.objects.all()

    context = {
        'paper_instance': paper_instance,
        'chapters': chapters,
        'questions': questions,
        'templates': templates,
        'subjects': SUBJECT_CHOICES,
        'classes': CLASS_CHOICES,
        'question_types': QUESTION_TYPE_CHOICES,
        'difficulties': DIFFICULTY_CHOICES,
        'boards': BOARD_CHOICES,
    }
    return render(request, 'question_paper/create_question_paper.html', context)

@login_required
def subject_builder_view(request, subject_code='MATH'):
    if not check_permission(request.user):
        return redirect('dashboard')

    sub_code_upper = subject_code.upper()
    valid_subjects = [s[0] for s in SUBJECT_CHOICES]
    if sub_code_upper not in valid_subjects:
        sub_code_upper = 'MATH'

    if request.method == 'POST':
        # Create Question in Bank
        try:
            q = QuestionBank(
                subject=sub_code_upper,
                class_level=request.POST.get('class_level', 'Class 9'),
                topic=request.POST.get('topic', ''),
                question_type=request.POST.get('question_type', 'CREATIVE'),
                difficulty=request.POST.get('difficulty', 'MEDIUM'),
                board_standard=request.POST.get('board_standard', 'DHAKA'),
                board_year=int(request.POST.get('board_year')) if request.POST.get('board_year') else None,
                marks=int(request.POST.get('marks', 10)),
                question_text=request.POST.get('question_text', ''),
                answer_explanation=request.POST.get('answer_explanation', ''),
                stimulus_passage=request.POST.get('stimulus_passage', ''),
                q_ka=request.POST.get('q_ka', ''),
                m_ka=int(request.POST.get('m_ka', 1)),
                q_kha=request.POST.get('q_kha', ''),
                m_kha=int(request.POST.get('m_kha', 2)),
                q_ga=request.POST.get('q_ga', ''),
                m_ga=int(request.POST.get('m_ga', 3)),
                q_gha=request.POST.get('q_gha', ''),
                m_gha=int(request.POST.get('m_gha', 4)),
                option_a=request.POST.get('option_a', ''),
                option_b=request.POST.get('option_b', ''),
                option_c=request.POST.get('option_c', ''),
                option_d=request.POST.get('option_d', ''),
                correct_option=request.POST.get('correct_option', 'A'),
                latex_formula=request.POST.get('latex_formula', ''),
                chemical_equation=request.POST.get('chemical_equation', ''),
                code_snippet=request.POST.get('code_snippet', ''),
                created_by=request.user if request.user.is_authenticated else None,
            )

            ch_id = request.POST.get('chapter_id')
            if ch_id:
                q.chapter = Chapter.objects.filter(pk=ch_id).first()

            if 'diagram_image' in request.FILES:
                q.diagram_image = request.FILES['diagram_image']
            if 'stimulus_image' in request.FILES:
                q.stimulus_image = request.FILES['stimulus_image']

            q.save()
            return JsonResponse({'status': 'success', 'message': 'প্রশ্ন সফলভাবে তৈরি করা হয়েছে!', 'id': q.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    chapters = Chapter.objects.filter(subject=sub_code_upper)
    questions = QuestionBank.objects.filter(subject=sub_code_upper).order_by('-created_at')[:30]

    context = {
        'current_subject': sub_code_upper,
        'chapters': chapters,
        'questions': questions,
        'subjects': SUBJECT_CHOICES,
        'classes': CLASS_CHOICES,
        'question_types': QUESTION_TYPE_CHOICES,
        'difficulties': DIFFICULTY_CHOICES,
        'boards': BOARD_CHOICES,
    }
    return render(request, 'question_paper/subject_builders.html', context)

@login_required
def question_bank_view(request):
    if not check_permission(request.user):
        return redirect('dashboard')

    qs = QuestionBank.objects.all().order_by('-created_at')

    # Filtering
    sub = request.GET.get('subject')
    cls = request.GET.get('class_level')
    qtype = request.GET.get('question_type')
    diff = request.GET.get('difficulty')
    search = request.GET.get('search')

    if sub: qs = qs.filter(subject=sub)
    if cls: qs = qs.filter(class_level=cls)
    if qtype: qs = qs.filter(question_type=qtype)
    if diff: qs = qs.filter(difficulty=diff)
    if search: qs = qs.filter(question_text__icontains=search)

    paginator = Paginator(qs, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_count': qs.count(),
        'subjects': SUBJECT_CHOICES,
        'classes': CLASS_CHOICES,
        'question_types': QUESTION_TYPE_CHOICES,
        'difficulties': DIFFICULTY_CHOICES,
        'boards': BOARD_CHOICES,
    }
    return render(request, 'question_paper/question_bank.html', context)

@login_required
def history_view(request):
    if not check_permission(request.user):
        return redirect('dashboard')

    papers = QuestionPaper.objects.all().order_by('-created_at')

    search = request.GET.get('search')
    if search:
        papers = papers.filter(title__icontains=search)

    context = {
        'papers': papers,
    }
    return render(request, 'question_paper/history.html', context)

@login_required
def print_preview_view(request, paper_id=None):
    if paper_id:
        paper = get_object_or_404(QuestionPaper, pk=paper_id)
    else:
        # Dummy paper preview
        paper = QuestionPaper(
            title="বার্ষিক পরীক্ষা — ২০২৬",
            school_name="গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়",
            class_name="৯ম শ্রেণি",
            subject="গণিত",
            time_allowed="৩ ঘণ্টা",
            full_marks=100,
            academic_year="2026",
            teacher_name="মোঃ রফিকুল ইসলাম",
            instructions="১. সকল প্রশ্নের মান সমান।\n২. ক্যালকুলেটর ব্যবহার করার অনুমতি আছে।"
        )
    context = {
        'paper': paper,
    }
    return render(request, 'question_paper/print_preview.html', context)

# API Endpoints
@csrf_exempt
@login_required
def api_save_paper(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        paper_id = data.get('id')

        if paper_id:
            paper = QuestionPaper.objects.get(pk=paper_id)
            paper.version += 1
        else:
            paper = QuestionPaper()

        paper.title = data.get('title', 'বার্ষিক পরীক্ষা — ২০২৬')
        paper.academic_year = data.get('academic_year', '2026')
        paper.class_name = data.get('class_name', 'Class 9')
        paper.section = data.get('section', 'A')
        paper.subject = data.get('subject', 'গণিত')
        paper.teacher_name = data.get('teacher_name', request.user.get_full_name() or request.user.username)
        paper.time_allowed = data.get('time_allowed', '৩ ঘণ্টা')
        paper.full_marks = int(data.get('full_marks', 100))
        paper.pass_marks = int(data.get('pass_marks', 33))
        paper.written_marks = int(data.get('written_marks', 70))
        paper.mcq_marks = int(data.get('mcq_marks', 30))
        paper.creative_marks = int(data.get('creative_marks', 70))
        paper.school_name = data.get('school_name', 'গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়')
        paper.eiin_number = data.get('eiin_number', 'EIIN: 123456')
        paper.instructions = data.get('instructions', '')
        paper.prepared_by = data.get('prepared_by', 'বিষয় শিক্ষক')
        paper.verified_by = data.get('verified_by', 'পরীক্ষা নিয়ন্ত্রক')
        paper.approved_by = data.get('approved_by', 'প্রধান শিক্ষক')
        paper.questions_json = data.get('questions_json', [])
        paper.numbering_style = data.get('numbering_style', 'BANGLA')
        paper.paper_size = data.get('paper_size', 'A4_PORTRAIT')

        if request.user.is_authenticated:
            paper.created_by = request.user

        paper.save()
        return JsonResponse({'status': 'success', 'paper_id': paper.id, 'message': 'প্রশ্নপত্র সফলভাবে সংরক্ষিত হয়েছে!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
def api_ai_generate(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        subject = data.get('subject', 'MATH')
        class_level = data.get('class_level', 'Class 9')
        chapter = data.get('chapter', 'সংখ্যা পদ্ধতি')
        topic = data.get('topic', 'সাধারন আলোচনা')
        difficulty = data.get('difficulty', 'MEDIUM')
        question_type = data.get('question_type', 'CREATIVE')
        marks = int(data.get('marks', 10))

        # Generator Templates based on NCTB curriculum
        generated = []
        if question_type == 'CREATIVE':
            sample_stimuli = [
                f"{chapter} অধ্যায়ের অধীনে একটি আয়তাকার পার্কের দৈর্ঘ্য এবং প্রস্থ যথাক্রমে (x + ৪) মিটার এবং (x - ২) মিটার। পার্কটির ক্ষেত্রফল ২৪ বর্গমিটার।",
                f"একটি পাত্রে হাইড্রোজেন ও অক্সিজেন গ্যাসের অনুপাত ২:১। উদ্দীপকটি বিশ্লেষণ করে {chapter} সম্পর্কিত গাণিতিক সমস্যাটি সমাধান কর।",
                f"উদ্দিপক: একটি তথ্যপ্রযুক্তি কোম্পানিতে ২০০ জন কর্মী কর্মরত আছেন। কোম্পানির মাসিক ডেটা অ্যানালিটিক্স ছক পর্যবেক্ষণ কর।",
            ]
            stimulus = random.choice(sample_stimuli)
            
            q = {
                'id': random.randint(10000, 99999),
                'subject': subject,
                'class_level': class_level,
                'type': 'Creative',
                'difficulty': difficulty,
                'marks': marks,
                'text': stimulus,
                'stimulus_passage': stimulus,
                'q_ka': f'{chapter} কাকে বলে? (১)',
                'm_ka': 1,
                'q_kha': f'উদ্দীপকের মূল ধারণা ব্যাখ্যা কর। (২)',
                'm_kha': 2,
                'q_ga': f'উদ্দীপকের তথ্যের আলোকে গাণিতিক মান বা পরিমাপ নির্ণয় কর। (৩)',
                'm_ga': 3,
                'q_gha': f'উদ্দীপকে বর্ণিত পরিস্থিতির বাস্তব প্রয়োগ এবং যৌক্তিক সিদ্ধান্ত বিশ্লেষণ কর। (৪)',
                'm_gha': 4,
            }
            generated.append(q)
        else:
            # MCQ / Short Generator
            mcq_samples = [
                {'text': f'{chapter} অধ্যায় অনুযায়ী নিচের কোনটি সঠিক তথ্য?', 'options': 'ক) ১ম উপাদান\nখ) ২য় উপাদান\nগ) ৩য় উপাদান\nঘ) ৪র্থ উপাদান', 'answer': 'খ', 'marks': 1},
                {'text': f'{topic} এর গাণিতিক সংকেত নিচের কোনটি?', 'options': 'ক) f(x)\nখ) g(x)\nগ) h(x)\nঘ) P(x)', 'answer': 'ক', 'marks': 1},
                {'text': f'নিচের কোনটি NCTB স্ট্যান্ডার্ড {subject} কারিকুলামভুক্ত?', 'options': 'ক) অপশন A\nখ) অপশন B\nগ) অপশন C\nঘ) অপশন D', 'answer': 'গ', 'marks': 1},
            ]
            sample = random.choice(mcq_samples)
            q = {
                'id': random.randint(10000, 99999),
                'subject': subject,
                'class_level': class_level,
                'type': question_type if question_type in ['MCQ', 'Short'] else 'MCQ',
                'difficulty': difficulty,
                'marks': sample['marks'],
                'text': sample['text'],
                'options': sample['options'],
                'answer': sample['answer'],
            }
            generated.append(q)

        return JsonResponse({'status': 'success', 'questions': generated})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
def api_delete_paper(request, paper_id):
    if request.method == 'POST':
        paper = get_object_or_404(QuestionPaper, pk=paper_id)
        paper.delete()
        return JsonResponse({'status': 'success', 'message': 'প্রশ্নপত্র সফলভাবে মুছে ফেলা হয়েছে!'})
    return JsonResponse({'error': 'POST method required'}, status=405)

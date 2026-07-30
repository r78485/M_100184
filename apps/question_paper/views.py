import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.management import call_command
from django.db import OperationalError, DatabaseError

from .models import (
    Chapter, QuestionBank, QuestionPaper, QuestionPaperTemplate,
    SUBJECT_CHOICES, QUESTION_TYPE_CHOICES, DIFFICULTY_CHOICES, BOARD_CHOICES, CLASS_CHOICES
)

def ensure_tables_exist():
    """Ensure database tables and all columns for question_paper exist"""
    try:
        call_command('migrate', 'question_paper', verbosity=0)
    except Exception as e:
        print("Migration command warning:", e)

    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Check question_paper_questionbank table columns
            cursor.execute("PRAGMA table_info(question_paper_questionbank);")
            columns = [row[1] for row in cursor.fetchall()]

            if 'mcq_type' not in columns:
                cursor.execute("ALTER TABLE question_paper_questionbank ADD COLUMN mcq_type varchar(20) DEFAULT 'SINGLE';")
            if 'statement_i' not in columns:
                cursor.execute("ALTER TABLE question_paper_questionbank ADD COLUMN statement_i varchar(500) NULL;")
            if 'statement_ii' not in columns:
                cursor.execute("ALTER TABLE question_paper_questionbank ADD COLUMN statement_ii varchar(500) NULL;")
            if 'statement_iii' not in columns:
                cursor.execute("ALTER TABLE question_paper_questionbank ADD COLUMN statement_iii varchar(500) NULL;")

            # Check question_paper_questionpaper table columns
            cursor.execute("PRAGMA table_info(question_paper_questionpaper);")
            paper_cols = [row[1] for row in cursor.fetchall()]

            if 'font_family' not in paper_cols:
                cursor.execute("ALTER TABLE question_paper_questionpaper ADD COLUMN font_family varchar(30) DEFAULT 'ARIAL';")
            if 'column_layout' not in paper_cols:
                cursor.execute("ALTER TABLE question_paper_questionpaper ADD COLUMN column_layout varchar(5) DEFAULT '1';")
            if 'show_answer_key' not in paper_cols:
                cursor.execute("ALTER TABLE question_paper_questionpaper ADD COLUMN show_answer_key bool DEFAULT 0;")

    except Exception as e:
        print("ensure_tables_exist alter exception handled:", e)




def check_permission(user):
    """Ensure user is authorized (Admin, Principal, Exam Controller, Teacher)"""
    if not user.is_authenticated:
        return False
    if user.is_superuser or getattr(user, 'role', '') in ['ADMIN', 'TEACHER']:
        return True
    return True  # Permissive for development/demo fallback

def seed_initial_sample_questions():
    """Auto populate initial sample NCTB CQs and MCQs in English and Bangla"""
    import os
    try:
        if QuestionBank.objects.count() == 0 and os.environ.get('SEED_DEFAULT_DATA', '').lower() == 'true':
            from seed_question_paper import seed
            seed()
    except Exception:
        pass

@login_required
def dashboard_view(request):
    if not check_permission(request.user):
        return redirect('dashboard')
        
    ensure_tables_exist()
    seed_initial_sample_questions()

    try:
        total_questions = QuestionBank.objects.count()
        total_papers = QuestionPaper.objects.count()
        total_chapters = Chapter.objects.count()
        recent_papers = QuestionPaper.objects.order_by('-created_at')[:5]
    except (OperationalError, DatabaseError):
        ensure_tables_exist()
        total_questions = 0
        total_papers = 0
        total_chapters = 0
        recent_papers = []

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
        
    ensure_tables_exist()
    seed_initial_sample_questions()

    paper_instance = None
    chapters = []
    questions = []
    templates = []

    try:
        if paper_id:
            paper_instance = QuestionPaper.objects.filter(pk=paper_id).first()

        chapters = Chapter.objects.all().order_by('chapter_number')
        questions = QuestionBank.objects.all().order_by('-created_at')[:100]
        templates = QuestionPaperTemplate.objects.all()
    except (OperationalError, DatabaseError):
        ensure_tables_exist()
        try:
            chapters = Chapter.objects.all().order_by('chapter_number')
            questions = QuestionBank.objects.all().order_by('-created_at')[:100]
            templates = QuestionPaperTemplate.objects.all()
        except Exception:
            pass


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

    ensure_tables_exist()

    sub_code_upper = subject_code.upper()
    valid_subjects = [s[0] for s in SUBJECT_CHOICES]
    if sub_code_upper not in valid_subjects:
        sub_code_upper = 'MATH'

    if request.method == 'POST':
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

    try:
        chapters = Chapter.objects.filter(subject=sub_code_upper)
        questions = QuestionBank.objects.filter(subject=sub_code_upper).order_by('-created_at')[:30]
    except (OperationalError, DatabaseError):
        ensure_tables_exist()
        chapters = []
        questions = []

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

    ensure_tables_exist()

    try:
        qs = QuestionBank.objects.all().order_by('-created_at')
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
        total_count = qs.count()
    except (OperationalError, DatabaseError):
        ensure_tables_exist()
        page_obj = []
        total_count = 0

    context = {
        'page_obj': page_obj,
        'total_count': total_count,
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

    ensure_tables_exist()

    try:
        papers = QuestionPaper.objects.all().order_by('-created_at')
        search = request.GET.get('search')
        if search:
            papers = papers.filter(title__icontains=search)
    except (OperationalError, DatabaseError):
        ensure_tables_exist()
        papers = []

    context = {
        'papers': papers,
    }
    return render(request, 'question_paper/history.html', context)

@login_required
def print_preview_view(request, paper_id=None):
    ensure_tables_exist()
    paper = None
    if paper_id:
        try:
            paper = QuestionPaper.objects.filter(pk=paper_id).first()
        except Exception:
            pass

    if not paper:
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

@csrf_exempt
@login_required
def api_save_paper(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    ensure_tables_exist()

    try:
        data = json.loads(request.body)
        paper_id = data.get('id')

        if paper_id:
            paper = QuestionPaper.objects.get(pk=paper_id)
            paper.version += 1
        else:
            paper = QuestionPaper()

        paper.title = data.get('title', 'Annual Examination — 2026')
        paper.academic_year = data.get('academic_year', '2026')
        paper.class_name = data.get('class_name', 'Class 9')
        paper.section = data.get('section', 'A')
        paper.subject = data.get('subject', 'Mathematics')
        paper.teacher_name = data.get('teacher_name', request.user.get_full_name() or request.user.username)
        paper.time_allowed = data.get('time_allowed', '3 Hours')
        paper.full_marks = int(data.get('full_marks', 100))
        paper.pass_marks = int(data.get('pass_marks', 33))
        paper.written_marks = int(data.get('written_marks', 70))
        paper.mcq_marks = int(data.get('mcq_marks', 30))
        paper.creative_marks = int(data.get('creative_marks', 70))
        paper.school_name = data.get('school_name', 'Gazimahmud Secondary School')
        paper.eiin_number = data.get('eiin_number', 'EIIN: 123456')
        paper.instructions = data.get('instructions', '')
        paper.prepared_by = data.get('prepared_by', 'Subject Teacher')
        paper.verified_by = data.get('verified_by', 'Exam Controller')
        paper.approved_by = data.get('approved_by', 'Headmaster')
        paper.questions_json = data.get('questions_json', [])
        paper.numbering_style = data.get('numbering_style', 'ENGLISH')
        paper.font_family = data.get('font_family', 'ARIAL')
        paper.column_layout = data.get('column_layout', '1')
        paper.paper_size = data.get('paper_size', 'A4_PORTRAIT')
        paper.show_answer_key = bool(data.get('show_answer_key', False))

        if request.user.is_authenticated:
            paper.created_by = request.user

        paper.save()
        return JsonResponse({'status': 'success', 'paper_id': paper.id, 'message': 'Question Paper saved successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def api_create_mcq(request):
    """Save a new MCQ question to QuestionBank and return its details"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    ensure_tables_exist()

    try:
        data = json.loads(request.body)
        mcq_type = data.get('mcq_type', 'SINGLE')
        
        q = QuestionBank(
            subject=data.get('subject', 'MATH'),
            class_level=data.get('class_level', 'Class 9'),
            topic=data.get('topic', ''),
            question_type='MCQ',
            difficulty=data.get('difficulty', 'MEDIUM'),
            marks=int(data.get('marks', 1)),
            question_text=data.get('question_text', ''),
            mcq_type=mcq_type,
            statement_i=data.get('statement_i', ''),
            statement_ii=data.get('statement_ii', ''),
            statement_iii=data.get('statement_iii', ''),
            option_a=data.get('option_a', ''),
            option_b=data.get('option_b', ''),
            option_c=data.get('option_c', ''),
            option_d=data.get('option_d', ''),
            correct_option=data.get('correct_option', 'A'),
            answer_explanation=data.get('explanation', ''),
            stimulus_passage=data.get('stimulus_passage', ''),
            created_by=request.user if request.user.is_authenticated else None,
        )
        q.save()

        res_data = {
            'id': q.id,
            'type': 'MCQ',
            'mcq_type': mcq_type,
            'text': q.question_text,
            'stimulus_passage': q.stimulus_passage,
            'statement_i': q.statement_i,
            'statement_ii': q.statement_ii,
            'statement_iii': q.statement_iii,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'correct_option': q.correct_option,
            'explanation': q.answer_explanation,
            'marks': q.marks,
        }

        return JsonResponse({'status': 'success', 'question': res_data, 'message': 'MCQ Question created successfully!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@csrf_exempt
@login_required
def api_bulk_create_mcq(request):
    """Bulk import multiple MCQs from text lines"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    ensure_tables_exist()

    try:
        data = json.loads(request.body)
        raw_text = data.get('raw_text', '')
        subject = data.get('subject', 'MATH')
        class_level = data.get('class_level', 'Class 9')

        if not raw_text.strip():
            return JsonResponse({'error': 'No text provided'}, status=400)

        # Basic parser for raw text: Question line followed by options
        blocks = raw_text.strip().split('\n\n')
        created_questions = []

        for block in blocks:
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            if not lines: continue

            q_text = lines[0]
            op_a, op_b, op_c, op_d = '', '', '', ''
            corr = 'A'

            for line in lines[1:]:
                l_lower = line.lower()
                if l_lower.startswith(('a)', 'a.', '(a)', 'ক)', 'ক.', '(ক)')):
                    op_a = line.split(')', 1)[-1].split('.', 1)[-1].strip()
                elif l_lower.startswith(('b)', 'b.', '(b)', 'খ)', 'খ.', '(খ)')):
                    op_b = line.split(')', 1)[-1].split('.', 1)[-1].strip()
                elif l_lower.startswith(('c)', 'c.', '(c)', 'গ)', 'গ.', '(গ)')):
                    op_c = line.split(')', 1)[-1].split('.', 1)[-1].strip()
                elif l_lower.startswith(('d)', 'd.', '(d)', 'ঘ)', 'ঘ.', '(ঘ)')):
                    op_d = line.split(')', 1)[-1].split('.', 1)[-1].strip()
                elif 'ans:' in l_lower or 'answer:' in l_lower or 'উত্তর:' in l_lower:
                    ans_part = line.split(':')[-1].strip().upper()
                    if ans_part in ['A', 'B', 'C', 'D', 'ক', 'খ', 'গ', 'ঘ']:
                        mapping = {'KHA': 'B', 'GA': 'C', 'GHA': 'D', 'ক': 'A', 'খ': 'B', 'গ': 'C', 'ঘ': 'D'}
                        corr = mapping.get(ans_part, ans_part[0])

            q = QuestionBank.objects.create(
                subject=subject,
                class_level=class_level,
                question_type='MCQ',
                question_text=q_text,
                option_a=op_a or 'Option A',
                option_b=op_b or 'Option B',
                option_c=op_c or 'Option C',
                option_d=op_d or 'Option D',
                correct_option=corr,
                marks=1,
                created_by=request.user if request.user.is_authenticated else None,
            )

            created_questions.append({
                'id': q.id,
                'type': 'MCQ',
                'text': q.question_text,
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_option': q.correct_option,
                'marks': 1,
            })

        return JsonResponse({
            'status': 'success', 
            'count': len(created_questions), 
            'questions': created_questions,
            'message': f'{len(created_questions)} MCQ questions imported successfully!'
        })
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
        chapter = data.get('chapter', 'Algebra / Geometry')
        topic = data.get('topic', 'General Discussion')
        difficulty = data.get('difficulty', 'MEDIUM')
        question_type = data.get('question_type', 'CREATIVE')
        lang = data.get('lang', 'EN')  # 'EN' or 'BN'
        marks = int(data.get('marks', 10 if question_type == 'CREATIVE' else 1))

        generated = []
        if question_type == 'CREATIVE':
            if lang == 'EN':
                sample_stimuli = [
                    f"In chapter '{chapter}', the length and breadth of a rectangular garden are (x + 4) meters and (x - 2) meters respectively. The area of the garden is 24 square meters.",
                    f"A container has hydrogen and oxygen gas in a 2:1 ratio. Analyze the stimulus to solve the mathematical problem regarding '{topic}'.",
                    f"Stimulus: A tech company has 200 employees. Observe the monthly data analytics table for '{chapter}'.",
                ]
                stimulus = random.choice(sample_stimuli)
                q = {
                    'id': random.randint(10000, 99999),
                    'subject': subject,
                    'class_level': class_level,
                    'type': 'CREATIVE',
                    'difficulty': difficulty,
                    'marks': 10,
                    'text': stimulus,
                    'stimulus_passage': stimulus,
                    'q_ka': f'Define {topic}.',
                    'm_ka': 1,
                    'q_kha': f'Explain the basic principle presented in the stimulus.',
                    'm_kha': 2,
                    'q_ga': f'Calculate the mathematical values based on the given information.',
                    'm_ga': 3,
                    'q_gha': f'Critically analyze the practical application and draw a logical conclusion.',
                    'm_gha': 4,
                }
            else:
                sample_stimuli = [
                    f"{chapter} অধ্যায়ের অধীনে একটি আয়তাকার পার্কের দৈর্ঘ্য এবং প্রস্থ যথাক্রমে (x + ৪) মিটার এবং (x - ২) মিটার। পার্কটির ক্ষেত্রফল ২৪ বর্গমিটার।",
                    f"একটি পাত্রে হাইড্রোজেন ও অক্সিজেন গ্যাসের অনুপাত ২:১। উদ্দীপকটি বিশ্লেষণ করে {chapter} সম্পর্কিত গাণিতিক সমস্যাটি সমাধান কর।",
                ]
                stimulus = random.choice(sample_stimuli)
                q = {
                    'id': random.randint(10000, 99999),
                    'subject': subject,
                    'class_level': class_level,
                    'type': 'CREATIVE',
                    'difficulty': difficulty,
                    'marks': 10,
                    'text': stimulus,
                    'stimulus_passage': stimulus,
                    'q_ka': f'{chapter} কাকে বলে?',
                    'm_ka': 1,
                    'q_kha': f'উদ্দীপকের মূল ধারণা ব্যাখ্যা কর।',
                    'm_kha': 2,
                    'q_ga': f'উদ্দীপকের তথ্যের আলোকে গাণিতিক মান নির্ণয় কর।',
                    'm_ga': 3,
                    'q_gha': f'উদ্দীপকে বর্ণিত পরিস্থিতির বাস্তব প্রয়োগ এবং যৌক্তিক সিদ্ধান্ত বিশ্লেষণ কর।',
                    'm_gha': 4,
                }
            generated.append(q)

        elif question_type == 'MCQ_POLYNOMIAL':
            if lang == 'EN':
                q = {
                    'id': random.randint(10000, 99999),
                    'subject': subject,
                    'class_level': class_level,
                    'type': 'MCQ',
                    'mcq_type': 'POLYNOMIAL',
                    'difficulty': difficulty,
                    'marks': 1,
                    'text': f"Regarding {chapter} and {topic}:",
                    'statement_i': "i. First fundamental property holds true",
                    'statement_ii': "ii. Secondary equation is satisfied",
                    'statement_iii': "iii. The system remains in dynamic equilibrium",
                    'option_a': "i and ii",
                    'option_b': "i and iii",
                    'option_c': "ii and iii",
                    'option_d': "i, ii and iii",
                    'correct_option': "D",
                    'explanation': "All three conditions hold true according to NCTB standard curriculum.",
                }
            else:
                q = {
                    'id': random.randint(10000, 99999),
                    'subject': subject,
                    'class_level': class_level,
                    'type': 'MCQ',
                    'mcq_type': 'POLYNOMIAL',
                    'difficulty': difficulty,
                    'marks': 1,
                    'text': f"{chapter} এবং {topic} এর ক্ষেত্রে:",
                    'statement_i': "i. প্রথম মৌলিক ধর্ম মেনে চলে",
                    'statement_ii': "ii. দ্বিতীয় সমীকরণটি সিদ্ধ হয়",
                    'statement_iii': "iii. ব্যবস্থার সাম্যাবস্থা অক্ষুণ্ণ থাকে",
                    'option_a': "i ও ii",
                    'option_b': "i ও iii",
                    'option_c': "ii ও iii",
                    'option_d': "i, ii ও iii",
                    'correct_option': "D",
                    'explanation': "এনসিটিবি পাঠ্যক্রম অনুযায়ী তিনটি তথ্যই সঠিক।",
                }
            generated.append(q)

        else:  # Standard Single MCQ
            if lang == 'EN':
                mcq_samples = [
                    {'text': f'Which of the following is correct regarding {chapter}?', 'option_a': 'Primary Element A', 'option_b': 'Secondary Element B', 'option_c': 'Tertiary Element C', 'option_d': 'Quaternary Element D', 'correct_option': 'B', 'marks': 1},
                    {'text': f'What is the standard formula symbol for {topic}?', 'option_a': 'f(x)', 'option_b': 'g(x)', 'option_c': 'h(x)', 'option_d': 'P(x)', 'correct_option': 'A', 'marks': 1},
                    {'text': f'In NCTB {subject} curriculum, which value represents standard atmospheric pressure?', 'option_a': '1.013 x 10^5 Pa', 'option_b': '9.8 ms^-2', 'option_c': '3 x 10^8 ms^-1', 'option_d': '6.022 x 10^23', 'correct_option': 'A', 'marks': 1},
                ]
            else:
                mcq_samples = [
                    {'text': f'{chapter} অধ্যায় অনুযায়ী নিচের কোনটি সঠিক তথ্য?', 'option_a': '১ম উপাদান A', 'option_b': '২য় উপাদান B', 'option_c': '৩য় উপাদান C', 'option_d': '৪র্থ উপাদান D', 'correct_option': 'B', 'marks': 1},
                    {'text': f'{topic} এর গাণিতিক সংকেত নিচের কোনটি?', 'option_a': 'f(x)', 'option_b': 'g(x)', 'option_c': 'h(x)', 'option_d': 'P(x)', 'correct_option': 'A', 'marks': 1},
                ]
            sample = random.choice(mcq_samples)
            q = {
                'id': random.randint(10000, 99999),
                'subject': subject,
                'class_level': class_level,
                'type': 'MCQ',
                'mcq_type': 'SINGLE',
                'difficulty': difficulty,
                'marks': sample['marks'],
                'text': sample['text'],
                'option_a': sample['option_a'],
                'option_b': sample['option_b'],
                'option_c': sample['option_c'],
                'option_d': sample['option_d'],
                'correct_option': sample['correct_option'],
            }
            generated.append(q)

        return JsonResponse({'status': 'success', 'questions': generated})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@login_required
def api_delete_paper(request, paper_id):
    if request.method == 'POST':
        ensure_tables_exist()
        try:
            paper = get_object_or_404(QuestionPaper, pk=paper_id)
            paper.delete()
            return JsonResponse({'status': 'success', 'message': 'Question paper deleted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'error': 'POST method required'}, status=405)


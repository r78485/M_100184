import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from apps.question_paper.models import QuestionBank, Chapter, QuestionPaper

def seed():
    print("Seeding NCTB Question Bank sample questions...")
    
    # 1. Create sample chapters if none exist
    ch_math, _ = Chapter.objects.get_or_create(
        subject='MATH',
        class_level='Class 9',
        chapter_number=1,
        defaults={'title': 'Algebraic Expressions & Equations', 'description': 'Algebraic formulas, factorization, and quadratic systems'}
    )

    ch_sci, _ = Chapter.objects.get_or_create(
        subject='SCIENCE',
        class_level='Class 9',
        chapter_number=2,
        defaults={'title': 'Photosynthesis and Energy Flow', 'description': 'Light and dark reactions in green plants'}
    )

    # 2. Add English & Bangla Sample MCQs
    mcqs = [
        {
            'subject': 'MATH',
            'class_level': 'Class 9',
            'question_type': 'MCQ',
            'mcq_type': 'SINGLE',
            'question_text': 'If x + 1/x = 5, what is the value of x^2 + 1/x^2?',
            'option_a': '23',
            'option_b': '25',
            'option_c': '27',
            'option_d': '110',
            'correct_option': 'A',
            'answer_explanation': '(x + 1/x)^2 - 2 = 25 - 2 = 23',
            'marks': 1,
            'difficulty': 'MEDIUM',
        },
        {
            'subject': 'MATH',
            'class_level': 'Class 9',
            'question_type': 'MCQ',
            'mcq_type': 'POLYNOMIAL',
            'question_text': 'Regarding the algebraic equation x^2 - 5x + 6 = 0:',
            'statement_i': 'i. The roots of the equation are 2 and 3',
            'statement_ii': 'ii. The sum of the roots is 5',
            'statement_iii': 'iii. The product of the roots is 6',
            'option_a': 'i & ii',
            'option_b': 'i & iii',
            'option_c': 'ii & iii',
            'option_d': 'i, ii & iii',
            'correct_option': 'D',
            'answer_explanation': 'All three statements are correct according to Vieta formulas.',
            'marks': 1,
            'difficulty': 'MEDIUM',
        },
        {
            'subject': 'PHYSICS',
            'class_level': 'Class 9',
            'question_type': 'MCQ',
            'mcq_type': 'SINGLE',
            'question_text': 'Which of the following represents acceleration due to gravity on Earth surface?',
            'option_a': '9.8 m/s^2',
            'option_b': '9.8 km/s',
            'option_c': '6.673 x 10^-11 N m^2/kg^2',
            'option_d': '3 x 10^8 m/s',
            'correct_option': 'A',
            'answer_explanation': 'Standard Earth acceleration due to gravity g = 9.8 m/s^2',
            'marks': 1,
            'difficulty': 'EASY',
        },
        {
            'subject': 'BANGLA_1',
            'class_level': 'Class 9',
            'question_type': 'MCQ',
            'mcq_type': 'SINGLE',
            'question_text': 'নিচের কোনটি রবীন্দ্র কাব্যের প্রধান বৈশিষ্ট্য?',
            'option_a': 'মানবতাবাদ ও রূপক চেতনা',
            'option_b': 'কেবলমাত্র ঐতিহাসিক কাহিনী',
            'option_c': 'নাটকীয় সংলাপ',
            'option_d': 'হাস্যরস',
            'correct_option': 'A',
            'marks': 1,
            'difficulty': 'EASY',
        },
        {
            'subject': 'CHEMISTRY',
            'class_level': 'Class 9',
            'question_type': 'MCQ',
            'mcq_type': 'SINGLE',
            'question_text': 'What is the molecular formula of Sulfuric Acid?',
            'option_a': 'HNO3',
            'option_b': 'H2SO4',
            'option_c': 'HCl',
            'option_d': 'CaCO3',
            'correct_option': 'B',
            'marks': 1,
            'difficulty': 'EASY',
        },
    ]

    for data in mcqs:
        QuestionBank.objects.get_or_create(
            question_text=data['question_text'],
            subject=data['subject'],
            defaults=data
        )

    # 3. Add Creative Questions (CQ)
    cqs = [
        {
            'subject': 'MATH',
            'class_level': 'Class 9',
            'question_type': 'CREATIVE',
            'question_text': 'The length and breadth of a rectangular garden are (x + 4) meters and (x - 2) meters respectively. The total area of the garden is 24 square meters.',
            'stimulus_passage': 'The length and breadth of a rectangular garden are (x + 4) meters and (x - 2) meters respectively. The total area of the garden is 24 square meters.',
            'q_ka': 'Write down the standard algebraic formula for the area of a rectangle.',
            'm_ka': 1,
            'q_kha': 'Formulate the quadratic equation based on the given stimulus condition.',
            'm_kha': 2,
            'q_ga': 'Find the exact value of x and calculate the perimeter of the garden.',
            'm_ga': 3,
            'q_gha': 'If a 2-meter wide pathway is constructed inside around the garden, calculate the cost to pave the path at $5 per sq meter.',
            'm_gha': 4,
            'marks': 10,
            'difficulty': 'MEDIUM',
        },
        {
            'subject': 'SCIENCE',
            'class_level': 'Class 9',
            'question_type': 'CREATIVE',
            'question_text': 'Green plants prepare glucose using carbon dioxide, water, and sunlight in the presence of chlorophyll.',
            'stimulus_passage': 'Green plants prepare glucose using carbon dioxide, water, and sunlight in the presence of chlorophyll.',
            'q_ka': 'What is photosynthesis?',
            'm_ka': 1,
            'q_kha': 'Explain why light-dependent reaction occurs in thylakoid membranes.',
            'm_kha': 2,
            'q_ga': 'Write the balanced chemical reaction for photosynthesis.',
            'm_ga': 3,
            'q_gha': 'Analyze the role of light intensity on the rate of oxygen release.',
            'm_gha': 4,
            'marks': 10,
            'difficulty': 'MEDIUM',
        }
    ]

    for data in cqs:
        QuestionBank.objects.get_or_create(
            question_text=data['question_text'],
            subject=data['subject'],
            defaults=data
        )

    print("✅ Question Bank seeding completed successfully!")

if __name__ == '__main__':
    seed()

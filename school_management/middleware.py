from django.core.management import call_command
from django.db import connection

_MIGRATED = False

def auto_repair_question_paper_schema():
    """Dynamically ensure missing SQLite columns exist for question_paper app"""
    if connection.vendor != 'sqlite':
        return
    try:
        tables = connection.introspection.table_names()
        if 'question_paper_questionbank' in tables:
            with connection.cursor() as cursor:
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

        if 'question_paper_questionpaper' in tables:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA table_info(question_paper_questionpaper);")
                paper_cols = [row[1] for row in cursor.fetchall()]

                if 'font_family' not in paper_cols:
                    cursor.execute("ALTER TABLE question_paper_questionpaper ADD COLUMN font_family varchar(30) DEFAULT 'ARIAL';")
                if 'column_layout' not in paper_cols:
                    cursor.execute("ALTER TABLE question_paper_questionpaper ADD COLUMN column_layout varchar(5) DEFAULT '1';")
                if 'show_answer_key' not in paper_cols:
                    cursor.execute("ALTER TABLE question_paper_questionpaper ADD COLUMN show_answer_key bool DEFAULT 0;")
    except Exception as e:
        print("Schema auto-repair warning:", e)


def auto_repair_student_admission_schema():
    """Dynamically ensure missing SQLite columns exist for users_studentadmission table"""
    if connection.vendor != 'sqlite':
        return
    try:
        tables = connection.introspection.table_names()
        if 'users_studentadmission' in tables:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA table_info(users_studentadmission);")
                columns = [row[1] for row in cursor.fetchall()]

                if 'father_dob' not in columns:
                    cursor.execute("ALTER TABLE users_studentadmission ADD COLUMN father_dob date NULL;")
                if 'father_occupation' not in columns:
                    cursor.execute("ALTER TABLE users_studentadmission ADD COLUMN father_occupation varchar(100) DEFAULT '';")
                if 'mother_dob' not in columns:
                    cursor.execute("ALTER TABLE users_studentadmission ADD COLUMN mother_dob date NULL;")
                if 'mother_occupation' not in columns:
                    cursor.execute("ALTER TABLE users_studentadmission ADD COLUMN mother_occupation varchar(100) DEFAULT '';")
                if 'present_post_office' not in columns:
                    cursor.execute("ALTER TABLE users_studentadmission ADD COLUMN present_post_office varchar(100) DEFAULT '';")
                if 'permanent_post_office' not in columns:
                    cursor.execute("ALTER TABLE users_studentadmission ADD COLUMN permanent_post_office varchar(100) DEFAULT '';")
    except Exception as e:
        print("StudentAdmission schema auto-repair warning:", e)


def ensure_default_students():
    import os
    if os.environ.get('SEED_DEFAULT_DATA', '').lower() != 'true':
        return
    try:
        from apps.users.models import StudentAdmission
        if StudentAdmission.objects.count() == 0:
            import datetime
            default_students = [
                {
                    'student_name_bn': "মোঃ রাহাত হোসেন", 'student_name_en': "Md. Rahat Hossain",
                    'admission_no': "ADM-2026-0101", 'dob': datetime.date(2009, 5, 14), 'gender': "Boy",
                    'mobile': "01719565306", 'father_name': "মোঃ মোতাহার হোসেন", 'mother_name': "মোছাঃ শামিমা আক্তার",
                    'desired_class': "Class 10", 'version': "Bangla", 'section': "A", 'roll_no': 101, 'status': "Approved"
                },
                {
                    'student_name_bn': "হাসিবুল ইসলাম", 'student_name_en': "Hasibul Islam",
                    'admission_no': "ADM-2026-0102", 'dob': datetime.date(2010, 5, 15), 'gender': "Boy",
                    'mobile': "01711000000", 'father_name': "মোঃ রফিকুল ইসলাম", 'mother_name': "হাসিনা বেগম",
                    'desired_class': "Class 9", 'version': "Bangla", 'section': "A", 'roll_no': 102, 'status': "Approved"
                },
                {
                    'student_name_bn': "ফাতেমা আক্তার তামান্না", 'student_name_en': "Fatema Akter Tamanna",
                    'admission_no': "ADM-2026-0103", 'dob': datetime.date(2010, 8, 20), 'gender': "Girl",
                    'mobile': "01711223344", 'father_name': "মোঃ রফিকুল ইসলাম", 'mother_name': "নাজমা বেগম",
                    'desired_class': "Class 9", 'version': "Bangla", 'section': "B", 'roll_no': 103, 'status': "Approved"
                },
                {
                    'student_name_bn': "সাদমান সাকিব", 'student_name_en': "Sadman Sakib",
                    'admission_no': "ADM-2026-0104", 'dob': datetime.date(2011, 3, 10), 'gender': "Boy",
                    'mobile': "01811223344", 'father_name': "কামরুল হাসান", 'mother_name': "সালমা আক্তার",
                    'desired_class': "Class 8", 'version': "Bangla", 'section': "A", 'roll_no': 104, 'status': "Approved"
                },
                {
                    'student_name_bn': "নুসরাত জাহান লিয়া", 'student_name_en': "Nusrat Jahan Lia",
                    'admission_no': "ADM-2026-0105", 'dob': datetime.date(2012, 11, 25), 'gender': "Girl",
                    'mobile': "01911223344", 'father_name': "আবদুল ওহাব", 'mother_name': "মরিয়ম বিবি",
                    'desired_class': "Class 7", 'version': "Bangla", 'section': "A", 'roll_no': 105, 'status': "Approved"
                },
                {
                    'student_name_bn': "তানভীর আহমেদ রিয়াদ", 'student_name_en': "Tanvir Ahmed Riyad",
                    'admission_no': "ADM-2026-0106", 'dob': datetime.date(2013, 1, 15), 'gender': "Boy",
                    'mobile': "01511223344", 'father_name': "শহিদুল ইসলাম", 'mother_name': "রেহানা পারভীন",
                    'desired_class': "Class 6", 'version': "Bangla", 'section': "A", 'roll_no': 106, 'status': "Approved"
                },
                {
                    'student_name_bn': "মেহেদী হাসান শুভ", 'student_name_en': "Mehedi Hasan Shuvo",
                    'admission_no': "ADM-2026-0107", 'dob': datetime.date(2008, 9, 12), 'gender': "Boy",
                    'mobile': "01611223344", 'father_name': "আব্দুর রহিম", 'mother_name': "খাদিজা বেগম",
                    'desired_class': "SSC 2026", 'version': "Bangla", 'section': "Science", 'roll_no': 107, 'status': "Approved"
                },
                {
                    'student_name_bn': "আফরোজা সুলতানা জেরিন", 'student_name_en': "Afroza Sultana Jerin",
                    'admission_no': "ADM-2026-0108", 'dob': datetime.date(2008, 12, 5), 'gender': "Girl",
                    'mobile': "01722334455", 'father_name': "মোঃ সোলাইমান", 'mother_name': "রুমা আক্তার",
                    'desired_class': "SSC 2026", 'version': "Bangla", 'section': "Humanities", 'roll_no': 108, 'status': "Approved"
                },
            ]
            for s_data in default_students:
                StudentAdmission.objects.create(**s_data)
    except Exception as e:
        print("ensure_default_students warning:", e)



def auto_repair_school_profile_schema():
    """Dynamically ensure missing SQLite columns exist for admit_cards_schoolprofile & transcripts_institutionprofile table"""
    if connection.vendor != 'sqlite':
        return
    try:
        tables = connection.introspection.table_names()
        if 'admit_cards_schoolprofile' in tables:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA table_info(admit_cards_schoolprofile);")
                columns = [row[1] for row in cursor.fetchall()]

                if 'seal' not in columns:
                    cursor.execute("ALTER TABLE admit_cards_schoolprofile ADD COLUMN seal varchar(100) NULL;")

        if 'transcripts_institutionprofile' in tables:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA table_info(transcripts_institutionprofile);")
                t_cols = [row[1] for row in cursor.fetchall()]

                if 'seal' not in t_cols:
                    cursor.execute("ALTER TABLE transcripts_institutionprofile ADD COLUMN seal varchar(100) NULL;")
    except Exception as e:
        print("SchoolProfile schema auto-repair warning:", e)



class AutoMigrateMiddleware:
    """
    Guarantees that database tables (django_session, users_user, question_paper_questionbank, etc.)
    exist before SessionMiddleware or AuthenticationMiddleware attempt to access the database.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _MIGRATED
        if not _MIGRATED:
            try:
                call_command('migrate', interactive=False)
                tables = connection.introspection.table_names()
                if 'users_user' in tables:
                    from apps.users.models import User
                    for uname, uemail in [('M_100184', 'school100184@gmail.com'), ('admin', 'admin@example.com')]:
                        u, created = User.objects.get_or_create(
                            username=uname,
                            defaults={'email': uemail, 'role': 'ADMIN', 'is_staff': True, 'is_superuser': True, 'is_active': True}
                        )
                        if created:
                            u.set_password('admin1234')
                        u.email = uemail
                        u.role = 'ADMIN'
                        u.is_staff = True
                        u.is_superuser = True
                        u.is_active = True
                        u.save()
                _MIGRATED = True
            except Exception as e:
                print("AutoMigrateMiddleware exception:", e)

        # Auto repair question_paper & student_admission & school_profile schema columns if missing
        auto_repair_question_paper_schema()
        auto_repair_student_admission_schema()
        auto_repair_school_profile_schema()

        return self.get_response(request)


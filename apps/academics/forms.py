from django import forms
from .models import QuestionBank, BanglaQuestion, EnglishQuestion, MathQuestion, ScienceQuestion

# বেস ফর্ম
class BaseQuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionBank
        fields = ['question_type', 'class_level', 'marks']
        widgets = {
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'class_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# বাংলা
class BanglaQuestionForm(forms.ModelForm):
    class Meta:
        model = BanglaQuestion
        fields = ['section', 'passage', 'question_text']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'passage': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# ইংরেজি
class EnglishQuestionForm(forms.ModelForm):
    class Meta:
        model = EnglishQuestion
        fields = ['section', 'passage', 'question_text']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'passage': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

# গণিত
class MathQuestionForm(forms.ModelForm):
    class Meta:
        model = MathQuestion
        fields = ['chapter_type', 'latex_formula', 'has_diagram', 'diagram_image']
        widgets = {
            'chapter_type': forms.Select(attrs={'class': 'form-select'}),
            'latex_formula': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'যেমন: E = mc^2'}),
            'has_diagram': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diagram_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# বিজ্ঞান
class ScienceQuestionForm(forms.ModelForm):
    class Meta:
        model = ScienceQuestion
        fields = ['branch', 'stem_text', 'image', 'question_text']
        widgets = {
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'stem_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

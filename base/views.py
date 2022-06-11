from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import  ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy
# Create your views here.
def home(request):
    return render(request , 'home.html')
def about(request):
    return render(request , 'about.html')

# CRUD for finding questions
class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering= ['-date_created']

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context
class QuestionDetailView(DetailView):
    model = Question
    fields = ['title' , 'content']
    context_object_name = 'question'

    def form_valid(self , form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuestionCreateView(LoginRequiredMixin , CreateView):
    model = Question
    fields = ['title' , 'content']
    context_object_name = 'question'

    def form_valid(self , form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class QuestionUpdateView(UserPassesTestMixin , LoginRequiredMixin , UpdateView):
    model = Question
    fields = ['title' , 'content']

    def form_valid(self , form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False
class QuestionDeleteView(UserPassesTestMixin , LoginRequiredMixin , DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = '/'
    template_name = 'base/question_delete.html'
    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False

class CommentDetailView(CreateView):
    model = Comment
    form_class: CommentForm
    template_name = 'base/details.html'

    def form_valid(self , form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('question-detail')

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm

    template_name = 'base/question_answer.html'
    def form_valid(self , form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('question-list')

def like(request , pk):
    post = get_object_or_404(Question , id=request.POST.get('question_id'))
    liked = False

    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        liked = False
    else:
        post.like.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('question-detail' , args=[str(pk)]))

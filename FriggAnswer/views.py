#/usr/bin/python
# coding: utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from .forms import FriggForm, UploadForm
from .models import answer, answer_file
from messages import intro_message

def question_view(request):
    ans = intro_message()
    if request.method == 'POST':
        form = FriggForm(request.POST)
        if form.is_valid():
    	    quest = request.POST['question']
	    ans = answer(quest)
	    context={"form": form, "subtest": ans}
	    return render(request, "FriggTemplates/index.html", context)
	    return HttpResponse("/FriggResponse/")
    #acontece de qualquer forma...
    form = FriggForm()
    context={"form": form, "intro": ans}
    return render_to_response("FriggTemplates/index.html", context ,RequestContext(request), RequestContext(request))

def upload_view(request):
    ans = "Pode carregar o arquivo"
    if request.method == 'POST':
        up_form = UploadForm(request.POST, request.FILES)
        ques_form = FriggForm(request.POST)
        if up_form.is_valid() and ques_form.is_valid:
    	    text = request.FILES['file']
            ques = request.POST['question']
	    ans = answer_file(ques, text)
	    context={"up_form": up_form, "question_form":ques_form, "subtest": ans}
	    return render(request, "FriggTemplates/upload.html", context)
	    return HttpResponse("/FriggResponse/")
    #acontece de qualquer forma...
    up_form = UploadForm()
    ques = FriggForm()
    context={"up_form": up_form, "question_form":ques, "subtest": ans}
    return render_to_response("FriggTemplates/upload.html", context ,RequestContext(request), RequestContext(request))
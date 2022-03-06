from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib import messages 


from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", min_length=2, max_length=20)
    text = forms.CharField(widget=forms.Textarea(), min_length=1)
    

def index(request):
    # if a request came through the search form
    if request.method=="POST":
        title=request.POST['q']
        # if the page exists, redirect to that page
        if util.get_entry(title):
            #return HttpResponseRedirect("/wiki/" + title)
            return HttpResponseRedirect(reverse("page", kwargs={'title':title}))
        # if the page does not exist, show page matches
        else:
            pages=util.list_entries()
            page_matches=list(filter(lambda x: title.lower() in x.lower(), pages))
            return render(request, "encyclopedia/title_search_results.html", {
                "entries": page_matches,
                "title": title
            })
    # if the request method = "get", show all pages
    else:   
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title): 
    
    # if "wiki/new_page" URL is requested
    if title=="new_page":
        # if the "new_page" requested through NewPageForm, get the data from the form
        if request.method=="POST":
            form=NewPageForm(request.POST)
            if form.is_valid():
                title_new=form.cleaned_data["title"]
                content_new=form.cleaned_data["text"]
                # if page to be created already exists, show error
                if util.get_entry(title_new):
                    return HttpResponse("Error: Type BusinessLogicError: The title already exists")
                # if doesn't exist, save and forward to it
                else:
                    util.save_entry(title_new, content_new)
                    return HttpResponseRedirect(reverse("page", kwargs={'title':title_new}))
        
        # if through the link "Create New Page", show a page with an empty form
        else:
            return render(request, "encyclopedia/title_new.html", {
            "form": NewPageForm()
            })
    elif title=="random_title":
        title_to_show=util.random_title()
        return HttpResponseRedirect(reverse("page", kwargs={'title':title_to_show}))

    # if any other "wiki/url" (than "neww_page") is requested
    else:
        # if the page exists, show the page and its contents
        if util.get_entry(title):
            return render(request, "encyclopedia/title.html", {
                "title": title, 
                #"article": util.get_entry(title)
                "article": util.convert(title)
            })
        # if the page does not exit, show error
        else:
            return render(request, "encyclopedia/error.html", {
                "title": title.capitalize()
            })

def edit(request, title):
    
    # if the edit view was called through the edit form
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title_new=form.cleaned_data["title"]
            content_new=form.cleaned_data["text"]
            # if server validation fails, return Error
            if len(title_new)<=3 or len(content_new)<=2:
                return HttpResponse("Error: Type BusinessLogicError: Cannot save empty fields")
            # otherwise save and forward to the page view
            else:
                util.save_entry(title_new, content_new)
                return HttpResponseRedirect(reverse("page", kwargs={'title':title_new}))
    # if the edit view was called by the link on the Home view
    else:
        prefilled_values = {
            "title": title,
            "text": util.get_entry(title)
        }
        return render(request, "encyclopedia/title_edit.html", {
            "title": title,
            "form": NewPageForm(initial=prefilled_values)
        })
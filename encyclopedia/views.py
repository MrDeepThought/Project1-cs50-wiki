from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from . import util
import os
from random import choice

def index(request):
    if request.method == "POST":
        data = request.POST
        query = data['q']
        entries = util.list_entries()

        content = util.get_entry(query)
        if content is not None:
            markdowner = Markdown()
            html = markdowner.convert(content)
            return render(request, f"encyclopedia/{query}.html", {
            "html": html
            })
        else:
            possible = []
            for entry in entries:
                if query.lower() in entry.lower():
                    possible.append(entry)
            return render(request, "encyclopedia/search.html",{
            "possible": possible,
            "query": query.capitalize()
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
            })

def title(request, title):
    content = util.get_entry(title)
    if content is not None:
        markdowner = Markdown()
        html = markdowner.convert(content)
        return render(request, f"encyclopedia/{title}.html", {
        "html": html
        })
    else:
        message = f"The page \'{title}\' that you are trying to request doesnot exist in the Entries!"
        return render(request, f"encyclopedia/error.html", {
        "message": message
        })

def save_html(title):
    htmlContent = "{% extends 'encyclopedia/layout.html' %}\n{% block title %}\n" + title + "\n{% endblock %}\n{% block nav %}\n<div><a href="+f"'{title}/Edit Page'"+">Edit Page</a></div>\n{% endblock %}\n{% block body %}\n{{html|safe}}\n{% endblock %}\n"

    basePath = os.getcwd()
    absPath = basePath + f"\\encyclopedia\\templates\\encyclopedia\\{title}.html"

    with open(absPath, mode='w') as f:
        f.write(htmlContent)

def edit_page(request,title):
    if request.method == "POST":
        data = request.POST
        content = data["content"]
        util.save_entry(title,content)
        markdowner = Markdown()
        html = markdowner.convert(content)

        return HttpResponseRedirect(reverse("encyclopedia:index") + f"{title}")
    else:
        content = util.get_entry(title)
        return render(request, f"encyclopedia/editpage.html", {
        "title": title,
        "content":content
        })

def new_page(request):
    if request.method == "POST":
        data = request.POST
        title = data["title"]

        result = util.get_entry(title)
        if result is None:
            content = data["content"]
            util.save_entry(title,content)
            save_html(title)

            markdowner = Markdown()
            html = markdowner.convert(content)
            '''return render(request, f"encyclopedia/{title}.html", {
            "html": html
            })'''
            return HttpResponseRedirect(reverse("encyclopedia:index") + f"{title}")
        else:
            message = f"There already exists an Entry with the same name as '{title}'!"
            return render(request, "encyclopedia/error.html",{
            "message": message
            })
    else:
        return render(request, "encyclopedia/newpage.html")

def random_page(request):
    entries = util.list_entries()
    title = choice(entries)
    content = util.get_entry(title)
    markdowner = Markdown()
    html = markdowner.convert(content)
    return render(request, f"encyclopedia/{title}.html", {
    "html": html
    })

from django.http import Http404
from django.shortcuts import render, redirect
from random import randint
from markdown2 import Markdown

from . import util
from . import forms


def index(request):
    entries = util.list_entries()
    entries_urls = dict()
    for entry in entries:
        entries_urls[entry] = util.get_url(entry)
    context = {
        "entries_urls": entries_urls,
    }
    return render(request, "encyclopedia/index.html", context)


def show_entry(request, entry_name):
    current_entry = util.get_entry(entry_name)
    markdowner = Markdown()
    if not current_entry:
        raise Http404('Entry does not exist!')
    context = {
        'entry': markdowner.convert(current_entry),
        'entry_edit_url': util.get_url_for_edit(entry_name),
        'title': entry_name,
    }
    return render(request, "encyclopedia/show_entry.html", context)


def search(request):
    search_q = request.POST["q"]
    if not search_q:
        return render(request, "encyclopedia/search.html")
    search_match = util.get_entry(search_q)
    if search_match:
        return redirect('show_entry', entry_name=search_q)
    entries = util.search_entries_dict(search_q)
    context = {
        "entries": entries
    }
    return render(request, "encyclopedia/search.html", context)


def random_page(request):
    entries = util.list_entries()
    random_entry_index = randint(0, len(entries) - 1)
    random_entry = entries[random_entry_index]
    return redirect('show_entry', entry_name=random_entry)


def create_page(request):
    form = forms.NewEntryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_page_title, new_page_content = form.cleaned_data['title'], form.cleaned_data['content']
            util.save_entry(new_page_title, new_page_content)
            return redirect('show_entry', entry_name=new_page_title)
    context = {
        'form': form,
    }
    return render(request, "encyclopedia/create_page.html", context)


def edit_page(request, entry_name):
    current_entry = util.get_entry(entry_name)
    form = forms.EditEntryForm(request.POST or None,
        initial={'content': current_entry}
    )
    if request.method == 'POST':
        if form.is_valid():
            page_content = form.cleaned_data['content']
            util.save_entry(entry_name, page_content)
            return redirect('show_entry', entry_name=entry_name)
    context = {
        'form': form,
    }
    return render(request, "encyclopedia/edit_page.html", context)
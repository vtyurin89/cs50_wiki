import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def get_url(entry_name):
    """
    Returns url of the entry.
    """
    return reverse('show_entry', kwargs={'entry_name': entry_name})


def get_url_for_edit(entry_name):
    """
    Returns url of the editing page of the entry.
    """
    return reverse('edit_page', kwargs={'entry_name': entry_name})


def search_entries_dict(search_q):
    """
    Returns a dictionary of entries that have the query as a substring.
    With their URLs.
    """
    _, filenames = default_storage.listdir("entries")
    result_dict = dict()
    for filename in filenames:
        formatted_filename = re.sub(r"\.md$", "", filename)
        if filename.endswith(".md") and search_q.lower() in formatted_filename.lower():
            result_dict[formatted_filename] = get_url(formatted_filename)
    return result_dict

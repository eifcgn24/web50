import re, random, markdown2

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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

def get_title(title):
    """
    Retrieves the title name as written in the entry
    """
    try:
        pages=list_entries()
        pattern="^"+title+"$"
        page_match=filter(lambda x: re.match(pattern, x), pages)
        return page_match.group(0)
    except:
        pass

def random_title():
    """
    Retrieves a random title
    """
    pages=list_entries()
    pages_size=len(pages)
    random_no=random.randrange(0,pages_size-1)
    return pages[random_no]

def convert(title):
    return markdown2.markdown(get_entry(title))

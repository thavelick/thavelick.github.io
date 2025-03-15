import markdown

def render_markdown(text):
    """
    Render markdown text using the fenced_code extension.
    """
    return markdown.markdown(text, extensions=['fenced_code'])

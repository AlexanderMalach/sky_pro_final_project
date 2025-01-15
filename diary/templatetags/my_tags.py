from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return f"#"


@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value

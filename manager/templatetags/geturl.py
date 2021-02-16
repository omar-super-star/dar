from django import template

register = template.Library()

@register.simple_tag
def geturl(url=None):
    if url ==None:
        return ""
    else:
        paralist=url.split("&")
        if len(paralist) ==1:
           if paralist[0].split("=")[0] == "page":
               return ""
           else:
               return url
        else:
            return "&".join(paralist[1:])
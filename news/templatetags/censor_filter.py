from django import template

register = template.Library()



@register.filter()
def censor(text):
    if type(text) == str:
        BAD_WORDS = ["Новость", "Статья"]
        for word in BAD_WORDS:
            text = text.replace(word[1::], '*' * len(word))

        return text    
    
    else: 
        print("TypeError")


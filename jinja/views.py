from django.shortcuts import render


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age


cities = [
    {'id': 1, 'name': 'Kyiv', 'info': 'sdfsdf', 'basedYear': '1999'},
    {'id': 2, 'name': 'Dnipro', 'info': 'sdfsdf', 'basedYear': '1999'},
    {'id': 3, 'name': 'Lviv', 'info': 'sdfsdf', 'basedYear': '1999'},
    {'id': 4, 'name': 'Boyarka', 'info': 'sdfsdf', 'basedYear': '1999'},
    {'id': 5, 'name': 'Sevastopil', 'info': 'sdfsdf', 'basedYear': '1999'},
]


def jinja(request):
    person = Person('Dima', 23)
    name = 'Andrii <div></div> '
    age = 24

    context = {
        'name': name,
        'age': age,
        'person': person,
        'cities': cities,
    }
    return render(request, 'jinja/jinja.html',  context=context)

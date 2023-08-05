# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickstruct']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'quickstruct',
    'version': '0.1.2',
    'description': 'A small library to ease the creation, usage, serialization and deserialization of C structs.',
    'long_description': '===========\nQuickStruct\n===========\n\nQuickStruct is a small library written in Python that allows you to\neasily create C structs (and a bit more dynamic stuff) in Python!\n\nIt\'s fairly easy to use::\n\n    from quickstruct import *\n\n    class Person(DataStruct):\n        name: String\n        age: i8\n\nStructs can also be composed::\n\n    class TeachingClass(DataStruct):\n        teacher: Person\n        # we use Array[T] to make it dynamic sized\n        students: Array[Person]\n\n\nAnd structs can also inherit other structs\n(we even support multiple inheritance!)::\n\n    class Employee(Person):\n        salary: i32\n\n\nNow let\'s use the structs we defined::\n\n    # we have 2 options when initializing\n    # 1. by setting each attribute individually\n    person = Person()\n    person.name = "John Doe"\n    person.age = 42\n\n    # or by passing them as keyword arguments\n    person = Person(name="John Doe", age=42)\n\n\nThe main use for C structs is to convert them from bytes and back::\n\n    data = person.to_bytes()\n    # do something with the data\n    \n    # and it\'s also easy to deserialize\n    person = Person.from_bytes(data)\n\n\nWhen deserializing a struct with multiple bases or if one of the fields was overriden, \nthe deserialization must be done through the exact type of the struct.\n',
    'author': 'Binyamin Y Cohen',
    'author_email': 'binyamincohen555@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xpodev/quickstruct',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

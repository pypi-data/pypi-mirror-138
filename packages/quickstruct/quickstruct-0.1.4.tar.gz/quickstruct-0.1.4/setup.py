# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickstruct']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'quickstruct',
    'version': '0.1.4',
    'description': 'A small library to ease the creation, usage, serialization and deserialization of C structs.',
    'long_description': '# QuickStruct\n\nQuickStruct is a small library written in Python that allows you to\neasily create C structs (and a bit more dynamic stuff) in Python!\n\nIt\'s fairly easy to use\n```py\nfrom quickstruct import *\n\nclass Person(DataStruct):\n    name: String\n    age: i8\n```\n\nStructs can also be composed\n\n```py\nclass TeachingClass(DataStruct):\n    teacher: Person\n    # We use Array[T] to make it dynamic sized\n    students: Array[Person]\n```\n\nAnd structs can also inherit other structs\n(we even support multiple inheritance!)\n```py\nclass Employee(Person):\n    salary: i32\n```\n\n\nNow let\'s use the structs we defined\n```py\n# We have 2 options when initializing.\n# Either by setting each attribute individually\nperson = Person()\nperson.name = "John Doe"\nperson.age = 42\n\n# Or by passing them as keyword arguments\nperson = Person(name="John Doe", age=42)\n```\n\n\nThe main use for C structs is to convert them from bytes and back\n```py\ndata = person.to_bytes()\n# Do something with the data\n\n# And it\'s also easy to deserialize\nperson = Person.from_bytes(data)\n```\n\n\nWhen deserializing a struct with multiple bases or if one of the fields was overriden, \nthe deserialization must be done through the exact type of the struct.\n\n\n# Alignment\nIt is also possible to add padding to the struct. There are 2 ways to do that:\n## Manual Alignment\nThis can be done with the `Padding` type.\n```py\nclass AlignedStruct(DataStruct):\n    c1: char\n    # This adds a single byte padding\n    _pad0: Padding\n    short: i16\n    # We can also add multi-byte padding\n    # Here we\'ll pad to get 8 byte alignment (missing 4 bytes)\n    _pad1: Padding[4]\n```\n\n## Automatic Alignment\nThis can done by passing some flags to the class definition. By default the struct is automatically aligned.\n```py\n# Aligned on 2 byte boundary\nclass AlignedStruct(DataStruct, flags = StructFlags.Align2Bytes):\n    c1: char\n    # Padding will be added here\n    short: i16\n```\n\n## Struct Flags\n| Flag              | Description                                                                                                           |\n|-------------------|-----------------------------------------------------------------------------------------------------------------------|\n| NoAlignment       | This is the most packed form of the struct. All fields are adjacent with no padding (unless manually added)           |\n| Packed            | Same as `NoAlignment` except that `NoAlignment` is a bit more optimized because no alignment is done.                 |\n| Align1Byte        | Same as `Packed`                                                                                                      |\n| Align2Bytes       | Aligns the fields on 2 byte boundary.                                                                                 |\n| Align4Bytes       | Aligns the fields on 4 byte boundary.                                                                                 |\n| Align8Bytes       | Aligns the fields on 8 byte boundary.                                                                                 |\n| AlignAuto         | Aligns the fields by their type.                                                                                      |\n| ReorderFields     | Specifies the fields should be reordered in order to make the struct a little more compressed.                        |\n| ForceDataOnly     | Specifies that the struct may only contain serializable fields. Data-only structs may only inherit data-only structs. |\n| AllowOverride     | If set, fields defined in the struct may override fields that are defined in the base struct.                         |\n| ForceSafeOverride | If set, when fields are overridden, they must have the same type (which would make it pretty useless to override).    |\n| ForceFixedSize    | If set, the struct must have a fixed size. If not, an exception is raised.                                            |\n| AllowInline       | If set, the struct\'s fields will be inlined into another struct the contains this struct.                             |\n| Final             | Marks the structure so it won\'t be inheritable by any other class.                                                    |\n| LockedStructure   | If set, denies any overrides of that structure. This flag is not yet implemented.                                     |\n\n\n',
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

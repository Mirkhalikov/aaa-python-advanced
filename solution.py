import json
import keyword


class ColorizeMixin:
    """Colorize mixin for Advert class."""

    repr_color_code = 33

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        original_str = cls.__str__
        cls.repr_color_code = ColorizeMixin.repr_color_code

        def colorized_str(self):
            return f'\033[{self.repr_color_code}m{original_str(self)}\033[0m'

        cls.__str__ = colorized_str

    def __str__(self):
        return f'{self.title} | {self.price} ₽'


class JSONToObject:
    """Class that converts JSON-objects into python-objects
      with access to the attributes using dot notation.
    """

    def __init__(self, mapping=None):
        if mapping is not None:
            for key, value in mapping.items():
                setattr(self, key, value)

    def __getattr__(self, item):
        """Modified __getattr__ method"""
        return self.__dict__.get(item)

    def __setattr__(self, key, value):
        """Modified __setattr__ method that allows to use dot
        notation on any level of nesting."""
        if isinstance(value, dict):
            self.__dict__[self._sanitize_attribute_name(
                key)] = JSONToObject(value)
        else:
            self.__dict__[self._sanitize_attribute_name(key)] = value

    def _sanitize_attribute_name(self, name: str) -> str:
        """Method that checks if the attribute name is a keyword.
        If so, it adds an underscore to the end of the name."""
        if keyword.iskeyword(name):
            return name + '_'
        return name


class Advert(ColorizeMixin):
    """Advert class"""

    repr_color_code = 32

    def __init__(self, mapping: str):
        jsonToObj = JSONToObject(mapping)

        for key, value in jsonToObj.__dict__.items():
            setattr(self, key, value)

        if 'price' not in self.__dict__:
            self.price = 0

    def __setattr__(self, key: str, value: any):
        """Modified __setattr__ method that checks
        the value of the price attribute."""
        if key == 'price' and value < 0:
            raise ValueError('price must be >= 0')
        self.__dict__[key] = value


if __name__ == '__main__':
    print('//------------------------PART 1------------------------//\n')
    lesson_str = '''
    {
        "title": "python",
        "price": 0,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
        }
    }
    '''
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad.location.address)

    dog_str = '''
    {
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs"
    }
    '''
    dog = json.loads(dog_str)
    dog_ad = Advert(dog)

    print(dog_ad.class_)

    lesson_str = '{"title": "python", "price": -1}'
    lesson = json.loads(lesson_str)
    try:
        lesson_ad = Advert(lesson)
    except ValueError as e:
        print(e)

    lesson_str = '{"title": "python", "price": 1}'
    lesson = json.loads(lesson_str)
    try:
        lesson_ad = Advert(lesson)
        lesson_ad.price = -3
    except ValueError as e:
        print(e)
    lesson_str = '{"title": "python"}'
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad.price)

    print('\n//------------------------PART 2------------------------//\n')

    json_str = """{
    "title": "Вельш-корги",
    "price": 1000,
    "class": "dogs"
    }"""
    advert = Advert(json.loads(json_str))

    print(advert)  # Вывод с цветовым оформлением
    print(advert.class_)  # Доступ к атрибуту, являющемуся ключевым словом

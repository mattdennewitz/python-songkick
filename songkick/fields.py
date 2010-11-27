from datetime import date
from decimal import Decimal
from time import strptime

from dateutil.parser import parse as dateutil_parse

from songkick.base import BaseField


class Field(BaseField):

    def to_python(self, value):
        return value


class StringField(BaseField):

    def to_python(self, value):
        if not isinstance(value, basestring):
            value = str(value)
        return value.encode('utf-8')


class BooleanField(Field):

    def to_python(self, value):
        return bool(value)


class IntField(Field):

    def to_python(self, value):
        if not isinstance(value, int):
            value = int(value)
        return value

class DecimalField(Field):

    def to_python(self, value):
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        return value


class DateField(Field):

    def to_python(self, value):
        return date(*strptime(value, '%Y-%m-%d')[:3])


class DateTimeField(Field):

    def to_python(self, value):
        return dateutil_parse(value)


class TimeField(Field):

    def to_python(self, value):
        return strptime(value, '%H:%M:%S')


class ObjectField(Field):

    def __init__(self, object_class, **kwargs):
        self.cls = object_class
        super(ObjectField, self).__init__(**kwargs)

    def to_python(self, value):
        return self.cls._from_json(value)


class ListField(Field):

    def __init__(self, field=None, **kwargs):
        self.field = field
        kwargs['default'] = []
        super(ListField, self).__init__(**kwargs)

    def to_python(self, value):
        if self.field is not None:
            return [self.field.to_python(v) for v in value]
        return value


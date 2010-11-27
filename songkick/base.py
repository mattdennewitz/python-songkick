class SongkickModelOptions(object):
    fields = None

    def __new__(cls, meta=None):
        overrides = {}
        if meta is not None:
            for key, value in meta.iteritems():
                if key.startswith('_'):
                    continue
                overrides[key] = value
        return object.__new__(type('SongkickModelOptions', 
                                   (cls, ),
                                   overrides))


class SongkickModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        
        new_cls = super(SongkickModelMetaclass, cls).__new__(cls, name, 
                                                             bases, attrs)
        if '__metaclass__' in attrs:
            return new_cls

        opts = getattr(new_cls, 'Meta', None)
        new_cls._meta = SongkickModelOptions(opts)

        fields = {}

        for key, value in attrs.iteritems():
            if isinstance(value, BaseField):
                value.field_name = key
                if value.mapping is None:
                    value.mapping = key
                fields[key] = value

        new_cls._fields = fields

        return new_cls


class SongkickModel(object):
    __metaclass__ = SongkickModelMetaclass    

    def __init__(self, **values):
        self._data = {}

        for field_name in self._fields.keys():
            try:
                setattr(self, field_name, values.pop(field_name))
            except AttributeError:
                pass

    @classmethod
    def _from_json(cls, data):
        """Build an instance of ``cls`` using ``data``.
        """

        values = {}

        for field_name, field in cls._fields.items():

            # start with nothing
            value = None

            if '__' in field.mapping:
                bits = field.mapping.split('__')
                first_bit = bits.pop(0)
                value = data[first_bit]

                while bits:
                    bit = bits.pop(0)
                    value = value.get(bit)
            else:
                value = data.get(field.mapping)

            if value is not None:
                value = field.to_python(value)

            # finally, set the value
            values[field_name] = value

        return cls(**values)


class BaseField(object):

    def __init__(self, field_name=None, mapping=None, default=None):
        """Set up a Songkick field responsible for storing
        and translating JSON data into something useful.
        """

        self.field_name = field_name
        self.mapping = mapping or field_name
        self.default = default

    def __get__(self, instance, owner):
        value = instance._data.get(self.field_name)
        if value is None:
            # try a default
            return self.default
        return value

    def __set__(self, instance, value):
        instance._data[self.field_name] = value

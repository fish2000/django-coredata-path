
import base64
import biplist
from django.db import models

class BinaryPropertyList(models.TextField):
    
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        if value == "":
            return None
        try:
            if isinstance(value, basestring):
                return biplist.readPlistFromString(
                    base64.decodestring(value))
            return value
        except (ValueError, biplist.InvalidPlistException):
            pass
        return value
    
    def get_internal_type(self):
        return "TextField"
    
    def get_prep_value(self, value):
        if value:
            try:
                biplist.readPlistFromString(value)
            except biplist.InvalidPlistException:
                return biplist.writePlistToString(
                    value, binary=True)
            else:
                return value
        return value
    
    def get_db_prep_value(self, value, connection=None, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        if value:
            return base64.encodestring(value)
        return value
    
    def value_to_string(self, obj):
        return self.get_db_prep_value(
            self._get_val_from_obj(obj))
    
    def south_field_triple(self):
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return ('jangypath.fields.BinaryPropertyList', args, kwargs)


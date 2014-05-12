
import codecs
from django.utils import simplejson
from django.utils.encoding import DjangoUnicodeDecodeError
#from django.utils.encoding import smart_unicode
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers.json import Serializer as JSONSerializer
#from django.core.serializers.json import Deserializer

class Serializer(JSONSerializer):
    def handle_field(self, obj, field):
        try:
            super(Serializer, self).handle_field(obj, field)
        except DjangoUnicodeDecodeError:
            if hasattr(self, '_current'):
                self._current[field.name] = unicode(
                    str(field._get_val_from_obj(obj)),
                    encoding='utf-8',
                    errors='ignore')
            else:
                raise DjangoUnicodeDecodeError("FATAL ERROR: Serializer subclass has no _current dict.")
    
    def end_serialization(self):
        stream = codecs.getwriter('utf-8')(self.stream)
        simplejson.dump(
            self.objects, stream,
            cls=DjangoJSONEncoder,
            ensure_ascii=False,
            **self.options)

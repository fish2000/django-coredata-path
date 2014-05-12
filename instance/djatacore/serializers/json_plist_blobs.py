
from __future__ import print_function

import sys
import codecs
import base64
from django.utils import simplejson as json
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import smart_unicode
from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.json import DjangoJSONEncoder

class Serializer(JSONSerializer):
    
    _plist_fields = set()
    
    def __handle_it__(self, name, value):
        if hasattr(self, '_current'):
            self._current[name] = value
        else:
            raise DjangoUnicodeDecodeError(
                "FATAL ERROR: Serializer subclass has no _current dict.")
    
    def handle_field(self, obj, field):
        try:
            super(Serializer, self).handle_field(obj, field)
        
        except (DjangoUnicodeDecodeError, UnicodeDecodeError):
            raw_value = field._get_val_from_obj(obj)
            test_value = str(unicode(raw_value[:8],
                encoding='utf-8',
                errors='ignore'))
            
            # I am well aware that this is a circuitously
            # dumb way to check for a biplist-y blob.
            if test_value.lower().startswith('bplist'):
                self._plist_fields.add(str(field.name))
                self.__handle_it__(field.name,
                    base64.encodestring(raw_value))
            
            else:
                self.__handle_it__(field.name,
                    smart_unicode(raw_value,
                        encoding='utf-8',
                        strings_only=False,
                        errors='strict'))
    
    def end_serialization(self):
        print('Fields containing binary plists:',
            file=sys.stderr)
        for field in self._plist_fields:
            print(field, file=sys.stderr)
        print('', file=sys.stderr)
        
        stream = codecs.getwriter('utf-8')(self.stream)
        json.dump(self.objects, stream,
            cls=DjangoJSONEncoder,
            ensure_ascii=False,
            **self.options)






from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
import jangypath.models as dp

for model_class in dp.coredata_models:
    try:
        admin.site.register(model_class, model_class.admin())
    except AlreadyRegistered:
        print "WARNING: can't re-register model class %s" % str(model_class.__name__)
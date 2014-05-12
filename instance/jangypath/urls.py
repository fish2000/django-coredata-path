
from django.conf.urls.defaults import patterns, url, include

app_patterns = patterns('',

    url(r'^post/(?P<post_id>[\w\-]+)/?$',
        'jangypath.views.forkingpath',
        name="post"),

)

# URL namespace
urlpatterns = patterns('',

    url(r'', include(app_patterns,
        namespace='jangypath', app_name='jangypath')),

)




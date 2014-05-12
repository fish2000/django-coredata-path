#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
twemoir/views.py

Created by FI$H 2000 on 2011-08-02.
Copyright (c) 2011 Objects In Space And Time, LLC. All rights reserved.

"""
import watson
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from watson.models import SearchEntry
from jangypath.models import Post

def forkingpath(request, post_id=None):
    """ Display the Path.app post """
    if post_id is None:
        raise ObjectDoesNotExist('Choose a Path.app post to view')
    
    try:
        int(post_id)
    except ValueError:
        post = Post.objects.get(zid__iexact=post_id)
    else:
        post = Post.objects.get(pk=int(post_id))
    
    mt = loader.get_template('jangypath/forkingpath.html')
    return HttpResponse(
        mt.render(
            RequestContext(
                request, {
                    'post': post,
                }
            )))



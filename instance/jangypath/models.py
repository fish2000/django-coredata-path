# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

#from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.contrib.admin import ModelAdmin
from appconf import AppConf
from watson.registration import SearchAdapter
from jangypath.fields import BinaryPropertyList
from jangypath.utils import display

coredata_models = set()

class MaximumOverdrive(AppConf):
    """ This django-appconf config class overrides system defaults.
        Specifying a zero-length prefix string tricks the AppConf object
        into polluting the settings module's namespace (!) """
    
    class Meta:
        prefix = ""
    
    SERIALIZATION_MODULES = {
        'json-unicode': 'serializers.json_unicode',
        'json-plist-blobs': 'serializers.json_plist_blobs', }


class CoreDataSearchAdapter(SearchAdapter):
    """ The base class for the reflectively-generated CoreData adapter classes
        we hand off to the Watson search engine (see below). """
    def get_title(self, obj):
        return unicode(obj.title)
    def get_description(self, obj):
        return unicode(obj.description)
    def get_url(self, obj):
        return unicode(obj.url)

class CoreDataModelAdmin(ModelAdmin):
    """ The base class for generated Django admin-page config classes --
        furnished in the same fashion as the Watson adapters, and
        registered en masse with the Django admin (q.v jangypath/admin.py). """
    @display(desc="Description")
    def get_description(self, obj):
        return obj.description

class CoreDatum(models.Model):
    """ Abstract base model foundation, upon which all CoreData schema entities,
        metadata, and related thingees are built. """
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return "%s(%s)" % (
            getattr(self, 'zid', ''),
            getattr(self, 'z_pk', self.pk))
    
    def __unicode__(self):
        return unicode(str(self))
    
    def __repr__(self):
        return "<%s: %s>" % (
            self.__class__.__name__,
            str(self))
    """
    @property
    def id(self):
        return self.pk
    """
    @property
    def title(self):
        return unicode(self)
    
    @property
    def description(self):
        return getattr(self, 'zsummary', '')
    
    @property
    def url(self):
        return getattr(self, 'zurl', '')
    
    @classmethod
    def adapter(cls, fields=(), exclude=(), store=()):
        """ Implementation hook for Watson search adapter generation. """
        if hasattr(cls, 'fields'):
            fields += tuple([field.name for field in cls._meta.fields \
                if isinstance(field, (models.CharField, models.TextField))])
            fields += getattr(cls, 'fields')
        if hasattr(cls, 'exclude'):
            exclude += getattr(cls, 'exclude')
        if hasattr(cls, 'store'):
            store += getattr(cls, 'store')
        return type("%sSearchAdapter" % cls.__name__, (CoreDataSearchAdapter,), dict(
            fields=fields, exclude=exclude, store=store))
    
    @classmethod
    def admin(cls, fields=(), exclude=(), list_display=()):
        """ Implementation hook for Django admin config class generation. """
        list_display = ('id','title','get_description','url')
        if hasattr(cls, 'list_display'):
            list_display = getattr(cls, 'list_display')
        else:
            list_display = ('id','title','get_description','url')
        if hasattr(cls, 'fields'):
            fields += tuple([field.name for field in cls._meta.fields \
                if isinstance(field, (models.CharField, models.TextField))])
            #fields += getattr(cls, 'fields')
        if hasattr(cls, 'exclude'):
            exclude += getattr(cls, 'exclude')
        return type("%sAdmin" % cls.__name__, (CoreDataModelAdmin,), dict(
            fields=fields, exclude=exclude,
            list_display=list_display,
            list_display_links=('id',)))


class CoreMetaDatum(models.Model):
    """ Base model for CoreData metadata definitions.
        N.B. I hate the syntactic redundance in the phrase "CoreData metadata".
        The circumlocutiously inclined should send pull requests with suggestions
        for less insipid-sounding anologues. """
    class Meta:
        abstract = True


class PathCoreDatum(CoreDatum):
    """ Base model for the Django representation of the actual Core Data content
        from a single Path app instance. """
    
    class __metaclass__(ModelBase):
        """ An embedded metaclass for building a registry
            of all CoreData ORM-mapped classes. """
        def __new__(cls, name, bases, attrs):
            global coredata_models
            model = ModelBase.__new__(cls, name, bases, attrs)
            if model._meta.abstract is False:
                coredata_models.add(model)
            return model
    
    class Meta:
        abstract = True
        ordering = ['z_opt', 'z_ent', 'z_pk']
    
    z_pk = models.IntegerField(
        primary_key=True,
        default=0,
        db_column=u'Z_PK')
    
    z_ent = models.PositiveIntegerField(
        db_column=u'Z_ENT',
        default=0,
        null=True,
        blank=True)
    
    z_opt = models.PositiveIntegerField(
        db_column=u'Z_OPT',
        default=0,
        null=True,
        blank=True)


class PathCoreMetaDatum(CoreMetaDatum):
    """ Base model for Path-centric metadata defs """
    class Meta:
        abstract = True


class Activity(PathCoreDatum):
    
    zheight = models.IntegerField(
        null=True,
        db_column=u'ZHEIGHT',
        blank=True)
    
    zisfriendactivity = models.IntegerField(
        null=True,
        db_column=u'ZISFRIENDACTIVITY',
        blank=True)
    
    zisread = models.IntegerField(
        null=True,
        db_column=u'ZISREAD',
        blank=True)
    
    zphotoheight = models.IntegerField(
        null=True,
        db_column=u'ZPHOTOHEIGHT',
        blank=True)
    
    zphotowidth = models.IntegerField(
        null=True,
        db_column=u'ZPHOTOWIDTH',
        blank=True)
    
    zbook = models.ForeignKey('jangypath.Book',
        db_column=u'ZBOOK',
        related_name='activities',
        null=True,
        blank=True)
    
    zlocation = models.ForeignKey('jangypath.Location',
        db_column=u'ZLOCATION',
        related_name='activities',
        null=True,
        blank=True)
    
    zmovie = models.ForeignKey('jangypath.Movie',
        db_column=u'ZMOVIE',
        related_name='activities',
        null=True,
        blank=True)
    
    zmusic = models.ForeignKey('jangypath.Music',
        db_column=u'ZMUSIC',
        related_name='activities',
        null=True,
        blank=True)
    
    zperson = models.ForeignKey('jangypath.Person',
        db_column=u'ZPERSON',
        related_name='activities',
        null=True,
        blank=True)
    
    zrecipient = models.ForeignKey('jangypath.Person',
        db_column=u'ZRECIPIENT',
        related_name='received_activities',
        null=True,
        blank=True)
    
    zsuggestor = models.ForeignKey('jangypath.Person',
        db_column=u'ZSUGGESTOR',
        related_name='suggested_activities',
        null=True,
        blank=True)
    
    zdate = models.TextField(
        db_column=u'ZDATE',
        blank=True,
        null=True)
    
    zactivitycallout = models.TextField(
        db_column=u'ZACTIVITYCALLOUT',
        blank=True)
    
    zactivitydescription = models.TextField(
        db_column=u'ZACTIVITYDESCRIPTION',
        blank=True,
        null=True)
    
    zbutton1title = models.TextField(
        db_column=u'ZBUTTON1TITLE',
        blank=True,
        null=True)
    
    zbutton1url = models.TextField(
        db_column=u'ZBUTTON1URL',
        blank=True,
        null=True)
    
    zbutton2title = models.TextField(
        db_column=u'ZBUTTON2TITLE',
        blank=True,
        null=True)
    
    zbutton2url = models.TextField(
        db_column=u'ZBUTTON2URL',
        blank=True,
        null=True)
    
    zemotion = models.TextField(
        db_column=u'ZEMOTION',
        blank=True,
        null=True)
    
    ziconurl = models.TextField(
        db_column=u'ZICONURL',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zmomentsubtypestring = models.TextField(
        db_column=u'ZMOMENTSUBTYPESTRING',
        blank=True,
        null=True)
    
    zmomenttypestring = models.TextField(
        db_column=u'ZMOMENTTYPESTRING',
        blank=True,
        null=True)
    
    zphotourl = models.TextField(
        db_column=u'ZPHOTOURL',
        blank=True,
        null=True)
    
    ztitle = models.TextField(
        db_column=u'ZTITLE',
        blank=True)
    
    ztype = models.TextField(
        db_column=u'ZTYPE',
        blank=True)
    
    zurl = models.TextField(
        db_column=u'ZURL',
        blank=True)
    
    @property
    def person(self):
        return self.zperson.name
    
    @property
    def recipient(self):
        return self.zrecipient.name
    
    @property
    def title(self):
        return getattr(self, 'ztype', '')
    
    @property
    def description(self):
        return getattr(self, 'ztitle', '')
    
    @display(desc="Person")
    def get_person(self):
        return """<nobr>%s</nobr>""" % self.person
    
    @display(desc="Recipient")
    def get_recipient(self):
        return """<nobr>%s</nobr>""" % self.recipient
    
    fields = ('person', 'recipient')
    list_display = ('id', 'title', 'get_person', 'get_description', 'get_recipient', 'url')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZACTIVITY'

class ApiApplication(PathCoreDatum):
    
    zpathdotcolor = models.IntegerField(
        null=True,
        db_column=u'ZPATHDOTCOLOR',
        blank=True)
    
    zappstoreurl = models.TextField(
        db_column=u'ZAPPSTOREURL',
        blank=True)
    
    zclientid = models.TextField(
        db_column=u'ZCLIENTID',
        blank=True)
    
    zconnectdescription = models.TextField(
        db_column=u'ZCONNECTDESCRIPTION',
        blank=True)
    
    zconnecticonurl = models.TextField(
        db_column=u'ZCONNECTICONURL',
        blank=True)
    
    zfeediconurl = models.TextField(
        db_column=u'ZFEEDICONURL',
        blank=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zname = models.TextField(
        db_column=u'ZNAME',
        blank=True)
    
    @property
    def title(self):
        return getattr(self, 'zname', '')
    
    @property
    def description(self):
        return getattr(self, 'zconnectdescription', '')
    
    @property
    def url(self):
        return getattr(self, 'zconnecticonurl', '')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZAPIAPPLICATION'

class Book(PathCoreDatum):
    
    zindex = models.IntegerField(
        null=True,
        db_column=u'ZINDEX',
        blank=True)
    
    zyear = models.IntegerField(
        null=True,
        db_column=u'ZYEAR',
        blank=True)
    
    zauthor = models.TextField(
        db_column=u'ZAUTHOR',
        blank=True)
    
    zauthorid = models.TextField(
        db_column=u'ZAUTHORID',
        blank=True)
    
    zbookdescription = models.TextField(
        db_column=u'ZBOOKDESCRIPTION',
        blank=True)
    
    zgenre = models.TextField(
        db_column=u'ZGENRE',
        blank=True)
    
    zitunesurl = models.TextField(
        db_column=u'ZITUNESURL',
        blank=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zphotourl = models.TextField(
        db_column=u'ZPHOTOURL',
        blank=True)
    
    ztitle = models.TextField(
        db_column=u'ZTITLE',
        blank=True)
    
    @property
    def title(self):
        return getattr(self, 'ztitle', '')
    
    @property
    def description(self):
        return getattr(self, 'zbookdescription', '')
    
    @property
    def url(self):
        return getattr(self, 'zphotourl', '')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZBOOK'

class Comment(PathCoreDatum):
    
    zidiscustom = models.IntegerField(
        null=True,
        db_column=u'ZIDISCUSTOM',
        blank=True)
    
    zissynthesizedauthorcomment = models.IntegerField(
        db_column=u'ZISSYNTHESIZEDAUTHORCOMMENT',
        null=True,
        blank=True)
    
    zcreator = models.ForeignKey('jangypath.Person',
        db_column=u'ZCREATOR',
        related_name='comments',
        null=True,
        blank=True)
    
    zlocation = models.ForeignKey('jangypath.Location',
        db_column=u'ZLOCATION',
        related_name='comments_at',
        null=True,
        blank=True)
    
    zpost = models.ForeignKey('jangypath.Post',
        db_column=u'ZPOST',
        related_name='comments',
        null=True,
        blank=True)
    
    zdate = models.TextField(
        db_column=u'ZDATE',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    ztext = models.TextField(
        db_column=u'ZTEXT',
        blank=True,
        null=True)
    
    zlinkdata = BinaryPropertyList(
        db_column=u'ZLINKDATA',
        blank=True,
        null=True)
    
    @property
    def title(self):
        return "%s > '%s'" % (
            self.zcreator.name,
            self.zpost.title)
    
    @property
    def description(self):
        return getattr(self, 'ztext', '')
    
    @property
    def url(self):
        return getattr(self, 'zconnecticonurl', '')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZCOMMENT'

class CommentDraft(PathCoreDatum):
    
    zpost = models.ForeignKey('jangypath.Post',
        db_column=u'ZPOST',
        null=True,
        blank=True)
    
    ztext = models.TextField(
        db_column=u'ZTEXT',
        blank=True)
    
    @property
    def title(self):
        return "%s > '%s'" % (
            self.zpost.zcreator.name,
            self.zpost.title)
    
    @property
    def description(self):
        return getattr(self, 'ztext', '')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZCOMMENTDRAFT'

class Emotion(PathCoreDatum):
    
    zisnudge = models.IntegerField(
        null=True,
        db_column=u'ZISNUDGE',
        blank=True)
    
    zcreator = models.ForeignKey('jangypath.Person',
        db_column=u'ZCREATOR',
        related_name='emotions',
        null=True,
        blank=True)
    
    zpost = models.ForeignKey('jangypath.Post',
        db_column=u'ZPOST',
        null=True,
        blank=True)
    
    zcreated = models.TextField(
        db_column=u'ZCREATED',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    ztype = models.TextField(
        db_column=u'ZTYPE',
        blank=True,
        null=True)
    
    @property
    def title(self):
        return "%s : %s" % (
            self.zpost and self.zpost.title or "<None>",
            self.description.capitalize())
    
    @property
    def description(self):
        return getattr(self, 'ztype', '')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZEMOTION'

class Feed(PathCoreDatum):
    
    zcoverheight = models.IntegerField(
        null=True,
        db_column=u'ZCOVERHEIGHT',
        blank=True)
    
    zcoverwidth = models.IntegerField(
        null=True,
        db_column=u'ZCOVERWIDTH',
        blank=True)
    
    zfriendsincommon = models.IntegerField(
        null=True,
        db_column=u'ZFRIENDSINCOMMON',
        blank=True)
    
    zgapdetected = models.IntegerField(
        null=True,
        db_column=u'ZGAPDETECTED',
        blank=True)
    
    zmomentcount = models.IntegerField(
        null=True,
        db_column=u'ZMOMENTCOUNT',
        blank=True)
    
    zpathcreated = models.TextField(
        db_column=u'ZPATHCREATED',
        blank=True,
        null=True)
    
    zcoverfileurlhash = models.TextField(
        db_column=u'ZCOVERFILEURLHASH',
        blank=True,
        null=True)
    
    zcoverurl = models.TextField(
        db_column=u'ZCOVERURL',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    @property
    def url(self):
        return getattr(self, 'zcoverurl', '')
    
    @display(desc="Image URL")
    def get_url(self):
        if self.url:
            return """<img src="%s" />""" % self.url
        return ""
    
    list_display = (
        'id', 'get_url', 'title', 'get_description')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZFEED'

class FriendSuggestion(PathCoreDatum):
    
    zperson = models.ForeignKey('jangypath.Person',
        related_name='suggested_to',
        db_column=u'ZPERSON',
        null=True,
        blank=True)
    
    zsuggestedby = models.ForeignKey('jangypath.Person',
        related_name='suggested_by',
        db_column=u'ZSUGGESTEDBY',
        null=True,
        blank=True)
    
    zcreated = models.TextField(
        db_column=u'ZCREATED',
        blank=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZFRIENDSUGGESTION'

class Invite(PathCoreDatum):
    
    zdate = models.TextField(
        db_column=u'ZDATE',
        blank=True,
        null=True)
    
    zdestination = models.TextField(
        db_column=u'ZDESTINATION',
        blank=True,
        null=True)
    
    zerror = models.TextField(
        db_column=u'ZERROR',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zmethod = models.TextField(
        db_column=u'ZMETHOD',
        blank=True,
        null=True)
    
    zstate = models.TextField(
        db_column=u'ZSTATE',
        blank=True)
    
    zcontactdata = BinaryPropertyList(
        db_column=u'ZCONTACTDATA',
        blank=True,
        null=True)
    
    zhistorydata = models.TextField(
        db_column=u'ZHISTORYDATA',
        blank=True,
        null=True)
    
    @property
    def name(self):
        first = self.zcontactdata.get('first_name', '')
        last = self.zcontactdata.get('last_name', '')
        return ("%s %s" % (
            first and first or '',
            last and last or '')).strip()
    
    @property
    def facebook_id(self):
        return self.zcontactdata.get('facebook_id', '')
    
    @property
    def phone_numbers(self):
        return self.zcontactdata.get('normalized_phone_numbers', '')
    
    @property
    def email_addresses(self):
        return self.zcontactdata.get('email_addresses', '')
    
    @property
    def title(self):
        return self.name
    
    @property
    def description(self):
        return "%s (via %s)" % (
            getattr(self, 'zstate', ''),
            getattr(self, 'zmethod', ''))
    
    fields = ('name', 'facebook_id', 'phone_numbers', 'email_addresses')
    list_display = (
        'id', 'title', 'get_description', 'url',
        'name', 'facebook_id', 'phone_numbers', 'email_addresses')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZINVITE'

class Location(PathCoreDatum):
    
    zistemporary = models.IntegerField(
        null=True,
        db_column=u'ZISTEMPORARY',
        blank=True)
    
    zaccuracy = models.TextField(
        db_column=u'ZACCURACY',
        blank=True,
        null=True)
    
    zdirection = models.TextField(
        db_column=u'ZDIRECTION',
        blank=True,
        null=True)
    
    zelevation = models.TextField(
        db_column=u'ZELEVATION',
        blank=True,
        null=True)
    
    zelevationaccuracy = models.TextField(
        db_column=u'ZELEVATIONACCURACY',
        blank=True,
        null=True)
    
    zlatitude = models.TextField(
        db_column=u'ZLATITUDE',
        blank=True,
        null=True)
    
    zlongitude = models.TextField(
        db_column=u'ZLONGITUDE',
        blank=True,
        null=True)
    
    zspeed = models.TextField(
        db_column=u'ZSPEED',
        blank=True,
        null=True)
    
    zcity = models.TextField(
        db_column=u'ZCITY',
        blank=True,
        null=True)
    
    zcityid = models.TextField(
        db_column=u'ZCITYID',
        blank=True,
        null=True)
    
    zcountry = models.TextField(
        db_column=u'ZCOUNTRY',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True,
        null=True)
    
    zneighborhood = models.TextField(
        db_column=u'ZNEIGHBORHOOD',
        blank=True,
        null=True)
    
    zpostalcode = models.TextField(
        db_column=u'ZPOSTALCODE',
        blank=True,
        null=True)
    
    zprovince = models.TextField(
        db_column=u'ZPROVINCE',
        blank=True,
        null=True)
    
    zprovincecode = models.TextField(
        db_column=u'ZPROVINCECODE',
        blank=True,
        null=True)
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZLOCATION'

class Movie(PathCoreDatum):
    
    zcriticsscore = models.IntegerField(
        null=True,
        db_column=u'ZCRITICSSCORE',
        blank=True)
    
    zindex = models.IntegerField(
        null=True,
        db_column=u'ZINDEX',
        blank=True)
    
    zruntime = models.IntegerField(
        null=True,
        db_column=u'ZRUNTIME',
        blank=True)
    
    zyear = models.IntegerField(
        null=True,
        db_column=u'ZYEAR',
        blank=True)
    
    zcriticsconsensus = models.TextField(
        db_column=u'ZCRITICSCONSENSUS',
        blank=True,
        null=True)
    
    zcriticsrating = models.TextField(
        db_column=u'ZCRITICSRATING',
        blank=True,
        null=True)
    
    zgenre = models.TextField(
        db_column=u'ZGENRE',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zmoviedescription = models.TextField(
        db_column=u'ZMOVIEDESCRIPTION',
        blank=True,
        null=True)
    
    zmpaarating = models.TextField(
        db_column=u'ZMPAARATING',
        blank=True,
        null=True)
    
    zposterurl = models.TextField(
        db_column=u'ZPOSTERURL',
        blank=True,
        null=True)
    
    zsynopsis = models.TextField(
        db_column=u'ZSYNOPSIS',
        blank=True,
        null=True)
    
    ztitle = models.TextField(
        db_column=u'ZTITLE',
        blank=True,
        null=True)
    
    zweburl = models.TextField(
        db_column=u'ZWEBURL',
        blank=True,
        null=True)
    
    zcastdata = BinaryPropertyList(
        db_column=u'ZCASTDATA',
        blank=True,
        null=True)
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZMOVIE'

class Music(PathCoreDatum):
    
    zidiscustom = models.IntegerField(
        null=True,
        db_column=u'ZIDISCUSTOM',
        blank=True)
    
    zindex = models.IntegerField(
        null=True,
        db_column=u'ZINDEX',
        blank=True)
    
    ztracktimemillis = models.IntegerField(
        null=True,
        db_column=u'ZTRACKTIMEMILLIS',
        blank=True)
    
    zreleasedate = models.TextField(
        db_column=u'ZRELEASEDATE',
        blank=True,
        null=True)
    
    zartistid = models.TextField(
        db_column=u'ZARTISTID',
        blank=True,
        null=True)
    
    zartistname = models.TextField(
        db_column=u'ZARTISTNAME',
        blank=True,
        null=True)
    
    zartworkurl100 = models.TextField(
        db_column=u'ZARTWORKURL100',
        blank=True,
        null=True)
    
    zcollectionname = models.TextField(
        db_column=u'ZCOLLECTIONNAME',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zpreviewurl = models.TextField(
        db_column=u'ZPREVIEWURL',
        blank=True,
        null=True)
    
    zprimarygenrename = models.TextField(
        db_column=u'ZPRIMARYGENRENAME',
        blank=True,
        null=True)
    
    ztrackid = models.TextField(
        db_column=u'ZTRACKID',
        blank=True,
        null=True)
    
    ztrackname = models.TextField(
        db_column=u'ZTRACKNAME',
        blank=True,
        null=True)
    
    ztrackviewurl = models.TextField(
        db_column=u'ZTRACKVIEWURL',
        blank=True,
        null=True)
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZMUSIC'

class Person(PathCoreDatum):
    
    zcommonfriends = models.IntegerField(
        null=True,
        db_column=u'ZCOMMONFRIENDS',
        blank=True)
    
    zisfacebookauthenticated = models.IntegerField(
        null=True,
        db_column=u'ZISFACEBOOKAUTHENTICATED',
        blank=True)
    
    zisfriend = models.IntegerField(
        null=True,
        db_column=u'ZISFRIEND',
        blank=True)
    
    zisinactive = models.IntegerField(
        null=True,
        db_column=u'ZISINACTIVE',
        blank=True)
    
    zisincomingrequest = models.IntegerField(
        null=True,
        db_column=u'ZISINCOMINGREQUEST',
        blank=True)
    
    zismale = models.IntegerField(
        null=True,
        db_column=u'ZISMALE',
        blank=True)
    
    zisoutgoingrequest = models.IntegerField(
        null=True,
        db_column=u'ZISOUTGOINGREQUEST',
        blank=True)
    
    zisuser = models.IntegerField(
        null=True,
        db_column=u'ZISUSER',
        blank=True)
    
    zpeoplecount = models.IntegerField(
        null=True,
        db_column=u'ZPEOPLECOUNT',
        blank=True)
    
    zpostcount = models.IntegerField(
        null=True,
        db_column=u'ZPOSTCOUNT',
        blank=True)
    
    zsuggestiongroup = models.IntegerField(
        null=True,
        db_column=u'ZSUGGESTIONGROUP',
        blank=True)
    
    zincomingrequestcreated = models.TextField(
        db_column=u'ZINCOMINGREQUESTCREATED',
        blank=True,
        null=True)
    
    zmostrecentpostdate = models.TextField(
        db_column=u'ZMOSTRECENTPOSTDATE',
        blank=True,
        null=True)
    
    zemail = models.TextField(
        db_column=u'ZEMAIL',
        blank=True,
        null=True)
    
    zfacebookid = models.TextField(
        db_column=u'ZFACEBOOKID',
        blank=True,
        null=True)
    
    zfirstname = models.TextField(
        db_column=u'ZFIRSTNAME',
        blank=True,
        null=True)
    
    zheadline = models.TextField(
        db_column=u'ZHEADLINE',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zlastname = models.TextField(
        db_column=u'ZLASTNAME',
        blank=True,
        null=True)
    
    zphone = models.TextField(
        db_column=u'ZPHONE',
        blank=True,
        null=True)
    
    zphotosharingoriginalurl = models.TextField(
        db_column=u'ZPHOTOSHARINGORIGINALURL',
        blank=True,
        null=True)
    
    zphotosharingurl = models.TextField(
        db_column=u'ZPHOTOSHARINGURL',
        blank=True,
        null=True)
    
    zprimarynetwork = models.TextField(
        db_column=u'ZPRIMARYNETWORK',
        blank=True,
        null=True)
    
    zstate = models.TextField(
        db_column=u'ZSTATE',
        blank=True,
        null=True)
    
    zusername = models.TextField(
        db_column=u'ZUSERNAME',
        blank=True,
        null=True)
    
    zrecentposttypesdata = models.TextField(
        db_column=u'ZRECENTPOSTTYPESDATA',
        blank=True,
        null=True)
    
    zseenitsdata = models.TextField(
        db_column=u'ZSEENITSDATA',
        blank=True,
        null=True)
    
    @property
    def name(self):
        first = self.zfirstname
        last = self.zlastname
        return ("%s %s" % (
            first and first or '',
            last and last or '')).strip()
    
    @property
    def title(self):
        return ("%s %s" % (
            self.zusername,
            self.zemail and self.zemail or '')).strip()
    
    @property
    def description(self):
        return getattr(self, 'zheadline', '')
    
    @property
    def url(self):
        return getattr(self, 'zphotosharingurl', '')
    
    @display(desc="Name")
    def get_name(self):
        return """<nobr>%s</nobr>""" % self.name
    
    @display(desc="Image URL")
    def get_url(self):
        if self.url:
            return """<img src="%s" />""" % self.url
        return ""
    
    fields = ('name',)
    list_display = (
        'id', 'get_url', 'get_name', 'title', 'zprimarynetwork', 'get_description')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZPERSON'

class Place(PathCoreDatum):
    
    zlatitude = models.TextField(
        db_column=u'ZLATITUDE',
        blank=True,
        null=True)
    
    zlongitude = models.TextField(
        db_column=u'ZLONGITUDE',
        blank=True,
        null=True)
    
    zcategory = models.TextField(
        db_column=u'ZCATEGORY',
        blank=True,
        null=True)
    
    zcity = models.TextField(
        db_column=u'ZCITY',
        blank=True,
        null=True)
    
    zcountry = models.TextField(
        db_column=u'ZCOUNTRY',
        blank=True,
        null=True)
    
    ziconurl = models.TextField(
        db_column=u'ZICONURL',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zname = models.TextField(
        db_column=u'ZNAME',
        blank=True,
        null=True)
    
    zparentcategory = models.TextField(
        db_column=u'ZPARENTCATEGORY',
        blank=True,
        null=True)
    
    zphone = models.TextField(
        db_column=u'ZPHONE',
        blank=True,
        null=True)
    
    zstate = models.TextField(
        db_column=u'ZSTATE',
        blank=True,
        null=True)
    
    zstreetaddress = models.TextField(
        db_column=u'ZSTREETADDRESS',
        blank=True,
        null=True)
    
    zstreetaddress2 = models.TextField(
        db_column=u'ZSTREETADDRESS2',
        blank=True,
        null=True)
    
    zzip = models.TextField(
        db_column=u'ZZIP',
        blank=True,
        null=True)
    
    @property
    def description(self):
        return getattr(self, 'zsummary', '')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZPLACE'

class Post(PathCoreDatum):
    
    zidiscustom = models.IntegerField(
        null=True,
        db_column=u'ZIDISCUSTOM',
        blank=True)
    
    zimagepreviewheight = models.IntegerField(
        null=True,
        db_column=u'ZIMAGEPREVIEWHEIGHT',
        blank=True)
    
    zimagepreviewwidth = models.IntegerField(
        null=True,
        db_column=u'ZIMAGEPREVIEWWIDTH',
        blank=True)
    
    zisprivate = models.IntegerField(
        null=True,
        db_column=u'ZISPRIVATE',
        blank=True)
    
    zisread = models.IntegerField(
        null=True,
        db_column=u'ZISREAD',
        blank=True)
    
    zistemporary = models.IntegerField(
        null=True,
        db_column=u'ZISTEMPORARY',
        blank=True)
    
    ziswaitingforpostprocessing = models.IntegerField(
        null=True,
        db_column=u'ZISWAITINGFORPOSTPROCESSING',
        blank=True)
    
    zpeoplecount = models.IntegerField(
        null=True,
        db_column=u'ZPEOPLECOUNT',
        blank=True)
    
    zphotoheight = models.IntegerField(
        null=True,
        db_column=u'ZPHOTOHEIGHT',
        blank=True)
    
    zphotowidth = models.IntegerField(
        null=True,
        db_column=u'ZPHOTOWIDTH',
        blank=True)
    
    zseenitcount = models.IntegerField(
        null=True,
        db_column=u'ZSEENITCOUNT',
        blank=True)
    
    zsharetofacebook = models.IntegerField(
        null=True,
        db_column=u'ZSHARETOFACEBOOK',
        blank=True)
    
    zsharetofoursquare = models.IntegerField(
        null=True,
        db_column=u'ZSHARETOFOURSQUARE',
        blank=True)
    
    zsharetotumblr = models.IntegerField(
        null=True,
        db_column=u'ZSHARETOTUMBLR',
        blank=True)
    
    zsharetotwitter = models.IntegerField(
        null=True,
        db_column=u'ZSHARETOTWITTER',
        blank=True)
    
    zstate = models.IntegerField(
        null=True,
        db_column=u'ZSTATE',
        blank=True)
    
    zuploadattempts = models.IntegerField(
        null=True,
        db_column=u'ZUPLOADATTEMPTS',
        blank=True)
    
    zambientdestinationlocation = models.IntegerField(
        null=True,
        db_column=u'ZAMBIENTDESTINATIONLOCATION',
        blank=True)
    
    zambientoriginlocation = models.IntegerField(
        null=True,
        db_column=u'ZAMBIENTORIGINLOCATION',
        blank=True)
    
    zapplication = models.ForeignKey('jangypath.ApiApplication',
        related_name='posts',
        db_column=u'ZAPPLICATION',
        null=True,
        blank=True)
    
    zbook = models.ForeignKey('jangypath.Book',
        related_name='posts',
        db_column=u'ZBOOK',
        null=True,
        blank=True)
    
    zcommentdraft = models.ForeignKey('jangypath.CommentDraft',
        related_name='posts',
        db_column=u'ZCOMMENTDRAFT',
        null=True,
        blank=True)
    
    zcreator = models.ForeignKey('jangypath.Person',
        related_name='posts',
        db_column=u'ZCREATOR',
        null=True,
        blank=True)
    
    zlocation = models.ForeignKey('jangypath.Location',
        related_name='posts',
        db_column=u'ZLOCATION',
        null=True,
        blank=True)
    
    zmovie = models.ForeignKey('jangypath.Movie',
        related_name='posts',
        db_column=u'ZMOVIE',
        null=True,
        blank=True)
    
    zmusic = models.ForeignKey('jangypath.Music',
        related_name='posts',
        db_column=u'ZMUSIC',
        null=True,
        blank=True)
    
    zparentpost = models.ForeignKey('self',
        related_name='child_posts',
        db_column=u'ZPARENTPOST',
        null=True,
        blank=True)
    
    zplace = models.IntegerField(
        null=True,
        db_column=u'ZPLACE',
        blank=True)
    
    zcapturedatdate = models.TextField(
        db_column=u'ZCAPTUREDATDATE',
        blank=True,
        null=True)
    
    zcommentslastupdated = models.TextField(
        db_column=u'ZCOMMENTSLASTUPDATED',
        blank=True,
        null=True)
    
    zcreationdate = models.TextField(
        db_column=u'ZCREATIONDATE',
        blank=True,
        null=True)
    
    zserverdate = models.TextField(
        db_column=u'ZSERVERDATE',
        blank=True,
        null=True)
    
    zuploadprogress = models.TextField(
        db_column=u'ZUPLOADPROGRESS',
        blank=True,
        null=True)
    
    zvideoduration = models.TextField(
        db_column=u'ZVIDEODURATION',
        blank=True,
        null=True)
    
    zambienticonstring = models.TextField(
        db_column=u'ZAMBIENTICONSTRING',
        blank=True,
        null=True)
    
    zambienturl = models.TextField(
        db_column=u'ZAMBIENTURL',
        blank=True,
        null=True)
    
    zapisubtype = models.TextField(
        db_column=u'ZAPISUBTYPE',
        blank=True,
        null=True)
    
    zfilter = models.TextField(
        db_column=u'ZFILTER',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True,
        null=True)
    
    zinfostring = models.TextField(
        db_column=u'ZINFOSTRING',
        blank=True,
        null=True)
    
    zphotofilepath = models.TextField(
        db_column=u'ZPHOTOFILEPATH',
        blank=True,
        null=True)
    
    zphotooriginalurl = models.TextField(
        db_column=u'ZPHOTOORIGINALURL',
        blank=True,
        null=True)
    
    zphotourl = models.TextField(
        db_column=u'ZPHOTOURL',
        blank=True,
        null=True)
    
    zserverstate = models.TextField(
        db_column=u'ZSERVERSTATE',
        blank=True,
        null=True)
    
    zsubtype = models.TextField(
        db_column=u'ZSUBTYPE',
        blank=True,
        null=True)
    
    zsummary = models.TextField(
        db_column=u'ZSUMMARY',
        blank=True,
        null=True)
    
    ztemplate = models.TextField(
        db_column=u'ZTEMPLATE',
        blank=True,
        null=True)
    
    zthought = models.TextField(
        db_column=u'ZTHOUGHT',
        blank=True,
        null=True)
    
    ztype = models.TextField(
        db_column=u'ZTYPE',
        blank=True,
        null=True)
    
    zvideofeedurl = models.TextField(
        db_column=u'ZVIDEOFEEDURL',
        blank=True,
        null=True)
    
    zvideofilepath = models.TextField(
        db_column=u'ZVIDEOFILEPATH',
        blank=True,
        null=True)
    
    zapimomentdata = BinaryPropertyList(
        db_column=u'ZAPIMOMENTDATA',
        blank=True,
        null=True)
    
    zpeopledata = BinaryPropertyList(
        db_column=u'ZPEOPLEDATA',
        blank=True,
        null=True)
    
    zpeoplewithoutaccounts = models.TextField(
        db_column=u'ZPEOPLEWITHOUTACCOUNTS',
        blank=True,
        null=True)
    
    zseenitdata = BinaryPropertyList(
        db_column=u'ZSEENITDATA',
        blank=True,
        null=True)
    
    zthoughtlinkdata = BinaryPropertyList(
        db_column=u'ZTHOUGHTLINKDATA',
        blank=True,
        null=True)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('jangypath:post',
            current_app='jangypath',
            kwargs=dict(post_id=self.zid))
    
    @property
    def seen_by(self):
        seenitdata = self.zseenitdata or []
        return Person.objects.filter(
            zid__in=seenitdata)
    
    @property
    def mentions(self):
        peopledata = self.zpeopledata or {}
        return Person.objects.filter(
            zid__in=map(lambda d: d['id'],
                filter(lambda d: d['type'] == 'path',
                    peopledata)))
    
    @property
    def name(self):
        return self.zcreator.name
    
    @property
    def title(self):
        return ("%s %s" % (
            self.zid,
            self.zsummary and self.zsummary or '')).strip()
    
    @property
    def url(self):
        return getattr(self, 'zphotourl', '')
    
    @display(desc="Seen By")
    def get_seen_by(self):
        if len(self.seen_by) > 0:
            out_list = ", ".join("""<nobr><b>%s</b></nobr>""" % eyewitness.name \
                for eyewitness in self.seen_by)
            return "Seen by %s" % out_list
        return ''
    
    @display(desc="Mentioning")
    def get_mentions(self):
        if len(self.mentions) > 0:
            out_list = ", ".join("""<nobr><b>%s</b></nobr>""" % accomplice.name \
                for accomplice in self.mentions)
            return "Mentioning %s" % out_list
        return ''
    
    @display(desc="Name")
    def get_name(self):
        return """<nobr>%s</nobr>""" % self.name
    
    @display(desc="Image URL")
    def get_url(self):
        if self.ztype.lower() == 'photo':
            return """<a href="%s"><img src="%s" /></a>""" % (
                self.get_absolute_url(), self.url)
        return ""
    
    fields = ('ztype', 'seen_by', 'mentions')
    list_display = (
        'id', 'get_url', 'name', 'get_description',
        'get_seen_by', 'get_mentions')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZPOST'

class Recommendation(PathCoreDatum):
    
    zlatitude = models.TextField(
        db_column=u'ZLATITUDE',
        blank=True,
        null=True)
    
    zlongitude = models.TextField(
        db_column=u'ZLONGITUDE',
        blank=True,
        null=True)
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zdata = BinaryPropertyList(
        db_column=u'ZDATA',
        blank=True,
        null=True)
    
    @property
    def data_objects(self):
        return self.zdata['$objects'][2:-1]
    
    @property
    def place_recommendations(self):
        import watson
        out = []
        for i in xrange(len(self.data_objects)):
            out.append(
                watson.search(self.data_objects[i])[0].object)
        return out
    
    @property
    def person_recommendations(self):
        from pprint import pformat
        return pformat(self.data_objects)
    
    @display(desc="Recommendations")
    def get_person_recommendations(self):
        return """<pre>%s</pre>""" % self.person_recommendations
    
    list_display = (
        'id', 'title', 'place_recommendations', 'get_person_recommendations')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZRECOMMENDATION'

class SuggestionGroup(PathCoreDatum):
    
    zid = models.TextField(
        db_column=u'ZID',
        blank=True)
    
    zdata = BinaryPropertyList(
        db_column=u'ZDATA',
        blank=True,
        null=True)
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'ZSUGGESTIONGROUP'

class SeenPosts(PathCoreDatum):
    
    z_13seenitspeople = models.IntegerField(
        blank=True, null=True,
        db_column=u'Z_13SEENITSPEOPLE')
        # [Removed primary_key=True param. -ed]
    
    z_15seenposts = models.IntegerField(
        primary_key=True,
        db_column=u'Z_15SEENPOSTS')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'Z_13SEENPOSTS'
        unique_together = ('z_13seenitspeople','z_15seenposts')

class TaggedPosts(PathCoreDatum):
    
    z_13taggedusers = models.IntegerField(
        blank=True, null=True,
        db_column=u'Z_13TAGGEDUSERS')
        # [Removed primary_key=True param. -ed]
    
    z_15taggedposts = models.IntegerField(
        primary_key=True,
        db_column=u'Z_15TAGGEDPOSTS')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'Z_13TAGGEDPOSTS'
        unique_together = ('z_13taggedusers','z_15taggedposts')

class Recommendations(PathCoreDatum):
    
    z_14places = models.IntegerField(
        blank=True, null=True,
        db_column=u'Z_14PLACES')
        # [Removed primary_key=True param. -ed]
    
    z_16recommendations = models.IntegerField(
        primary_key=True,
        db_column=u'Z_16RECOMMENDATIONS')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'Z_14RECOMMENDATIONS'
        unique_together = ('z_14places','z_16recommendations')

class Posts(PathCoreDatum):
    
    z_7feeds = models.IntegerField(
        blank=True, null=True,
        db_column=u'Z_7FEEDS')
        # [Removed primary_key=True param. -ed]
    
    z_15posts = models.IntegerField(
        primary_key=True,
        db_column=u'Z_15POSTS')
    
    class Meta(PathCoreDatum.Meta):
        db_table = u'Z_7POSTS'
        unique_together = ('z_7feeds','z_15posts')

class MetaData(PathCoreMetaDatum):
    """ Model class representing a metadatum in the Path app's schema """
    
    z_version = models.IntegerField(
        blank=True,
        null=True,
        db_column=u'Z_VERSION')
    
    z_uuid = models.CharField(
        primary_key=True,
        max_length=255,
        db_column=u'Z_UUID')
    
    z_plist = BinaryPropertyList(
        db_column=u'Z_PLIST',
        blank=True)
    
    class Meta(PathCoreMetaDatum.Meta):
        db_table = u'Z_METADATA'

class PrimaryKey(PathCoreMetaDatum):
    """ NOTE: I am not exactly sure how this is supposed to work;
        my guess is that I did actually know this, like at one point,
        based on how it appears that I was gearing up to do stuff with
        this class. That was a while ago, though, erm. """
    
    z_ent = models.IntegerField(
        db_column=u'Z_ENT',
        primary_key=True)
    
    z_name = models.TextField(
        db_column=u'Z_NAME',
        blank=True)
    
    z_super = models.IntegerField(
        null=True,
        db_column=u'Z_SUPER',
        blank=True)
    
    z_max = models.IntegerField(
        null=True,
        db_column=u'Z_MAX',
        blank=True)
    
    class Meta(PathCoreMetaDatum.Meta):
        db_table = u'Z_PRIMARYKEY'
        ordering = ['z_ent', 'z_super', 'z_name']

# watson registration
import watson
for model in coredata_models:
    watson.register(model, adapter_cls=model.adapter())
watson.register(MetaData)
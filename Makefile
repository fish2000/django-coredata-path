
# SOLR
SOLR_ROOT = local/lib/solr/example
SOLR_LIB = $(SOLR_ROOT)/solr/lib
SOLR_STOPWORDS_LANG = $(SOLR_CONF)/lang/stopwords_en.txt
SOLR_STOPWORDS_COPY_TO = $(SOLR_STOPWORDS_LANG) $(SOLR_STOPWORDS_EN)

# deployment
NGINX_CONF = /etc/nginx/sites-available/$(INSTANCE_SAFE_NAME)
NGINX_CONF_BACKUP = $(INSTANCE_TMP)/$(INSTANCE_NAME).nginx.conf.BACKUP
NGINX_DEPLOY = etc/$(INSTANCE_NAME).nginx.conf
SUPERVISOR_INIT = /etc/init.d/supervisord
SUPERVISOR_INIT_DEPLOY = etc/$(INSTANCE_NAME).supervisord-init.sh
REQUIREMENTS = etc/requirements.txt

# javascript post-processing
MAXJS = $(shell find instance -type f \( -iname "*.js" ! -name "*.min.js" ! -ipath "*libs*" \))
MINJS = $(MAXJS:.js=.min.js)

deploy: deploy-git
deploy-all: deploy-git deploy-uwsgi deploy-nginx

# HEY GUYS!
# GETTING MOST OF THIS 'DEPLOY' STUFF WORKING WILL TAKE SOME DOING ON YOUR PART.
# You'll need to create users, verify that nginx is installed, possibly dip into visudo, etc.
# This is a STARTING POINT. So have a good start with it, yes!
deploy-git:
		git pull
		bin/python manage.py collectstatic --noinput
		test -r $(NGINX_CONF) && cp $(NGINX_CONF) $(INSTANCE_TMP)/$(INSTANCE_NAME).nginx.conf.BACKUP

deploy-uwsgi:
		# NEEDS SUDOING
		sudo $(SUPERVISORCTL) restart $(INSTANCE_NAME):uwsgi $(INSTANCE_NAME):memcached

deploy-nginx:
		# NEEDS SUDOING
		sudo cp $(NGINX_DEPLOY) $(NGINX_CONF) && sudo service nginx restart

deploy-pip:
		bin/pip install -U -r $(REQUIREMENTS)

deploy-supervisor:
		# NEEDS SUDOING
		sudo service supervisord restart

deploy-supervisor-init:
		test -r $(SUPERVISOR_INIT) && cp $(SUPERVISOR_INIT) $(INSTANCE_TMP)/$(INSTANCE_NAME).supervisor-init.sh.BACKUP
		sudo cp $(SUPERVISOR_INIT_DEPLOY) $(SUPERVISOR_INIT)
		sudo chmod +x $(SUPERVISOR_INIT)
		sudo update-rc.d supervisord defaults
		# SUPERVISORD CAN NOW BE STARTED:
		# sudo service supervisord start

clean-js:
		rm -f $(MINJS)

%.min.js: %.js
		bin/uglifyjs -o $@ $<

minify: $(MAXJS:.js=.min.js)
		bin/python manage.py collectstatic --noinput

js: clean-js minify
static: js
		$(SUPERVISORCTL) restart $(INSTANCE_NAME):memcached $(INSTANCE_NAME):uwsgi

# SOLR_SCHEMA gets assigned when `env_preinit` runs
schema-generate: $(SOLR_STOPWORDS_COPY_TO)
		bin/python manage.py build_solr_schema -f $(SOLR_SCHEMA) --verbosity=2

schema-patch: $(SOLR_STOPWORDS_COPY_TO)
		patch -p1 schema.xml \
			-d $(shell dirname `readlink etc/solr-schema.xml`) \
				< etc/solr-lire-schema-fields.patch

schema: schema-generate schema-patch

# There are basically two of this next rule --
# I am not at all sure which `stopwords.txt` file
# has to be where, for Solr to not freak out
# and bail when you tell it to launch.
$(SOLR_STOPWORDS_LANG): $(SOLR_STOPWORDS)
		cp $(SOLR_STOPWORDS) $(SOLR_STOPWORDS_LANG)

$(SOLR_STOPWORDS_EN): $(SOLR_STOPWORDS)
		cp $(SOLR_STOPWORDS) $(SOLR_STOPWORDS_EN)

clean: clean-pyc

distclean: clean-schema clean-all-pyc

clean-schema:
		rm -f $(SOLR_SCHEMA) && touch $(SOLR_SCHEMA)

clean-pyc:
		find $(INSTANCE) -name \*.pyc -print -delete

clean-all-pyc:
		find $(VIRTUAL_ENV) -name \*.pyc -print -delete

.PHONY: schema all distclean clean js minify static


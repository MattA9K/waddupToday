from django.db import models
import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from markdown import markdown
from tagging.fields import TagField

from django.conf import settings

#time used for upload form
from time import time



class Category(models.Model):
	title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
	slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title. Must be unique.')
	description = models.TextField()
	
	
	def __unicode__(self):
		return self.title
		
#_______________________________________________________________
#   ||															|
#  \||/   USED FOR SORTING THE CATEGORIES INSIDE THE ADMIN PANEL|
#   \/															|
	class Meta:									#				|
		ordering = ['title']					#				|	
		verbose_name_plural = "Categories"		#				|
#_______________________________________________________________|

#_______________________________________________________________
#   ||															|
#  \||/   Will return a string with the value of the categories |
#   \/		slug field											|
	def get_absolute_url(self):					#				|
		return "/categories/%s/" % self.slug	#				|	
												#				|
#_______________________________________________________________|




class Hashtag(models.Model):
	title = models.CharField(max_length=40, help_text='Maximum 40 characters.')
	num_used = models.IntegerField(default=0)
	last_used = models.DateTimeField(default=datetime.datetime.now)
	
	def __unicode__(self):
		return self.title
#_______________________________________________________________
#   ||															|
#  \||/   USED FOR SORTING THE CATEGORIES INSIDE THE ADMIN PANEL|
#   \/															|
	class Meta:									#				|
		ordering = ['title']					#				|	
		verbose_name_plural = "Hashtags"		#				|
#_______________________________________________________________|




def get_upload_file_name(instance, filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)
	
	

class LiveEntryManager(models.Manager):
	def get_query_set(self):
		return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)
# BLOG POST OBJECT FOR THE WEB APP			requires: sudo pip install pytz 
#_______________________________________________________________________
#   ||															        |
#  \||/   BLOG 												            |
#   \/															        |
class Entry(models.Model):
	title = models.CharField(max_length=250)
	slug = models.SlugField(unique_for_date='pub_date')
	excerpt = models.TextField(blank=True)
	body = models.TextField()
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	author = models.ForeignKey(User, default=1)
	enable_comments = models.BooleanField(default=True)
	features = models.BooleanField(default=False)
	
	num_comments = models.IntegerField(default=0)
	num_views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	thumbnail = models.FileField(upload_to=get_upload_file_name)
	
	rating_sum = models.DecimalField(max_digits=10, decimal_places=1, default=0)
	rating_current = models.DecimalField(max_digits=10, decimal_places=1, default=0)
	
	#awesome hashtag stuff!
	tags = models.ManyToManyField(Hashtag)
	
	#used for the HTML template filters for writing entries
	excerpt_html = models.TextField(editable=False, blank=True)
	body_html = models.TextField(editable=False, blank=True)
	
	#many to many is a way of relating two models to each other
	categories = models.ManyToManyField(Category) # VERY USEFUL used for TAGGING! inherits from the Category class
	
	#adds ability to compose draft or unlisted posts
	LIVE_STATUS = 1
	DRAFT_STATUS = 2
	HIDDEN_STATUS = 3
	STATUS_CHOICES = (
		(LIVE_STATUS, 'Live'),
		(DRAFT_STATUS, 'Draft'),
		(HIDDEN_STATUS, 'Hidden'),
	)
	status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
	live = LiveEntryManager()
	objects = models.Manager()
												        			   #|
#_______________________________________________________________________|


	def __unicode__(self):
		return self.title
		
		
#_______________________________________________________________
#   ||															|
#  \||/   USED FOR SORTING THE CATEGORIES INSIDE THE ADMIN PANEL|
#   \/															|
	class Meta:									#				|				
		verbose_name_plural = "Entries"			#				|
		ordering = ['-pub_date']				#				|
#_______________________________________________________________|


#_______________________________________________________________
#   ||															|
#  \||/   runs Markdown over the body field and stores the 	    |
#   \/		resulting HTML in body_HTML							|
	def save(self, force_insert=False, force_update=False):	   #|
		self.body_html = markdown(self.body)	#				|	
		if self.excerpt:
			self.excerpt_html = markdown(self.excerpt)	
		super(Entry, self).save(force_insert, force_update)	#	|
#_______________________________________________________________|

#_______________________________________________________________
#   ||															|
#  \||/   Will return a string with the value of the categories |
#   \/		slug field											|
	def get_absolute_url(self):					#				|
		return "/weblog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
												#				|
#_______________________________________________________________|


class EntryAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'slug': ['title'] }
	
	
	
	
class Link(models.Model):
	title = models.CharField(max_length=250)
	description = models.TextField(blank=True)
	description_html = models.TextField(blank=True)
	url = models.URLField(unique=True)
	posted_by = models.ForeignKey(User)
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	slug = models.SlugField(unique_for_date='pub_date')
	tags = TagField()
	enable_comments = models.BooleanField(default=True)
	post_elsewhere = models.BooleanField('Post to Delicious', default=True)
	
	via_name = models.CharField('Via',
								max_length=250,
								blank=True,
								help_text='The name of the person whose site you spotted the link on. Optional.')
	via_url = models.URLField('Via URL',
							  blank=True,
							  help_text='The URL of the site where you spotted the link. Optional.')

	class Meta:
		ordering = ['-pub_date']
		
	def __unicode__(self):
		return self.title
		
	def save(self):
		if self.description:
			self.description_html = markdown(self.description)
		if not self.id and self.post_elsewhere:
			import pydelicious
			from django.utils.encoding import smart_str
			pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD,
							smart_str(self.url), smart_str(self.title),
							smart_str(self.tags))
		super(Link, self).save()
	
	def get_absolute_url(self):
		return (
			'coltrane_link_detail',
			(),
			{
				'year': self.pub_date.strftime('%Y'),
				'month': self.pub_date.strftime('%b').lower(),
				'day': self.pub_date.strftime('%d'),
				'slug': self.slug
			}
		)
	get_absolute_url = models.permalink(get_absolute_url)
	
	
class Comments(models.Model):
	parent_entry = models.ForeignKey(Entry, default=3)
	author = models.CharField(max_length=250)
	author_id = models.IntegerField(default=0)
	body = models.TextField()
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	
	def __unicode__(self):
		return self.body
		
	def get_parent(self):
		return self.parent_entry




class User_Likes(models.Model):
	user = models.IntegerField(default=0)
	liked_entry = models.IntegerField(default=0)
	
	
	
	
class User_Profile(models.Model):
	uid = models.ForeignKey(User)
	bio = models.TextField()
	website = models.CharField(max_length=80)
	avatar = models.FileField(upload_to=get_upload_file_name)
	is_setup = models.BooleanField(default=False)
	
	num_views = models.IntegerField(default=0)
	num_posts = models.IntegerField(default=0)
	num_comments = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)

from django.conf.urls import patterns, include, url
from tagging.models import Tag

from django.contrib import admin
admin.autodiscover()

from coltrane.models import Entry, Link, Category, User_Profile




entry_info_dict = {
	'queryset': Entry.objects.all(),
	'date_field': 'pub_date',
}

category_info_dict = {
	'queryset': Category.objects.all(),
	'title': 'title',
}

link_info_dict = {
	'queryset': Link.objects.all(),
	'date_field': 'pub_date',
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'coltrane.views.home_page'),
    
    #url(r'^pages/', include('django.contrib.flatpages.urls')),
    
    (r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
    			{'document_root': '/var/www/apress/cms/templates/tinymce'}),
    			
    (r'^search/$', 'coltrane.views.search_titles'),
    
    (r'^search_hash/$', 'coltrane.views.search_hashes'),
    
    (r'^login/$', 'coltrane.views.user_login'),
    (r'^register/$', 'coltrane.views.user_register'),
    (r'^register_process/$', 'coltrane.views.register'),
    (r'^auth/$', 'coltrane.views.user_auth'),
    (r'^logout/$', 'coltrane.views.user_logout'),
    
    (r'^weblog/$', 'coltrane.views.entries_index'),
    
    (r'^tags/$', 'coltrane.views.tags'),
    (r'^tags/(?P<id>[-\w]+)/$', 'coltrane.views.tag_detail'),
    
	#(r'^weblog/(P?<slug>[-\w]+)/$',
	#						'coltrane.views.entry_detail'),
    
    (r'^user/(?P<user_id>\d+)/$', 'coltrane.views.user_index'),
    
    (r'^weblog/(?P<entry_id>\d+)/$', 'coltrane.views.entry_detail'),
	
	(r'^links/$', 'archive_index', link_info_dict, 'coltrane_link_archive_index'),
	
	(r'^create/$', 'coltrane.views.create'),
	(r'^create_pick/$', 'coltrane.views.create_pick'),
	(r'^create_text/$', 'coltrane.views.create_text'),
	(r'^create_url/$', 'coltrane.views.create_url'),
	
	#user profile views:
	(r'^update_profile/$', 'coltrane.views.user_profile_setup'),
	(r'^profile/$', 'coltrane.views.profile'),
	(r'^profile_list/$', 'coltrane.views.profile_list'),
	
	url(r'^add_comment/(?P<entry_id>\d+)/$', 'coltrane.views.add_comment'),
	
	url(r'^rate1/(?P<entry_id>\d+)/$', 'coltrane.views.like_entry1'),
	url(r'^rate2/(?P<entry_id>\d+)/$', 'coltrane.views.like_entry2'),
	url(r'^rate3/(?P<entry_id>\d+)/$', 'coltrane.views.like_entry3'),
	url(r'^rate4/(?P<entry_id>\d+)/$', 'coltrane.views.like_entry4'),
	url(r'^rate5/(?P<entry_id>\d+)/$', 'coltrane.views.like_entry5'),
														 		
	
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/user/password/reset/done/'}, name="password_reset"),
    (r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),											 
)

"""
urlpatterns += patterns('coltrane.views',
    (r'^categories/$', 'category_list'),
    (r'^categories/(?P<slug>[-\w]+)/$', 'category_detail'),
)
"""
#apparently the top does the same as the bottom
#the bottom will be commented out
urlpatterns += patterns('',
    (r'^categories/$', 'coltrane.views.category_list'),
    (r'^categories/(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail'), #newest
    
    (r'^categories/comments/(?P<slug>[-\w]+)/$', 'coltrane.views.category_comments'), #most views
    (r'^categories/views/(?P<slug>[-\w]+)/$', 'coltrane.views.category_views'), #most views
    (r'^categories/likes/(?P<slug>[-\w]+)/$', 'coltrane.views.category_likes'), #most likes
)

"""
urlpatterns += patterns('',
	(r'^tags/$', 'django.views.generic.list.ListView', { 'queryset': Tag.objects.all() }),
	(r'^tags/entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Entry, 'template_name': 'coltrane/entries_by_tag.html' }),
	(r'^tags/links/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', {'queryset_or_model': Link, 'template_name': 'coltrane/links_by_tag.html' }),
)"""

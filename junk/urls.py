from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'junk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','views.dashboard'),
    url(r'^facebook_connect/$', 'views_fb.facebook_connect'),
    url('^accounts/facebook_callback/$','views_fb.facebook_callback'),
    url(r'^twitter_connect/$','views_tw.twitter_connect'),
    url(r'^accounts/twitter_callback/$','views_tw.twitter_callback'),
    url('^accounts/login/$','views_login.login_screen'),
    url('^accounts/create/$','views_login.create'),
    url('^confirmed/$','views_login.confirmed'),
    url('^accounts/logout/$','views_login.logout_view'),
    url(r'^in_connect/$','views_in.in_connect'),
    url(r'^accounts/in_callback/$','views_in.in_callback'),
    url(r'^g_connect/$','views_g.g_connect'),
    url(r'^accounts/g_callback/$','views_g.g_callback'),

    url(r'^upload/$','views_upload.upload'),
    url(r'^upload_process/$','views_upload.upload_process'),	

    #custom tab for FB Biz page
    url(r'^fb_custom_tab/$','views_fb_custom_tab.custom_tab'),

)

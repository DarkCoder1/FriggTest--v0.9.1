from django.conf.urls import patterns, include, url
from django.contrib import admin
from FriggAnswer.views import question_view, upload_view

urlpatterns = [
    # Examples:
    # url(r'^$', 'FriggTest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'FriggAnswer/$', question_view),
    url(r'FriggAnswerFiles/$', upload_view),
    #url(r'FriggResponse/$', bar),
]

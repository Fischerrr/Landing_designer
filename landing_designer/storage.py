from django.contrib.staticfiles.storage import StaticFilesStorage
from django.conf import settings
from django.utils.safestring import mark_safe


# Because visitors' browsers locally store a cached copy of the static files,
# there is a possibility for them not to see the changes when you update your site
# By creating a hashed CSS file, the user will always have the current version of CSS.
class StaticVersionStaticFilesStorage(StaticFilesStorage):
    def __init__(self, *args, **kwargs):
        self.touch_id = settings.TOUCH_ID
        super(StaticVersionStaticFilesStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        url = super(StaticVersionStaticFilesStorage, self).url(name)
        return mark_safe('{}{}hash={}'.format(url, '&' if url.find('?') > -1 else '?', self.touch_id))

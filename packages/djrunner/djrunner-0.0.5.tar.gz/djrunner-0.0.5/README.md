
# Quick run django project

This app makes it possible to add custom settings from child apps __init__ file,
so to install it you just have to add your app to requirements.txt and INSTALLED_APPS.
It will install itself automatically.
It also helps you to reduce number of django settings and quickly setup production environment.
I'll update docs later. You can ask the questions here: pmaigutyak@gmail.com

Project structure:
* core
  * common_settings.py
  * settings.py
  * settings.example.py
  * urls.py
  * wsgi.py
* locale
* templates
* manage.py
* requirements.txt

### Installation
1. Add `djrunner` to `requirements.txt`

`.gitignore` must contain:
* core/settings.py
* tmp
* *.pyc

`common_settings.py` example:
```
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'project secret key'
DB_NAME = 'project db'
INSTALLED_APPS = [
  'app1',
  ...
]
```

`settings.py` example:

```
from core.common_settings import *

from djrunner import setup_settings

setup_settings(globals())
```

`urls.py` example:
```

from django.conf.urls import path, include

from djrunner import setup_urlpatterns


urlpatterns = [

    path('admin/', admin.site.urls),

    ...

]

setup_urlpatterns(urlpatterns)
```

## Child app

App structure:
* __init__.py
* urls.py

`__init__.py` example:

```

import os

from django.apps import AppConfig
from django.conf import global_settings


def setup_settings(settings, is_prod, **kwargs):

    settings['MY_CUSTOM_VAR'] = True


class MyAppConfig(AppConfig):

    name = 'myapp'


default_app_config = 'myapp.MyAppConfig'

```

`urls.py` example:

```

from django.urls import path, include

from django.conf.urls.i18n import i18n_patterns

from myapp import views


app_name = 'myapp'


urlpatterns = [
    path('somepath/', views.someview, name='myview')
]


app_urls = i18n_patterns(

    path('myapp/', include((urlpatterns, app_name))),

)
```

# Exact steps for how I got to this repo in 15 minutes
I worked on [The Amendments Project](https://amendmentsproject.org/) over the summer - inspired by that dataset, here is a project to set up an API to serve amendments data with Django that I completed in 15 minutes (the docs took longer than the initial runthrough).

## Initial setup
```
mkdir djangoapidemo
cd djangoapidemo
python -m venv djangoapienv
code .
source djangoapienv/bin/activate
```

## Install requirements
`touch requirements.txt`

```
django>=5.0
djangorestframework >= 3.14.0
requests
```

`pip install -r requirements.txt`

## First run
Create the Django project. It will use a local SQLLite database by default which is enough for this starter project demo.
```bash
django-admin startproject djangoapidemo
cd djangoapidemo
python manage.py runserver
```

You should see the Close the runserver with Ctrl+C

## First migrations
python manage.py migrate

## Make the first app
`python manage.py startapp api`
### Make the templates directory
    Make home.html:
```html
    <html>
        <body>
            <h1>Home page</h1>
        </body>
    </html>
```
### Add the views
    In api/views.py, add the view. We use the Django render shortcut to render the template using the request we got from the user and the template name:
    ```
    def home(request):
        return render(request, 'home.html')
    ```
        
### Configure settings
- Add `api` to settings.py INSTALLED_APPS
- Add BASE_DIR / "api/templates", to TEMPLATES DIRS[]
- Add the URL patterns to connect the view to the template based on a URL. In djangoapi/urls.py:
    from api import views as api_views
    urlpatterns = [
        path("", api_views.home, name="home"), # this is the new line that says, at the root URL, use the home view
        path('admin/', admin.site.urls),
    ]
- Run `python manage.py runserver`. See the changes!

## Django models
### Make the model
In api/models.py, add the model class:
```python
    class Amendment(models.Model):
        date = models.DateField()
        text = models.TextField()
        title = models.CharField(max_length=100)

        def __str__(self):
            return self.title
```
### Make and run migrations   
`python manage.py makemigrations`
This creates a new migration file in api/migrations
`python manage.py migrate`

## Add data to our model
Now, add an amendment. Here's some amendment text to use: https://constitution.congress.gov/constitution/amendment-1/

We can do this from the Django shell via the command line:
`python3 manage.py shell`

`>>> from api.models import Amendment`

`>>> a1 = Amendment(title="First Amendment", text="Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances.", date="December 15, 1971")`

`>>> a1.save()`

This fails because the date is not in the right format, and Django automatically validates all fields when you try to save a model. Let's fix that.

`>>> a1 = Amendment(title="First Amendment", text="Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances.", date="1971-12-15")`

`>>> a1.save()`

Now we have some data! We can also create an amendment with the create method:

`>>> Amendment.objects.create(title="Second Amendment", text="A well regulated Militia, being necessary to the security of a free State, the right of the people to keep and bear Arms, shall not be infringed.", date="1791-12-15")`

`>>> Amendment.objects.get(id=1)`

This will show the `__str__` method we defined in the model class:

`<Amendment: First Amendment>`

We can also easily get a list of all amendments, which Django calls a QuerySet:

`>>> Amendment.objects.all()`

`<QuerySet [<Amendment: First Amendment>, <Amendment: Second Amendment>]>`

Let's close out the shell with Ctrl+C

## Show first data on our website
### Update the view
In api/views.py, we need to pass the context (model data) to the template. Then we can use the list of amendments in the template. We get the amendments using a Queryset, like we did in the shell, and then assign it to a dict with the key 'amendments':
```python
    def home(request):
        amendments = Amendment.objects.all()
        return render(request, 'home.html', context={'amendments': amendments})
```
### Update the home page template to show the amendment
In api/templates/home.html, we can now use the amendments in the template. We use the Django template language to loop over the amendments and show the title and date:
```html
<h2>Amendments</h2>
<ol>
    {% for item in amendments %}
        <li>{{ item.title }}: {{ item.date }}</li>
    {% endfor %}
</ol>
```

### Run the server and see the changes
`python manage.py runserver`
You should now see the amendments on the home page!

## Add the API (Django REST Framework)
### Settings configuration
In settings.py:
Add 'rest_framework' to INSTALLED_APPS
Add a new settings variable (see the DRF docs for more info):

```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

### Create the serializer for the Amendment model
Make a new api/serializers.py file. This is where we define the serializer for the Amendment model. We can use a HyperlinkedModelSerializer to automatically generate the URLs for the amendments. We also need to import the Amendment model. All we need to do to serialize a model in most cases is to define the model and the fields we want to serialize; DRF will handle the rest. If you have more complex nested models, you can add `RelatedFields` to the serializer to handle those. See the [DRF docs](https://www.django-rest-framework.org/api-guide/relations/) for more info.
```python
from rest_framework import serializers
from api.models import Amendment

class AmendmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Amendment
        fields = ['date', 'text', 'title', 'id']
```

### Add the view for DRF
In api.views.py:
```python
from rest_framework import viewsets
from api.serializers import AmendmentSerializer
from api.models import Amendment

class AmendmentViewSet(viewsets.ModelViewSet):
    queryset = Amendment.objects.all() # we can sort and filter here too
    serializer_class = AmendmentSerializer
```
### Add the router
In urls.py:
```python
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'amendments', api_views.AmendmentViewSet, basename="Amendment")

url patterns:
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("api/", include(router.urls)),
```
### Run the server and see the changes
Head to http://localhost:8000/api/

### Create a superuser
Back on the CLI, you can create a superuse so you can POST amendments to the API endpoint, and also so you can log in to the Django admin site:
`python manage.py createsuperuser`

### Login on the API site
Head to http://localhost:8000/api/ and log in with your superuser credentials. You should see the API endpoint and the amendments.

### Create a third amendment
Head to http://localhost:8000/api/amendments and log in with your superuser credentials. There should be a form to create a new amendment. Create a third amendment.

### Use the Admin interface
We first need to register models in api/admin.py:
```python
from django.contrib import admin
from api.models import Amendment
@admin.register(Amendment)
class AmendmentAdmin(admin.ModelAdmin):
    pass
```
Now we can head to http://localhost:8000/admin/ and log in with our superuser credentials. We can see the amendments and edit them.

### Delete an amendment
Back on the CLI (`python manage.py shell`), we can delete an amendment:

`>>> from api.models import Amendment`

`>>> a = Amendment.objects.get(id=3)`

`>>> a.delete()`

## Get the amendments with requests
`>>> import requests`

`>>> r = requests.get("http://localhost:8000/api/amendments/")`

`>>> r.status_code`

` 200`

`>>> amendments = r.json()` # use the json() method to get the JSON data

`>>> amendments`

We get back a list of amendments:

`[{'date': '1791-12-15', 'text': 'Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances.', 'title': 'First Amendment', 'id': 1}, {'date': '1791-12-15', 'text': 'A well regulated Militia, being necessary to the security of a free State, the right of the people to keep and bear Arms, shall not be infringed.', 'title': 'Second Amendment', 'id': 2}]`

We can access them with standard Python methods:

`>>> amendments[0]["title"]`

`'First Amendment'`
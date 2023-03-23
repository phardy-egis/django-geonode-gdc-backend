# django-geonode-gdc-backend
## About gdc-backend
`gdc` (GDC) stands for Geo-Spatial Data Catalogue. It is a Django app for Geonode that facilitates the data browsing and visualisation from Geonode. This repo contains the `backend` django API for GDC. The front-end REACT app is hosted int the [gdc-frontend](https://github.com/phardy-egis/django-geonode-gdc-frontend) repository.

It is released under GNU-GPL licence version 3.

Detailed documentation is in the "docs" directory.

## Add Django app. to Geonode setup
### Manual install
Here below are listed the instruction for install:

1. If you are using `docker`, stop services

    ```console
    docker-compose down
    ```

2. Add "gdc" to your INSTALLED_APPS by adding the following lines at the end of `./geonode/settings.py` file:

    ```python
    # Addition of gdc app
    INSTALLED_APPS += ('geonode.gdc',)
    ```

3. Include the gdc URLconf in `./geonode/urls.py` file like this:

    ```python
    if "geonode.gdc" in settings.INSTALLED_APPS:
        urlpatterns += [  # '',
            url(r'^gdc/', include('geonode.gdc.urls')),
        ]
    ```

4. Move `gdc` folder inside `./geonode` django project folder:


5. If you are using `docker`, rebuild geonode and restart services (this may stop the web site for a while):

    ```console
    docker-compose down && docker-compose build && docker-compose up -d
    ```

6. Once geonode has restarted, authneticated users with admins permissions can reach the endpoints under `/gdc/api` to search for datasets.

7. `gdc-backend` comes with [gdc-frontend](https://github.com/phardy-egis/django-geonode-gdc-frontend). A [gdc-frontend](https://github.com/phardy-egis/django-geonode-gdc-frontend) production build should be served to make the interface available for users.

### Example setup

You can find an example of geonode setup with GDC app in this repo: [django-geonode-dev](https://github.com/phardy-egis/django-geonode-dev.git). 
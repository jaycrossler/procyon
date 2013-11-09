Procyon
=======


Startup steps:

    Install XCode, update to latest, From Preferences->Downloads, install command line tools (or will get clang errors)

    sudo easy_install pip
    Download Postgres.app
    cd ~/Sites
    pip install virtualenv
    virtualenv stardev
    add to: ~/.bash_login:
        export PATH=/Library/Frameworks/Python.framework/Versions/Current/bin:$PATH
        export PGHOST=localhost
        source ~/Sites/stardev/bin/activate

    pip install psycopg2
    pip install numpy
    brew install postgis
    brew install gdal
    brew install libgeoip

    pip install virtualenv
    virtualenv stardev
    source stardev/bin/activate
    pip install Django==1.5.5
    pip install Paver

    NOTES: Created the page using pinax template:
    django-admin.py startproject --template=https://github.com/pinax/pinax-project-account/zipball/master procyon
    In admin menu, change site name with siteid = 1
    NOTE: add custom pavement.py, and update requirements.txt

    After everything is configured, run these to set up page:

    paver install_dependencies
    paver createdb
    python manage.py createsuperuser
    paver create_db_user
    paver sync

    # Import star information (update with proper file locations and counts)
    paver install_dev_fixtures
    paver start


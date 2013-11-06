Procyon, built upon pinax-project-account
=====================


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
    pip install Django==1.4.5
    django-admin.py startproject --template=https://github.com/pinax/pinax-project-account/zipball/master procyon

    pip install Paver
    add custom pavement.py
    paver install_dependencies
    paver createdb
    python manage.py createsuperuser
    paver create_db_user
    paver install_dev_fixtures
    paver sync
    paver start

    In admin menu, change site name with siteid = 1

Procyon
=======


Startup steps: (about 1 hour total)

    Install XCode, update to latest, From Preferences->Downloads, install command line tools (or will get clang errors)

    (open terminal window)
    sudo easy_install pip
    Download Postgres.app (google it. After installing, run it - should see an Elephant on the toolbar)
    cd ~/Sites
    sudo pip install virtualenv
    virtualenv stardev
    add to: ~/.bash_login:
        export PATH=/Applications/Postgres93.app/Contents/MacOS/bin:/Library/Frameworks/Python.framework/Versions/Current/bin:$PATH
        export PGHOST=localhost
        export LDFLAGS="-L/usr/X11/lib"
        export CFLAGS="-I/usr/X11/include -I/usr/X11/include/freetype2 -I/usr/X11/include/libpng12"

        source ~/Sites/stardev/bin/activate
    (close terminal, open new one)

    pip install psycopg2
    pip install numpy
    install homebrew (from terminal):
        ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"

    brew install freetype
    brew install postgis
    brew install gdal (probably already installed)
    brew install libgeoip

    pip install Paver

    paver install_dependencies
    paver createdb
    paver create_db_user
    paver sync
    python manage.py createsuperuser

    # Import star information (update with proper file locations and counts)
    paver install_dev_fixtures
    paver start


Making new Star Systems
=======================

Currently, you can build new "model stars" that extend the base star information by hitting:
    http://127.0.0.1:8000/maker/task_colors/
You might want to rewrite the "model" data with:
    http://127.0.0.1:8000/maker/task_colors/True

    TODO - this needs to be turned into a background task, as 10k items takes 2 minutes or so.


Notes on Project Config
=======================
Created the page using pinax template:
    django-admin.py startproject --template=https://github.com/pinax/pinax-project-account/zipball/master procyon
    In admin menu, changed site name with siteid = 1

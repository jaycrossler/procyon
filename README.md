Procyon
=======

Procyon is both a Star System search tool as well as a Star System simulator. It's originally loaded with 120,000 of the "most interesting" stars, but can have other databases loaded as well. It uses Postgres and PostGIS for quick "geospatial" searching of stars (as well as caching results for quicker lookups).  In addition, the starsystemmaker module simulates details about stars and planetary systems based on best guesses.  All of this information is available as JSON/JSONP data requests to make details sharable.

![alt tag](https://raw.github.com/jaycrossler/procyon/master/procyon/doc/doc_search_screen.png)

API
===

    JSON of real star data (for star ID # 70667, Proxima Centauri):
    http://127.0.0.1:8000/stars/star/70667

    JSONP of real star data:
    http://127.0.0.1:8000/stars/star/70667?callback=myFunction

    JSON of generated star data, along with nearest stars:
    http://127.0.0.1:8000/maker/star/70667

    JSONP of generated star data:
    http://127.0.0.1:8000/maker/star/70667



Installation
============

Startup steps: (about 1 hour total)

    For older macs, Install XCode, update to latest, From Preferences->Downloads, install command line tools (or will get clang errors)

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


Notes on Project Config
=======================
Created the page using pinax template:
    django-admin.py startproject --template=https://github.com/pinax/pinax-project-account/zipball/master procyon
    In admin menu, changed site name with siteid = 1

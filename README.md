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
    paver install_dev_fixtures
    paver sync

    Import star information (update with propoer file locations and counts):
        psql -d procyon -c "COPY starcatalog_star FROM '/Users/jay/Sites/procyon/fixtures/hygxyz.csv' DELIMITER ',' CSV header;"
        psql -d procyon -c "alter sequence starcatalog_star_id_seq restart with 119618;"
        psql -d procyon -c "COPY starcatalog_planet FROM '/Users/jay/Sites/procyon/fixtures/exoplanets.csv' DELIMITER ',' CSV header;"
        psql -d procyon -c "alter sequence starcatalog_planet_id_seq restart with 756;"
        psql -d procyon -c "COPY starcatalog_starpossiblyhabitable FROM '/Users/jay/Sites/procyon/fixtures/HabHYG_extracted.csv' DELIMITER ',' CSV header;"
        psql -d procyon -c "alter sequence starcatalog_planet_id_seq restart with 17132;"



    paver start


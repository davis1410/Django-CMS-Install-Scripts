import os
import sys
import webbrowser
import MySQLdb as mdb

sites_path = "/Users/bdavis/Sites"

def create_django_project(site_name, project_name, root_pswd, prj_pswd, env_name):

    #create mysql database and user
    print "creating mysql database..."
    db = mdb.connect(host="localhost", user="root", passwd=root_pswd)
    
    cur = db.cursor()
    cur.execute("CREATE DATABASE %s_db" % project_name)
    cur.execute("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s'" % (project_name, prj_pswd))
    cur.execute("GRANT ALL ON %s_db.* TO '%s'@'localhost'" % (project_name, project_name))
    
    db.close()
    print "done"
    
    #create site directory
    print "creating directory..."
    os.makedirs("%s/%s" % (sites_path, site_name))
    print "done"
    
    #create virtual environment
    print "creating virtual environment..."
    os.system("virtualenv %s/%s/%s --no-site-packages" % (sites_path, site_name, env_name))
    print "done"
    
    #activate virtual environment
    print "activating virtual environment..."
    activate_venv = "%s/%s/%s/bin/activate_this.py" % (sites_path, site_name, env_name)
    execfile(activate_venv, dict(__file__=activate_venv))
    print "done"
    
    #install mysql-python
    print "installing mysql-python..."
    os.system("pip install mysql-python")
    print "done"
    
    #install djangocms-installer
    print "installing djangocms-installer..."
    os.system("pip install djangocms-installer")
    print "done"
    
    #run djangocms-installer
    print "running django-cms installer..."
    project_path = "%s/%s/%s"  % (sites_path, site_name, project_name)
    os.system("djangocms -p %s %s" % (project_path, project_name))
    
    #make manage.py executable
    os.system("chmod +x %s/manage.py" % project_path)
    
    #migrate database
    print "migrating database..."
    os.system("%s/manage.py migrate" % project_path)
    
    #launch in brackets and web browser
    url = "http://127.0.0.1:8000"
    webbrowser.open(url, new=2)
    os.system("brackets %s" % project_path)
    os.system("brackets %s/%s/settings.py" % (project_path, project_name))
    
    #start debug server
    print "starting the debug server..."
    os.system("%s/manage.py runserver" % project_path)
    
try:
    site_name = sys.argv[1]
    project_name = sys.argv[2]
    root_pswd = sys.argv[3]
    prj_pswd = sys.argv[4]
    env_name = "env_%s" % project_name
    
    create_django_project(site_name, project_name, root_pswd, prj_pswd, env_name)
    
except IndexError:
    print "please provide a site name, project name, mysql root user password, and mysql project user password"
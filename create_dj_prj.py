import os
import sys
import webbrowser

def create_django_project(cwd, project_name, env_name):
    
    #create site directory
    print "creating directory..."
    os.makedirs("%s/%s" % (cwd, project_name))
    print "done"
    
    #create virtual environment
    print "creating virtual environment..."
    os.system("virtualenv %s/%s/%s --no-site-packages" % (cwd, project_name, env_name))
    print "done"
    
    #activate virtual environment
    print "activating virtual environment..."
    activate_venv = "%s/%s/%s/bin/activate_this.py" % (cwd, project_name, env_name)
    execfile(activate_venv, dict(__file__=activate_venv))
    print "done"
    
    #install djangocms-installer
    print "installing djangocms-installer..."
    os.system("pip install djangocms-installer")
    print "done"
    
    #run djangocms-installer
    print "running django-cms installer..."
    project_path = "%s/%s/%s"  % (cwd, project_name, project_name)
    os.system("djangocms -w -p %s %s" % (project_path, project_name))
    
    #make manage.py executable
    os.system("chmod +x %s/manage.py" % project_path)
    
try:
    cwd = os.getcwd()
    project_name = sys.argv[1]
    env_name = "env_%s" % project_name
    
    create_django_project(cwd, project_name, env_name)
    
except IndexError:
    print "please provide a project name"
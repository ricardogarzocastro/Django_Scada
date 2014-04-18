#Django_Scada


This a **SCADA Django web application** for automation processes.

##Table of contents:

1. Project description
2. File directory description
3. Installation and usage
4. Contact information


###1. Project description

This my Bachelor Thesis project for the University of Zaragoza. The goal was to build a SCADA that would:
  1. Provide control operations over any brand of PLC
  2. Remote access to the control platform

These requirements were met by developing a **Python web application**, with **Django** and **Bootstrap** as frameworks, that is allocated in a **Apache** server with **WSGI** technology and that is capable of meeting **SCADA** standards through **OPC** communicaiton.

###2. File directory description

The file directory description is as follows: 
  1. **http.conf**: This is the Apache configuration file. Feel free to use it as reference.
  2. **django_scada**: This folder contains the Python files, static files and databases for the Django Scada application.
    3. apache: Static files folder
    4. celerybeat-schedule: config file for the Celerby Beat Cron Manager
    5. django_admin_bootstrapped: Administration panel for this Django application comes with bootstrap theme.
    6. django_scada: Folder with the necessary files for a Django project
    7. variables: Django application folder for the SCADA











5-line code snippet on how its used (if it's a library)
configuration instructions
instructions to install, configure, and to run the programs

copyright and licensing information (or "Read LICENSE")

list of authors or "Read AUTHORS"
instructions to submit bugs, feature requests, submit patches, join mailing list, get announcements, or join the user or dev community in other forms
other contact info (email address, website, company name, address, etc)


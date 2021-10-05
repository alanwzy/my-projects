

### Project Umbrella
### Team: TA42-Lemon Lemonade

# Introduction
This a website that provides information on Sunlight Proection.

# System Architecture:

The Front-End of our website is built using ASP.NET with CSHTML, Javascript and C#.

The Back-End of our website is built using Python 3.

Both the Front-End and Back-End parts are hosted using Microsoft Azure.

## Back-End system

The main Back-End system is run by the app.py file, which initiates a Flask web application.

The uvr.py and data_wrangle.py files do the job of data pre-processing and database initialization.

Folders, such as hospitals, protectors, or Quiz contains CSV files that store the raw data.

The testing folder stores unit testing scripts.

The following Python packages need to be installed for the operation of the Back-End system:
```
Flask==2.0.1
mysql-connector-python==8.0.26
requests==2.26.0
simplejson==3.17.4
pandas==1.1.5
Flask-Cors==3.0.10
```

## Front-End system

The following packages need to be installed for the operation of the Front-End system:
```
Antlr==3.5.0.2
bootstra==5.1.0
jQuery==Version 3.6.0
jQuery.Validation==1.19.3
Microsoft.AspNet.Mvc==5.2.7
Microsoft.AspNet.Razor==3.2.7
Microsoft.AspNet.Web.Optimizatio==1.1.3
Microsoft.AspNet.WebPages==3.2.7
Microsoft.CodeDom.Providers.DotNetComplierPlatform==3.6.0
Microsoft.jQuery.Unobstrusive.Ajax==3.2.6
Microsoft.jQuery.Unobstrusive.Validation==3.2.12
Microsoft.Web.Infrastructure==1.0.0
Modernizr==2.8.3 
Newtonsoft.Json==13.0.1
WebGrease==1.6.0
```

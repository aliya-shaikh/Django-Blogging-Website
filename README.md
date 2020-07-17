# Awesome-Blog
 This a Blogging Website and my first project which i have created using django, There is all functionality in it as i remember and on Comment section i am still working and when i will done with this will update the file. It is completely working now.
#REQUIREMENTS : 
Python version 3.6 or higher, Subllime Text (or any other IDE you like), Django Lates Version
To download Django : pip install django
To start the project use the command: django-admin startproject myblog (you can give any name to your project and you can create wherever you want)
Go to that folder : cd myblog
To Run The Server use the command : python manage.py runserver
To stop it use: Ctrl C
To Create subapp : python manage.py startapp blog(you can give any name & You can create as much app as you want in myblog)
To access to Admin Panel you need a super user.
To create a super user : python manage.py createsuperuser (give username,email,and password)]
To see admin panel Go in the browser and write : localhost:8000/admin

#Whenver we make changes in model.py we must have to run these 2 Command.
 python manage.py makemigrations
 python manage.py migarte

# I have use crispy forms so that my forms will look more classic and formal
To install crispy : pip install django-crispy-forms
# To use images in our project we need PIL to install it use : pip install pillow

# For security Purpose so no one can access to my email and password i set them as environment variable while reseting the passwords:
in Settings.py i have used EMAIL_HOST_USER = os.environ.get('EMAIL_USER) and same for the password too (You can write your email id and password if you are using only for yourself esle put the detail in environament variable)

# To create environment Variable You can watch the video of Corey Schafer on Youtube
# and if your gmail is not a 2 way authenticated then what you have to do is
  Go to Google -> Search For Google Apps Paasword -> Click on the link (App Password) -> Sign In -> Google Account and Allow access to less secure app -> Save 

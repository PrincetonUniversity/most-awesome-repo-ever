CharterWebsite
==============

Princeton Charter Club's Grand Old Website

### How to run the server:

Type this into ther terminal:

    python manage.py runserver

Then navigate to the URL it gives you, and you should be accessing the site!


Run these commands when you first download the repo:
---

- This sets up a directory to store executables of files unique to this project. This way, if this project requires Django 1.7, but your computer actually has Django 1.8 installed, turning on the virtual env (using "source ..." below) will force your computer to use Django 1.7.

        virtualenv venv

- Turn on the virtual environment:

        source venv/bin/activate

This changes the location of all of the dependencies to be ./venv/bin/activate instead of /usr/local/bin. All of the executable files needed to run this website are in that folder already, and this allows all of us to test the website with the same installed version of software.

If you don't run this command, you will likely be missing a bunch of software. Sorry :(

- Install the required packages:

        pip install django-toolbelt

Make sure you install django 1.7.4 (otherwise this won't work):

        pip install django==1.7.4

- Install the CAS authentication:

        cd django-cas
        python setup.py install
        cd ..

This installs the authentication package needed for Django onto your system.

- Install [Postgres](http://postgresapp.com/)!

This way, when we start making calls to the database and you try to test the changes locally on your computer, you'll still be able to.

Open 'psql' and run:

        CREATE ROLE admin LOGIN PASSWORD 'kernighan';
        CREATE DATABASE chartermembers;

This creates a role that can login to the database `chartermembers`. You will
use this below. See the [video](https://docs.google.com/a/princeton.edu/file/d/0B6HetodYPhDwX3NtTlVQc19YQ2s/edit).

- Set your environment variables by obtaining a `localEnv.sh` file from the tech chair, and run it by using the command:

		source localEnv.sh

- Install pillow:

        pip install pillow

- Setup the database according to Django's specifications.

        python manage.py migrate
        python manage.py syncdb

If you run into an error stating something along the lines of `ImportError: No module named blank` (the modules are `jquery, dajax, dajaxice, crispy_forms, storages, jsmin, ldap, boto`), try running `pip install django-blank` (replacing blank with the module that can't be found) 

**NB: ldap's module is `django-auth-ldap` not `django-ldap`**

It will ask you to create an admin. Use the login credentials in
`charterclub/local_settings.py`. Say yes, and use the following:

        Username: admin
        Password: kernighan

- Run it and see if everything works!

        python manage.py runserver

Then navigate to http://127.0.0.1:8000/, and if you see a success page, then you're good!

- Once you're done developing, exit your virtual environment with:

        deactivate

Yay! Questions?

Git Protocols
---

Congrats! You've cloned the repo. Here's what you want to do if you want to submit a change:

**DON'T PUSH TO MASTER, CREATE A BRANCH INSTEAD**

- Create a new branch to work with by using 

        git checkout -b branch_name

- Edit your files.
- Add all files to the staging area. If you don't add files to the staging area, git won't recognize them, and won't share them with everyone else.

        git add *your_changed_files*

- Commit your changes. Bundle all of your changes into one "commit," which is tagged with a commit message and sent to the remote repo.

        git commit -m "Descriptive message"

- Update with what everyone else is doing! You want to stay updated with all of the changes everyone else does, so switch to master, update, and switch back to your branch:

        git checkout master
        git pull
        git checkout branch_name
        git rebase master
        
This will make sure that you are in sync with the live master

- If you're done testing (and **ONLY** if you're don't testing), share your changes with everyone else.

        git push origin branch_name

This will create a new branch on the origin repo

- On the branch page on github, open a new pull request for your branch. Tag people in it so that they can see and comment on it before pushing to master. Once you receive enough approval, close the pull request to merge into master!


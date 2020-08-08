# Table of Contents
- 1: Workflow
- 2: File Structure
- 3: Specific Commands

_____
# 1: Workflow

1. Start virtual environment
2. Create/ switch to branch for the feature you're working on
3. Write your code
4. Freeze your dependencies in virtualenv
5. Push your feature branch to remote
6. Make a pull request to master
7. Stop virtual environment
_____
# 2: File Structure

Highlight of most relevant files:
requirements.txt: contains a list of package dependencies. Always remember to load it and update it with virtual environment!!

web/blueprints/* : All routing and controller logic is here.
web/static/* : Contains static files. Ex: CSS, JS, images
web/templates/* : View templates are here. So all HTML files
models.py : Define models (database tables) here.
serve.py : Where the main application is defined.
_____
# 3: Specific Commands
# Welcome to CS162 Final Project

## Using git in this repository

### First time Set up

First, create a clone of this repository in your local environment. The

    $ git clone https://github.com/minerva-schools/cs162-community

Create a branch and check out a new branch for your work

    $ git checkout master
    $ git branch newBranchName
    $ git checkout newBranchName

### Re-initailizing local environment with changes in Github

First fetch all new changes

    $git fetch

Next create a new branch locally pulling from the branch on Github.

    $ git branch branch_name_on_local_environment origin/branch_name_on_github

Then, switch to the branch you are testing

    $git checkout branch_name_on_local_environment

#### Working locally with git

Look at your untracked files by running the following

    $ git status

When done modifying a file, add the file to the stage

    $ git add  <filename> #add a particular file
    $ git add . #add all files

Make a commit once you have made a substantial change across one or many files. This extends your branch by one commit

    $ git commit -m "new message"

#### Checking your history and reverting to an old branch

Check your log

    $ git log

It should show a list of all commits.

```bash

commit 10685f1108b2ea0c9a2144b7fe8d9aecba423c69 (HEAD -> master, origin/master, origin/HEAD)
Author: Amal <mamalanand3@gmail.com>
Date:   Mon Feb 24 15:22:13 2020 -0300

    Modified README.md to include Git&Github instructions, and instructions on saving modifications to virtual environment

commit d443ed713c1d2094444cf84bf9ff0bcf773eae09
Author: Philip Sterne <sterne@gmail.com>
Date:   Fri Jan 31 10:32:22 2020 +0200
```

Select the commit you want to undo and revert using the commit id

    $ git revert <commitID>

To reset to a particular commit use the git commant. The --hard flag resets the working directory, and the --soft flag resets only commits

    $ git reset --hard <commit hash or id>

To store the state of your directory before, use git stash to keep a copy of work done.

    $ git stash

It is possible to delete saved information on the remote repository.
But this is dangerous (deleting forever) and rarely defensible.

If there is a particular commit you want to check out, you can checkout that commit ID. Note this does not support modifying the files at the given state

    $ git checkout <commitID>


#### Creating a pull request to push your local changes to github

First, update your local repository with the latest upstream changes

    $ git fetch

Merge your branch with the new master branch , and solve any merge conflicts where code you wrote conflicts with code others wrote

    $git merge branchName master

Once all merge conflicts are resolved, push your changes to the remote on github. It is important you are on your local branch, not on the master branch cloned from the repository.

    $git push origin branchName

### Testing pull requests

Open up the `.git/config` file and add a new line under `[remote "origin"]`:

```
fetch = +refs/pull/*/head:refs/pull/origin/*
```

Now you can fetch and checkout any pull request so that you can test them:

```shell
# Fetch all pull request branches
git fetch origin

# Checkout out a given pull request branch based on its number
git checkout -b 999 pull/origin/999
```

These steps are read only to test the pull request, you will need to approve the pull request on github

## Run Virtual Environment

Virtual environment is a key component in ensuring that the application is configured in the right environment

##### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

Pip3 is installed with Python3

##### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

##### Usage
Creation of virtualenv:

    $ virtualenv -p python3 .venv

If the above code does not work, you could also do

    $ python3 -m venv .venv

To activate the virtualenv:

    $ source .venv/bin/activate

Or, if you are **using Windows** - [reference source:](https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate)

    $ .venv\Scripts\activate

Install dependencies in virtual environment:

    $ pip3 install -r requirements.txt

If you had installed new packages in the virtual environment that are required for the app to run, save the changes to requirements.txt

    $ pip freeze > requirements.txt

To deactivate the virtualenv (after you finished working):

    $ deactivate



## Environment Variables

All environment variables are stored within the `.env` file and loaded with dotenv package.

**Never** commit your local settings to the Github repository!

## Getting the Google Client ID and secret


1) Open the Google API Console Credentials page at https://console.developers.google.com/apis/credentials
2) Click Select a project, then NEW PROJECT, and enter a name for the project, and optionally, edit the provided project ID. Click Create.
3) On the Credentials page, select Create credentials, then OAuth client ID.
4) You may be prompted to set a product name on the Consent screen; if so, click Configure consent screen, supply the requested information, and click Save to return to the Credentials screen.
5) Select Web Application for the Application Type. Follow the instructions to enter JavaScript origins, redirect URIs, or both.
Click Create.
6) On the page that appears, copy the client ID and client secret to your clipboard, as you will need them when you configure your client library

Alternatively, you may email the author at amal@minerva.kgi.edu for the client ID and secret

## Run Application

Start the server by running:

The path to your ssl key and cert are most likely:
<path to project folder>/key.pem

!! Would recommend setting these variables in your bash profile if you intend on accessing this multiple times
    $ export FLASK_ENV=development
    $ export FLASK_APP=web
    $ export GOOGLE_CLIENT_ID=<<client_id>
    $ export GOOGLE_CLIENT_SECRET=<<client_secret>>
    $ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    $ export KEY_PATH=<<path to your ssl key>>
    $ export CERT_PATH=<<path to your ssl cert>>
    $ export FLASK_RUN_CERT=adhoc
    $ export DATABASE_URL='sqlite:///web.db'
    $ python web/serve.py

## Unit Tests
To run the unit tests use the following commands:

    $ python3 -m venv venv_unit
    $ source venv_unit/bin/activate
    $ pip install -r requirements-unit.txt
    $ export SQLALCHEMY_DATABASE_URI='sqlite:///web.db'
    $ pytest unit_test

## Integration Tests
Start by running the web server in a separate terminal.

Now run the integration tests using the following commands:

    $ python3 -m venv venv_integration
    $ source venv_integration/bin/activate
    $ pip3 install -r requirements-integration.txt
    $ pytest integration_test

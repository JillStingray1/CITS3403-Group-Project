# CITS3403-Group-Project Meeting Manager

  ## Description

  This is a web app used to schedule meetings with other users. The frontend of the website is used to create new activities and view activities that involve you. The backend stores activity data for each user, and analyses the data to prevent clashing activies being added.
  
  ## Students

  |UWA ID|Name|Github Username|
  |---|---|---|
  |23865869|Jerry Hou|JillStingray1|
  |22275812|Tom Jia|TomJia98|
  |24091054|Choo Yan Ling|Dragonicle|
  |23717085|Tylen Chetty|TDC350

## Table of Contents

* [Purpose](#purpose)
* [Tech Stack](#tech-stack)
* [Directory Structure](#directory-structure)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the App](#running-the-app)
* [Key Flows](#key-flows)
* [Testing](#testing)
---

## Purpose

Meeting Manager helps organisers create meetings over a date range, invite participants, collect 15‑minute availability slots, and automatically surface the best contiguous windows where the most people are free.

## Usage
To use the site, create and account or log in from the pages linked on the index.

You can then create meetings using the New Activity button on the main menu, and select your availability by clicking on the name of the meeting on the main menu.

If you wish to share the meeting, give the person that you'd like to share with the share code displayed on the main menu, and they should input that in the share code dropdown. You can then confirm the details for the shared meeting and add yourself to it. They can also fill in their own availability.

The app will automatically calculate the best time based on the submitted availabilities. If you'd like more details, you can click on the suggested time to view a bar chart ranking of the top 10 times.

## App design
The app is made up of multiple routes that make up the above pages, the app.py file contains the route for the index page, which contains a short guide on how to use the app.

The `/user/login`, `user/signup` and `/user/logout` routes are in user routes. These pages use flask forms to recieve and validate user inputs, and hashes the password using flask's built in Bcrypt library, all flask forms in the project require a CSRF token to meet the security requirements. The login page will also check if you have an active user session, and automatically log you in if you do.

The bulk of the logic for the website is in the meeting routes. Creating a meeting is also done using flask forms in the `/meeting/create` field, which commits the meeting to the database. 

The `/main-menu` route serves 2 purposes, it list all of a user's meetings, which is done by querying the database in the backend, and it allows you to join meetings by sharecode, this joining functionality is done via flask forms. There is also some AJAX to make a preview of the meeting by getting the meeting's details through the `/meeting/code/<share_code>` route. 

The availability selection is the most complicated part of the site. The template is rendered by the `/availability-selection/<meeting_id>` route, which takes in a meeting ID and sets it to the user's current session. Then, we use an GET request to generate all the timeslots for the meeting, through the `/meeting` route, this allows the user to save timeslots, and edit them later. Clicking on the timeslots sends POST requests to the `/meeting/timeslot` route, which adds the user to timeslots, which also automatically updates the suggested time for the meeting

The `/analysis/<meeting_id>` calculates the top 10 best times, instead of just the best time that availability selection, and we display that on a graph using Chart.js.
### Directory Structure

```
├── app.py                # Entry-point: Flask app, loads blueprints
├── .env                  # Secret keys & DB URI
├── models/               # SQLAlchemy models
│   ├── User.py           # user accounts
│   ├── Meeting.py        # meeting metadata
│   ├── Timeslot.py       # individual 15-min slots
│   ├── Association.py    # many-to-many tables
│   └── …                 
├── routes/               # Flask blueprints
│   ├── user_routes.py    # signup, login, profile
│   ├── meeting_routes.py # meeting creation, timeslot APIs, stats & analysis page
│   ├── routes.py
│   └── …                 
├── forms/                # Flask-WTF forms
│   ├── sign_up.py        
│   ├── login.py          
│   ├── activity_create.py
│   └── …                 
├── static/               # Client assets
│   ├── stylesheet/       # CSS files (common.css, mainmenu.css, analysis.css…)
│   ├── javascript/       # analysis.js, calendar.js, meeting-popup.js…
│   └── media/            # logos, icons, videos
├── templates/            # Jinja2 templates
│   ├── index.html        
│   ├── login.html        
│   ├── main-menu.html    
│   ├── activity-create.html
│   ├── analysis.html     
│   └── …                 
├── tools
│   ├── tools.py          # Business-logic helpers (eg. best-slot computation)
│   ├── config.py         # Stores various app configurations
│   └── extensions.py     # Initializes the database before creation
├── middleware/           # @secure decorator for login-required
├── migrations/           # Alembic DB migrations
├── test/                 # pytest test modules
└── requirements.txt      # project dependencies
```
### Key Routes





## Starting the App

1. **Clone the repo**

   Either clone using URL obtained from the green code button
   ```bash
   git clone <repository-url>
   cd CITS3403-Group-Project
   ```
   Or download an .zip archive of the repository on github

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Copy the example env file**

   ```bash
   cp .env.example .env
   ```

5. **Edit `.env`** and set:

   ```ini
   SECRET_KEY="your_secret_key_here"
   SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
   ```
6. Run the app
   ```bash
   flask run                 # listens on http://localhost:5000
   ```

Visit `http://localhost:5000/` to see the landing page.





## Testing

To run unit tests, follow the instructions above to install dependencies, and then run the following command.
```bash
python -m unittest
```

For Selenium testing, the Process constructor used to spawn the webserver doesn't work properly on windows, and will crash with `OSError: \[WinError 6\] The handle is invalid`.

Thus, to run the selenium tests located in `test_selenium.py`, please make sure you are running on Linux, with a Firefox binary installed, and not as a flatpak/snap. If you are on Ubuntu, where `apt` will automatically install Firefox as a snap, see [these instructions](https://askubuntu.com/questions/1399383/how-to-install-firefox-as-a-traditional-deb-package-without-snap-in-ubuntu-22).



## References
Main menu video obtained from https://www.pexels.com/video/man-people-woman-desk-7687999/

AI tools were used to generate the following parts of the project:
- availability-selection.js
- common.css
- main-menu.css
- landing.css
- analysis.css
- analysis.html

The details on which parts were generated by AI can be located as a comment in the top of each file.

*Thank you Happy scheduling!*

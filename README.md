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

---

## Tech Stack

* **Backend**

  * Flask (routing & templating)
  * Flask-SQLAlchemy (ORM)
  * Flask-WTF (forms & CSRF)
  * Flask-Bcrypt (password hashing)
  * PostgreSQL (production) / SQLite (development)

* **Frontend**

  * Jinja2 templates
  * Shared `common.css` + page‑specific styles in `static/stylesheet/`
  * Vanilla JavaScript + Chart.js for dynamic charts

* **Utilities**

  * `tools.py`: helper functions for timeslot computations and best‑window selection

* **Testing**

  * pytest for route, model, and analysis logic tests

---

## Directory Structure

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

---

## Installation

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

---

## Configuration

1. **Copy the example env file**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and set:

   ```ini
   SECRET_KEY="your_secret_key_here"
   SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
   ```

---

## Running the App

```bash
export FLASK_APP=app.py    # or set on Windows
export FLASK_ENV=development
flask run                 # listens on http://localhost:5000
```

Visit `http://localhost:5000/` to see the landing page.

---

## Key Routes

1. **User Signup & Login** (`/user/signup`, `/user/login`)
2. **Create Meeting** (`/meeting/create`)
3. **Join & Mark Availability**: Uses JS on `/avaiability-selection/<meeting_id>` to POST to `/meeting/timeslot`
4. **Stats Dashboard**: `/analysis` Renders a bar graph of best times

---

## Testing

To run unit tests, run the following command.
```bash
python -m unitest
```

For Selenium testing, the Process constructor used to spawn the webserver doesn't work properly on windows, and will crash with `OSError: \[WinError 6\] The handle is invalid`

Please make sure you are running on Linux, with a Firefox binary installed, and not as a flatpak/snap. If you are on Ubuntu, where `apt` will automatically install Firefox as a snap, see [these instructions](https://askubuntu.com/questions/1399383/how-to-install-firefox-as-a-traditional-deb-package-without-snap-in-ubuntu-22).



## References
Main menu video obtained from https://www.pexels.com/video/man-people-woman-desk-7687999/


---

*Thank you Happy scheduling!*

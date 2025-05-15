from flask import session, request, jsonify, redirect, url_for, render_template, flash
from models import User, Meeting, Timeslot
from tools.tools import (
    generate_share_code,
    format_meetings,
    get_num_unavailable_per_timeslot,
)
from middleware.middleware import secure
from forms import meetingCreationForm, ShareCodeForm
from models import association_table, Meeting, User

# TODO: add a migration to add a new column to the meeting table to store the current most effective timeslot. this should be calculated each time a timeslot is added or removed. change the add_to_timeslot function to update this column.


def get_timeslots(Meeting):
    """
    Gets all timeslots for a single meeting

    Args:
        Meeting (Meeting): A meeting from the database

    Returns:
        list[Timeslots]: A list of timeslots
    """
    timeslots = Meeting.timeslots
    timeslot_list = []

    for timeslot in timeslots:
        timeslot_list.append(
            {
                "id": timeslot.id,
                "order": timeslot.order,
                "unavailable_users": [user.username for user in timeslot.unavailable_users],
            }
        )
    return timeslot_list


def init_meeting_routes(app, db):
    # Create meetings page
    @app.route("/meeting/create", methods=["GET", "POST"])
    @secure
    def create_meeting():
        """
        Renders the meeting creation template and redirects to other menus
        """

        form = meetingCreationForm()
        if form.validate_on_submit():
            parsed_start_date = form.start_date.data
            parsed_end_date = form.end_date.data

            new_meeting = Meeting(
                start_date=parsed_start_date,
                end_date=parsed_end_date,
                meeting_length=form.meeting_length.data,
                meeting_name=form.meeting_name.data,
                meeting_description=form.meeting_description.data,
                share_code=generate_share_code(),
            )

            db.session.add(new_meeting)
            db.session.commit()
            new_meeting.users.append(User.query.get(session["user_id"]))

            amount_days = (parsed_end_date - parsed_start_date).days + 1
            for i in range(amount_days * 32):
                new_timeslot = Timeslot(order=i, meeting_id=new_meeting.id)
                db.session.add(new_timeslot)
                db.session.commit()

            session["meeting_id"] = new_meeting.id

            return redirect(
                url_for("availability_selection")
            )  # redirect to the date selection page after creating the meeting
        else:
            # If the form is not valid, render the form again with errors
            return render_template("activity-create.html", form=form)

    # routes related to main menu
    @app.route("/main-menu", methods=["GET", "POST"])
    @secure
    def main_menu():
        """
        Loads the main menu template, which has a list of user's meetings and
        handles sharing using share codes

        Returns:
            The rendered main menu template by default, or if there is an
            error. Reloads the page if sharing successful
        """
        meetings = Meeting.query.join(association_table).filter(association_table.c.user_id == session["user_id"]).all()
        current_activities, past_activities = format_meetings(meetings)
        form = ShareCodeForm()
        if form.validate_on_submit():
            user = User.query.get(session["user_id"])
            meeting = Meeting.query.filter_by(share_code=form.code.data).first()
            if not meeting or user in meeting.users:
                return render_template(
                    "main-menu.html",
                    created_activities=meetings,
                    form=form,
                    error="Something went wrong with the share code",
                )
            meeting.users.append(user)
            db.session.commit()
            return redirect(url_for("main_menu"))
        return render_template(
            "main-menu.html", created_activities=current_activities, past_activities=past_activities, form=form
        )

    @app.route("/meeting/code/<share_code>", methods=["GET"])
    @secure
    def get_meeting_by_code(share_code):
        """
        Get a meeting by Share code. Returns JSON with meeting details.
        This is used for ajax in the main menu
        """
        meeting = Meeting.query.filter_by(share_code=share_code).first()
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 403
        if User.query.get(session["user_id"]) in meeting.users:
            return jsonify({"error": "You are already in this meeting"}), 403
        return (
            jsonify(
                {
                    "start_date": meeting.start_date.strftime("%Y %B %d"),
                    "end_date": meeting.end_date.strftime("%Y %B %d"),
                    "meeting_length": meeting.meeting_length,
                    "meeting_name": meeting.meeting_name,
                    "meeting_description": meeting.meeting_description,
                }
            ),
            200,
        )

    # Analysis page route
    @app.route("/analysis/<int:meeting_id>")
    @secure
    def analysis_page(meeting_id: int):
        """
        Prints the analysis page based on the meeting id, this page is
        linked to from the main menu

        Args:
            meeting_id (int): The meeting Id for the graph we want to see

        Returns:
            Analysis page template if meeting exists and contains user, redirect
            back to main menu if not
        """
        meeting = Meeting.query.get(meeting_id)
        if meeting is None:
            redirect(url_for("main_menu"))
        user = User.query.get(session["user_id"])
        if user not in meeting.users:
            redirect(url_for("main_menu"))
        timeslots = get_timeslots(meeting)
        unavalibility_scores_list = list(get_num_unavailable_per_timeslot(timeslots, meeting.meeting_length).items())
        unavalibility_scores_list.sort(key=lambda x: x[1])
        top_scores = unavalibility_scores_list[:10]
        print(top_scores)

        if not meeting:
            flash("Please create or select a meeting first.", "warning")
            return redirect(url_for("main_menu"))

        # (optionally pre‐compute any stats server‐side here, or just let your JS fetch /meeting/stats)
        return render_template("analysis.html", meeting=meeting, top_scores=top_scores, start_date=meeting.start_date)

    # Availability selection routes
    @app.route("/availability-selection/<int:meeting_id>")
    @secure
    def availability_selection(meeting_id):
        """
        Renders the avaliability selection page for a meeting from its
        id

        Args:
            meeting_id (int): The meeting's id in the database
        """
        user = User.query.get(session["user_id"])
        meeting = Meeting.query.get(meeting_id)
        # prevents users from access meetings they are not in
        if meeting is None:
            return redirect(url_for("main_menu"))
        if user not in meeting.users:
            return redirect(url_for("main_menu"))

        session["meeting_id"] = meeting_id

        return render_template("availability-selection.html")

    @app.route("/meeting/timeslot", methods=["POST"])
    @secure
    def add_to_timeslot():
        """
        Add a user to a timeslot. Expects JSON as { timeslots: [{timeslot_id: int}] }
        """
        data = request.get_json()

        user = User.query.get(session["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        meeting = Meeting.query.get(session["meeting_id"])
        if user not in meeting.users:
            return jsonify({"error": "User not part of the meeting"}), 403

        timeslot_entries = data.get("timeslots", [])

        for entry in timeslot_entries:
            timeslot_id = entry.get("timeslot_id")
            timeslot = Timeslot.query.get(timeslot_id)
            if not timeslot:
                return jsonify({"error": f"Timeslot with ID {timeslot_id} not found"}), 404

            if user in timeslot.unavailable_users:
                timeslot.unavailable_users.remove(user)

            else:
                timeslot.unavailable_users.append(user)

        db.session.commit()

        timeslots = get_timeslots(meeting)

        slot_index_by_unavail = get_num_unavailable_per_timeslot(timeslots, meeting.meeting_length)
        best_order = min(
            slot_index_by_unavail, key=lambda k: slot_index_by_unavail[k]
        )  # get the order with the least amount of unavailable users in its window
        meeting.best_timeslot = best_order
        db.session.commit()

        return jsonify({"message": "User added to timeslot(s)"}), 200

    @app.route("/meeting", methods=["GET"])
    @secure
    def get_current_meeting():
        """
        Get the current meeting saved in session. Returns JSON with meeting details.
        """
        meeting = Meeting.query.get(session["meeting_id"])
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404

        timeslot_list = get_timeslots(meeting)

        best_timeslot = meeting.best_timeslot if meeting.best_timeslot else 0

        return (
            jsonify(
                {
                    "id": meeting.id,
                    "start_date": meeting.start_date,
                    "end_date": meeting.end_date,
                    "meeting_length": meeting.meeting_length,
                    "meeting_name": meeting.meeting_name,
                    "meeting_description": meeting.meeting_description,
                    "share_code": meeting.share_code,
                    "best_timeslot": best_timeslot,
                    "timeslots": timeslot_list,
                    "user_id": session["user_id"],
                    "username": session["username"],
                }
            ),
            200,
        )

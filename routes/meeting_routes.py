from flask import Flask, session, request, jsonify, redirect, url_for, render_template
from models.Models import User, Meeting, Timeslot
from tools import validate_username, validate_password, save_login_session, clear_login_session, generate_share_code
from middleware.middleware import secure
from datetime import date, datetime
from forms.activity_create import meetingCreationForm

    #TODO: add a migration to add a new column to the meeting table to store the current most effective timeslot. this should be calculated each time a timeslot is added or removed. change the add_to_timeslot function to update this column. 
    
def get_timeslots(Meeting):

    timeslots = Meeting.timeslots
    timeslot_list = []

    for timeslot in timeslots:
        timeslot_list.append({
            "id": timeslot.id,
            "order": timeslot.order,
            "unavailable_users": [user.username for user in timeslot.unavailable_users]
        })
    return timeslot_list
    


def init_meeting_routes(app, db):
    @app.route('/meeting/create', methods=["GET","POST"])
    @secure
    def create_meeting():
        """
        Create a new meeting. Expects JSON as { start_date: 'YYYY-MM-DD', end_date: 'YYYY-MM-DD',
        meeting_length: int%15=0, meeting_name: 'meeting_name', meeting_description: 'meeting_description' }
        """

        form = meetingCreationForm()
        if form.validate_on_submit():
            parsed_start_date = datetime.strptime(form.start_date.data, "%Y-%m-%d").date()
            parsed_end_date = datetime.strptime(form.end_date.data, "%Y-%m-%d").date()
        
        
            new_meeting = Meeting(start_date=parsed_start_date,
                            end_date=parsed_end_date,
                            meeting_length=form.meeting_length.data,
                            meeting_name=form.meeting_name.data,
                            meeting_description=form.meeting_description.data,
                            share_code=generate_share_code()
                            )
        
            db.session.add(new_meeting)
            db.session.commit()
            new_meeting.users.append(User.query.get(session['user_id']))


            amount_days = (parsed_end_date - parsed_start_date).days + 1
            for i in range(amount_days * 32):
                new_timeslot = Timeslot(order=i, meeting_id=new_meeting.id)
                db.session.add(new_timeslot)
                db.session.commit()
        
            session['meeting_id'] = new_meeting.id
            return redirect("/date-selection")  # redirect to the date selection page after creating the meeting
        return render_template("activity-create.html", form=form)
    
    @app.route('/meeting/all', methods=['GET'])
    @secure
    def get_all_meetings():
        """
        Get all current users meetings. Returns JSON with meeting details.
        """
        user = User.query.get(session['user_id'])
        user_meetings = user.meetings
        meeting_list = []
        for meeting in user_meetings:
            
            best_timeslot = meeting.best_timeslot if meeting.best_timeslot else 0
            meeting_list.append({
                "id": meeting.id,
                "start_date": meeting.start_date,
                "end_date": meeting.end_date,
                "meeting_length": meeting.meeting_length,
                "meeting_name": meeting.meeting_name,
                "meeting_description": meeting.meeting_description,
                "share_code": meeting.share_code,
                "best_timeslot": best_timeslot
              
            })
        
        return jsonify(meeting_list), 200
    
    @app.route('/meeting', methods=['GET'])
    @secure
    def get_current_meeting():
        """
        Get the current meeting saved in session. Returns JSON with meeting details.
        """
        meeting = Meeting.query.get(session['meeting_id'])
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        timeslot_list = get_timeslots(meeting)

        best_timeslot = meeting.best_timeslot if meeting.best_timeslot else 0

        return jsonify({
            "id": meeting.id,
            "start_date": meeting.start_date,
            "end_date": meeting.end_date,
            "meeting_length": meeting.meeting_length,
            "meeting_name": meeting.meeting_name,
            "meeting_description": meeting.meeting_description,
            "share_code": meeting.share_code,
            "best_timeslot": best_timeslot,
            "timeslots": timeslot_list
        }), 200
    
 
    @app.route('/meeting/<int:meeting_id>', methods=['GET'])
    @secure 
    def get_meeting(meeting_id):
        """
        Get a meeting by ID. Returns JSON with meeting details.
        """
        meeting = Meeting.query.get(meeting_id)
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        timeslot_list = get_timeslots(meeting)
        best_timeslot = meeting.best_timeslot if meeting.best_timeslot else 0

        return jsonify({
            "id": meeting.id,
            "start_date": meeting.start_date,
            "end_date": meeting.end_date,
            "meeting_length": meeting.meeting_length,
            "meeting_name": meeting.meeting_name,
            "meeting_description": meeting.meeting_description,
            "share_code": meeting.share_code,
            "best_timeslot": best_timeslot,
            "timeslots": timeslot_list
        }), 200
    
    @app.route('/meeting/timeslot', methods=['POST'])
    @secure
    def add_to_timeslot():
        """
        Add a user to a timeslot. Expects JSON as { timeslots: [{timeslot_id: int}] }
        """
        data = request.get_json()
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        meeting = Meeting.query.get(session['meeting_id'])
        if user not in meeting.users:
            return jsonify({"error": "User not part of the meeting"}), 403
        
        timeslot_entries = data.get("timeslots", [])

        for entry in timeslot_entries:
            timeslot_id = entry.get("timeslot_id")
            timeslot = Timeslot.query.get(timeslot_id)
    
            if not timeslot:
                return jsonify({"error": f"Timeslot with ID {timeslot_id} not found"}), 404

            timeslot.unavailable_users.append(user)

        db.session.commit()

        amount_timeslots_needed = meeting.meeting_length // 15

        timeslots = get_timeslots(meeting)
        sorted_timeslots = sorted(timeslots, key=lambda x: x["order"]) # sort the timeslots by order


        dict_order = {}

        for i in range(len(sorted_timeslots)):
            current_slot = sorted_timeslots[i]
            total_unavailable = 0

            for j in range(amount_timeslots_needed):
                if (i + j) < len(sorted_timeslots):
                    next_slot = sorted_timeslots[i + j]

                    total_unavailable += len(next_slot["unavailable_users"])
                else:
                    break
                 
            # Save the total sum into dict_order
            dict_order[current_slot["order"]] = total_unavailable

        best_order = min(dict_order, key=lambda k: dict_order[k]) # get the order with the least amount of unavailable users in its window
        meeting.best_timeslot = best_order
        db.session.commit()

        return jsonify({"message": "User added to timeslot(s)"}), 200
    

    @app.route('/meeting/code', methods=['POST'])
    @secure
    def join_meeting():
        """
        Join a meeting using a share code. Expects JSON as { share_code: 'share_code' }
        """
        data = request.get_json()
        share_code = data.get("share_code")
        
        meeting = Meeting.query.filter_by(share_code=share_code).first()
        
        if not meeting:
            return jsonify({"error": "Meeting not found"}), 404
        
        user = User.query.get(session['user_id'])
        
        if user in meeting.users:
            return jsonify({"error": "User already in meeting"}), 400
        
        meeting.users.append(user)
        db.session.commit()
        
        return jsonify({"message": "User added to meeting"}), 200
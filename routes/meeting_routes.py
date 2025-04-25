from flask import Flask, session, request, jsonify, redirect, url_for
from models.Models import User, Meeting, Timeslot
from tools import validate_username, validate_password, save_login_session, clear_login_session, generate_share_code
from middleware.middleware import secure
from datetime import date, datetime

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
    @app.route('/meeting', methods=['POST'])
    @secure
    def create_meeting():
        """
        Create a new meeting. Expects JSON as { start_date: 'YYYY-MM-DD', end_date: 'YYYY-MM-DD',
        meeting_length: int%15=0, meeting_name: 'meeting_name', meeting_description: 'meeting_description' }
        """
        data = request.get_json()
        print(data)
        parsed_start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%d").date()
        parsed_end_date = datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
        
        if parsed_start_date > parsed_end_date:
            return jsonify({"error": "Start date must be before end date"}), 400
        
        if data.get("meeting_length") % 15 != 0:
            return jsonify({"error": "Meeting length must be divisible by 15"}), 400
        
        
        new_meeting = Meeting(start_date=parsed_start_date,
                            end_date=parsed_end_date,
                            meeting_length=data.get("meeting_length"),
                            meeting_name=data.get("meeting_name"),
                            meeting_description=data.get("meeting_description"),
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
        return redirect(url_for('static', filename='date-selector.html')), 200
    
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
            meeting_list.append({
                "id": meeting.id,
                "start_date": meeting.start_date,
                "end_date": meeting.end_date,
                "meeting_length": meeting.meeting_length,
                "meeting_name": meeting.meeting_name,
                "meeting_description": meeting.meeting_description,
                "share_code": meeting.share_code
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

        return jsonify({
            "id": meeting.id,
            "start_date": meeting.start_date,
            "end_date": meeting.end_date,
            "meeting_length": meeting.meeting_length,
            "meeting_name": meeting.meeting_name,
            "meeting_description": meeting.meeting_description,
            "share_code": meeting.share_code,
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

        return jsonify({
            "id": meeting.id,
            "start_date": meeting.start_date,
            "end_date": meeting.end_date,
            "meeting_length": meeting.meeting_length,
            "meeting_name": meeting.meeting_name,
            "meeting_description": meeting.meeting_description,
            "share_code": meeting.share_code,
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
        return jsonify({"message": "User added to timeslot"}), 200
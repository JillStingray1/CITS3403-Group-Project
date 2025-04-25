from flask import Flask, session, request, jsonify, redirect, url_for
from models.Models import User, Meeting, Timeslot
from tools import validate_username, validate_password, save_login_session, clear_login_session, generate_share_code
from middleware.middleware import secure
from datetime import date, datetime


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


        amount_days = (parsed_end_date - parsed_start_date).days + 1
        for i in range(amount_days * 32):
            new_timeslot = Timeslot(order=i, meeting_id=new_meeting.id)
            db.session.add(new_timeslot)
            db.session.commit()
        
        return redirect(url_for('static', filename='date-selector.html')), 200
    

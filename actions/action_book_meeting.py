import os
import json
from datetime import datetime
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionBookMeeting(Action):

    def name(self):
        return "action_book_meeting"

    def run(self, dispatcher, tracker, domain):

        # Collect slot values
        meeting_date = tracker.get_slot("meeting_date")
        meeting_time = tracker.get_slot("meeting_time")
        meeting_reason = tracker.get_slot("meeting_reason")

        # Build appointment object
        appointment = {
            "date": meeting_date,
            "time": meeting_time,
            "reason": meeting_reason,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Build full path to appointments.json
        base_dir = r"C:\Users\saima\doctor_assistant"
        file_path = os.path.join(base_dir, "db", "appointments.json")

        try:
            # Ensure directory exists
            os.makedirs(os.path.join(base_dir, "db"), exist_ok=True)

            # Create file if missing
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    json.dump([], f)

            # Load existing appointments
            with open(file_path, "r") as f:
                data = json.load(f)

            # Append new appointment
            data.append(appointment)

            # Save updated list
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)

            # Return success
            return [SlotSet("return_value", "success")]

        except Exception as e:
            print("Error booking meeting:", e)
            return [SlotSet("return_value", "error")]

# app.py
from flask import Flask, request, jsonify
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER,API_KEY
from twilio.base.exceptions import TwilioRestException

app = Flask(__name__)


@app.route('/send-sms', methods=['POST'])
def send_sms():
    # Parse request data
    data = request.json
    phone_number = data.get('phone_number')
    message = data.get('message')
    
    # Send SMS using Twilio
    try:      
        provided_api_key = request.headers.get('X-API-Key')

        if not provided_api_key or provided_api_key != API_KEY:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401 
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return jsonify({'status': message.status, 'message': 'SMS sent successfully','message_id':message.sid})
    except TwilioRestException as e:
        # Handle Twilio exception and return an appropriate error response
        error_message = str(e.msg) if e.msg else 'Twilio error occurred'
        status_code = e.status
        return jsonify({'status': 'error','statusCode':status_code, 'message': error_message}), 400

    except Exception as e:
        status_code = e.status
        # Handle other exceptions
        return jsonify({'status': 'error','statusCode':status_code, 'message': str(e)}), 500

    

if __name__ == '__main__':
    app.run(debug=True)

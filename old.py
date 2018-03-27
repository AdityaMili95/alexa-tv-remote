import os
import json
from pprint import pprint
from flask import Flask
from flask_ask import Ask, statement, question, session
app = Flask(__name__)
ask = Ask(app, '/')
lirc_file_conf = 'myTv'
power_button_command = 'KEY_POWER'
@ask.launch
def start_skill():
    welcome_message = 'How should the t.v. update?'
    return question(welcome_message)
@ask.intent('ChangePowerIntent')
def change_power(power_value):
    # Tell LIRC to send IR LED blink pattern to turn TV on/off
    os.system('irsend SEND_ONCE {} {}'.format(lirc_file_conf, power_button_command))
    text = 'Turning the t.v. {}'.format(power_value)
    return statement(text)
if __name__ == '__main__':
    app.run(debug=True)
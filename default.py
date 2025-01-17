import blink_ir_led

import json
from pprint import pprint

from flask import Flask, request
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def start_skill():
    welcome_message = 'How should the t.v. update?'
    return question(welcome_message)

@ask.intent('ChangePowerIntent')
def change_power(power_value):
    print(power_value)

    r = blink_ir_led.change_power(power_value)

    if r == False:
        text = 'Sorry, I could not find that command.'
    else:
        text = 'Turning the t.v. {}'.format(power_value)

    return statement(text)

@ask.intent('ChangeSourceIntent')
def change_source(source_value):
    print(source_value)

    blink_ir_led.change_source(source_value)

    text = 'Changing the source to {}'.format(source_value)
    return statement(text)

@ask.intent('MuteIntent')
def change_mute(mute_value):
    print(mute_value)

    blink_ir_led.change_mute()

    text = 'Will {} the t.v.'.format(mute_value)
    return statement(text)

@ask.intent('ChangeVolumeIntent')
def change_volume(volume_value, increase_or_decrease_volume):
    print(volume_value)
    print(increase_or_decrease_volume)

    blink_ir_led.change_volume(int(volume_value), increase_or_decrease_volume)

    text = 'Updating the volume by {}'.format(volume_value)
    return statement(text)

@ask.intent('OpenSourceMenuIntent')
def change_sourcemenu(source_value):
    print(source_value)
    r = blink_ir_led.change_sourcemenu(source_value)
    if source_value == 'open':
        text = 'Opening the source menu'
    elif source_value == 'close':
        text = 'Closing the source menu'
    else:
        text = 'Sorry, I could not find that command.'
    return statement(text)

@ask.intent('MoveIntent')
def change_move(move_value):
    print(move_value)

    blink_ir_led.change_move(move_value)

    text = 'Moving {}'.format(move_value)
    return statement(text)

# API endpoint
@app.route('/api', methods=['POST'])
def api():
    print(request.form)
    action = request.form['action']
    value = request.form['value']
    if action == 'power':
        blink_ir_led.change_power(value)
    elif action == 'source':
        blink_ir_led.change_source(value)
    elif action == 'sourcemenu':
        blink_ir_led.change_sourcemenu(value)
    elif action == 'mute':
        blink_ir_led.change_mute()
    elif action == 'move':
        blink_ir_led.change_move(value)
    elif action == 'volume':
        if int(value) >= 0:
            increase_or_decrease_volume = 'increase'
        elif int(value) < 0:
            increase_or_decrease_volume = 'decrease'
        blink_ir_led.change_volume(abs(int(value)), increase_or_decrease_volume)
    else:
        return "Error", 500
    return "Updating TV", 200

if __name__ == '__main__':
    app.run(debug=True)

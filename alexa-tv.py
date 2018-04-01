import os
import json
import time
from pprint import pprint
from flask import Flask
from flask_ask import Ask, statement, question, session


time_between_press_initial = 1.5
time_between_press_source = 0.2
time_between_press_before_exit = 0.5

app = Flask(__name__)
ask = Ask(app, '/')
lirc_file_conf = 'myTv'


def change_power_func(power_value):
    if power_value != 'on' and power_value != 'off':
        return False

    os.system('irsend SEND_ONCE {} KEY_POWER'.format(lirc_file_conf))
    return True

def change_volume_func(volume_value, increase_or_decrease_volume):
    key = ''

    if volume_value > 20:
        volume_value = 20

    text = 'Sorry, I could not find that command.'

    if increase_or_decrease_volume == 'higher' or increase_or_decrease_volume == 'increase' or increase_or_decrease_volume == 'raise':
        key = 'KEY_VOLUMEUP'
        text = 'Increasing the volume by {}'.format(volume_value)
    elif increase_or_decrease_volume == 'decrease' or increase_or_decrease_volume == 'lower':
        key = 'KEY_VOLUMEDOWN'
        text = 'Reducing the volume by {}'.format(volume_value)
    else:
    	return text

    for x in range (0, volume_value):
        time.sleep(time_between_press_volume)
        os.system('irsend SEND_ONCE {} {}'.format(lirc_file_conf, key))

    return text

def change_program_func(program_value, next_or_previous_program):
	key = ''

	if program_value > 20:
		program_value = 20
	
	text = 'Sorry, I could not find that command.'

	if next_or_previous_program == 'next' or next_or_previous_program == 'forward':
		text = 'Updating the channel forward by {}'.format(program_value)
		key = 'KEY_PAGEUP'
	elif next_or_previous_program == 'previous' or next_or_previous_program == 'back':
		key = 'KEY_PAGEDOWN'
		text = 'Updating the channel backward by {}'.format(program_value)
	else:
		return text

	for x in range (0, program_value):
		time.sleep(time_between_press_volume)
		os.system('irsend SEND_ONCE {} {}'.format(lirc_file_conf, key))

	return text



def change_ok_func():
	os.system('irsend SEND_ONCE {} KEY_OK'.format(lirc_file_conf))

def change_programnumber_func(program_value):

	val = program_value
	if val > 99:
		val = 99
	elif val < 0:
		val = 0

	txtnumber = str(val)
	text = 'Updating to channel {}'.format(txtnumber)

	if val > 9:
		os.system('irsend SEND_ONCE {} KEY_{}'.format(lirc_file_conf,txtnumber))
	else:
		os.system('irsend SEND_ONCE {} KEY_{}'.format(lirc_file_conf,txtnumber[:1]))
		time.sleep(time_between_press_volume)
		os.system('irsend SEND_ONCE {} KEY_{}'.format(lirc_file_conf,txtnumber[1:2]))

	return text



def change_move_func(move_value):
    if move_value == 'up':
        os.system('irsend SEND_ONCE {} KEY_UP'.format(lirc_file_conf))
    elif move_value == 'right':
        os.system('irsend SEND_ONCE {} KEY_RIGHT'.format(lirc_file_conf))
    elif move_value == 'down':
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
    elif move_value == 'left':
        os.system('irsend SEND_ONCE {} KEY_LEFT'.format(lirc_file_conf))
    else:
    	return False

    return True

def change_mute_func():
    os.system('irsend SEND_ONCE {} KEY_MUTE'.format(lirc_file_conf))


def change_sourcemenu_func(source_value):
    if source_value == 'open':
        os.system('irsend SEND_ONCE {} KEY_SWITCHVIDEOMODE'.format(lirc_file_conf))
    elif source_value == 'close':
        os.system('irsend SEND_ONCE {} KEY_EXIT'.format(lirc_file_conf))
    else:
    	return False

    return True

def change_source_func(source_value):
    if source_value == 'cable box':
        os.system('irsend SEND_ONCE {} KEY_MENU'.format(lirc_file_conf))
        time.sleep(time_between_press_initial)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_OK'.format(lirc_file_conf))
        time.sleep(time_between_press_before_exit)
        os.system('irsend SEND_ONCE {} KEY_EXIT'.format(lirc_file_conf))
    elif source_value == 'HDMI2':
        os.system('irsend SEND_ONCE {} KEY_MENU'.format(lirc_file_conf))
        time.sleep(time_between_press_initial)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_OK'.format(lirc_file_conf))
        time.sleep(time_between_press_before_exit)
        os.system('irsend SEND_ONCE {} KEY_EXIT'.format(lirc_file_conf))
    elif source_value == 'Xbox':
        os.system('irsend SEND_ONCE {} KEY_MENU'.format(lirc_file_conf))
        time.sleep(time_between_press_initial)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_DOWN'.format(lirc_file_conf))
        time.sleep(time_between_press_source)
        os.system('irsend SEND_ONCE {} KEY_OK'.format(lirc_file_conf))
        time.sleep(time_between_press_before_exit)
        os.system('irsend SEND_ONCE {} KEY_EXIT'.format(lirc_file_conf))




@ask.launch
def start_skill():
    welcome_message = 'How should the t.v. update?'
    return question(welcome_message)

@ask.intent('ChangePowerIntent')
def change_power(power_value):
    # Tell LIRC to send IR LED blink pattern to turn TV on/off
    r = change_power_func(power_value)
    if r == False:
        text = 'Sorry, I could not find that command.'
    else:
        text = 'Turning the t.v. {}'.format(power_value)

    return statement(text)


@ask.intent('MuteIntent')
def change_mute(mute_value):
    change_mute_func()
    text = 'Will {} the t.v.'.format(mute_value)
    return statement(text)

@ask.intent('OkIntent')
def change_ok(ok_value):
    change_ok_func()
    text = 'Pressing okay button'
    return statement(text)

@ask.intent('ChangeProgramIntent')
def change_program(program_value, next_or_previous_program):
    text = change_program_func(int(program_value), next_or_previous_program)
    return statement(text)

@ask.intent('ChangeProgramNumberIntent')
def change_programnumber(program_value):
    text = change_programnumber_func(int(program_value))
    return statement(text)


@ask.intent('ChangeVolumeIntent')
def change_volume(volume_value, increase_or_decrease_volume):
    text = change_volume_func(int(volume_value), increase_or_decrease_volume)
    return statement(text)

@ask.intent('OpenSourceMenuIntent')
def change_sourcemenu(source_value):

	change_sourcemenu_func(source_value)

	if source_value == 'open':
		text = 'Opening the source menu'
	elif source_value == 'close':
		text = 'Closing the source menu'
	else:
		text = 'Sorry, I could not find that command.'
	return statement(text)


@ask.intent('MoveIntent')
def change_move(move_value):

    r = change_move_func(move_value)
    if r == False:
        text = 'Sorry, I could not find that command.'
    else:
        text = 'Moving {}'.format(move_value)

    return statement(text)

@ask.intent('ChangeSourceIntent')
def change_source(source_value):

    change_source_func(source_value)
    text = 'Changing the source to {}'.format(source_value)
    return statement(text)

# API endpoint
@app.route('/api', methods=['GET'])
def api():
    action = request.form['action']
    value = request.form['value']
    if action == 'power':
        change_power_func(value)
    elif action == 'source':
        change_source_func(value)
    elif action == 'sourcemenu':
        change_sourcemenu_func(value)
    elif action == 'mute':
        change_mute_func()
    elif action == 'move':
        change_move_func(value)
    elif action == 'ok':
        change_ok_func()
    elif action == 'program':
        if int(value) >= 0:
            next_or_previous_program = 'next'
        elif int(value) < 0:
            next_or_previous_program = 'back'
        change_program_func(abs(int(value)), next_or_previous_program)
    elif action == 'programnumber':
        change_programnumber_func(int(value))
    elif action == 'volume':
        if int(value) >= 0:
            increase_or_decrease_volume = 'increase'
        elif int(value) < 0:
            increase_or_decrease_volume = 'decrease'
        change_volume_func(abs(int(value)), increase_or_decrease_volume)
    else:
        return "Error", 500
    return "Updating TV", 200

if __name__ == '__main__':
    app.run(debug=True)

#Coded By Ashkan Rafiee https://github.com/AshkanRafiee/WarpRefer/
import PySimpleGUI as sg
import webbrowser
import urllib.request
import json
import time
import queue
import threading

current_failed = None
current_gb = None
referrer = None
status = None
stop_thread = None
url = 'https://api.cloudflareclient.com/v0a745/reg'


gui_queue = queue.Queue()
sg.theme('DarkPurple5')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Get Free Warp Plus Referrals!'),sg.Text('GB auto added'),sg.Text('0',key='success',size=(4,1)),sg.Text('GB auto failed'),sg.Text('0',key='failed',size=(4,1))],
          [sg.Text('Enter Your 1.1.1.1 ID'),sg.Input(size=(36,1), key='referrer'),sg.Text('',key='state',size=(15,1))],
          [sg.Button('Start Automatic'), sg.Button('Stop'), sg.Button('Website'), sg.Button('Exit'),sg.Text('Made By Ashkan Rafiee')]]
# Create the Window
window = sg.Window('WarpRefer - Get Free Warp Plus Referrals!', layout)
# Event Loop to process "events" and get the "values" of the inputs

def run():
	global referrer
	referrer = values['referrer']
	if ( len(referrer) != 36 ):
		sg.popup('Error - Invalid ID!', "Your ID must contain 36 characters")
	else:
		body = {"referrer": referrer}
		data = json.dumps(body).encode('utf8')
		headers = {'User-Agent': 'okhttp/3.12.1'}
		req         = urllib.request.Request(url, data, headers)
		response    = urllib.request.urlopen(req)
		status_code = response.getcode()
		return status_code

def automatic(gui_queue):
	window.Element('state').Update(value='Working...')
	global referrer
	global status
	global current_gb
	global current_failed
	global stop_thread
	referrer = values['referrer']
	x = 0
	y = 0
	while status:
		if stop_thread:
			break
		result = run()
		if result == 200:
			x = x + 1
			current_gb = x
			window.Element('success').Update(value=current_gb)
			for i in range(20,0,-1):
				if stop_thread:
					break
				window.Element('state').Update(value=i)
				time.sleep(1)
			gui_queue.put('** Done **')
		else:
			y = y + 1
			current_failed = y
			for i in range(20,0,-1):
				if stop_thread:
					break
				window.Element('state').Update(value=i)
				time.sleep(1)
			gui_queue.put('** Not Done **')


while True:
    event, values = window.read()
    if event == 'Start Automatic':
    	referrer = values['referrer']
    	if ( len(referrer) != 36 ):
    		sg.popup('Error - Invalid ID!', "Your ID must contain 36 characters, Find it at:                  1.1.1.1 App/☰/Advanced/Diagnostics/ID")
    	else:
    		stop_thread = False
    		status = True
    		window['Start Automatic'].update(disabled=True)
    		threading.Thread(target=automatic, args=(gui_queue,), daemon=True).start()

    if event == 'Stop':
    	status = False
    	stop_thread = True
    	window['Start Automatic'].update(disabled=False)
    	window.Element('state').Update(value='Everything Stopped!')

    if event == 'Website':
    	webbrowser.open_new('https://ashkanrafiee.ir/WarpRefer')

    if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
        break


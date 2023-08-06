Web radio expandable collection
---
 * REST API app on blueprints and application factory of the flask framework, with SQLite database
 * organize your web radios, delete and update, backup and restore
 * style your app with pictures, import a poem, song text, or a funny comment to have a good time
 * create a shuffled playlist of local audio files in seconds, directly in your gym or at work
 * backend (server) opens the connection, buffers the incoming stream and presents it to the browser on internal net
 * frontend (browser) controls the backend, plays local audio, shows a spectrum analyser at your disposal
 * Android: download to mobile (link below .-apk), rename *WHL to *ZIP, extract with Android _file_ manager
 * https://pypi.org/project/eisenradio-apk/ , uses Python Kivy library for multi-touch on start-up `https://pypi.org/project/Kivy/#files`



		""" sketch """

	     |B |               |S | Flask web server, Header[Werkzeug/2.0.2 Python/3.10.1]
	     |r |listen         |e |-------> starRadio
	     |o |------->   <-- |r |
	     |w |GhettoRecorder |v |-------> planetRadio
	     |s |--->    <----- |e |
	     |e |               |r |-------> satteliteRadio
	     |r |               |  |
         net: localhost     net: internet
         CORS: accept       CORS: deny
         audioNode: 1,-1    audioNode: 0, 0
         JavaScript,CSS     Python, SQL

    Cross-Origin Resource Sharing mechanism (CORS) 
    i.a. prevents Browser from analysing audio from internet
    
    
---
pip install
-
	""" xxs Linux xxs """
    $ pip3 install eisenradio
    $ python3 -m eisenradio.wsgi  # watch flask

    """ xxm Windows xxm """
    > pip install eisenradio
    > python -m eisenradio.wsgi

    """ xxl big company xxl """
    $$$ pip3 install eisenradio
    $$$ python3 -m eisenradio.app  # serve flask
    """ for the sake of completeness, a python
        production server 'waitress' is started """
---
Pytest
---
> ~ ... /test/functional$ python3 -m pytest -s    # -s print to console

find the modified test db in ./app_writable/db

Uninstall
---
Python user:

* find module location
* uninstall and then remove remnants

>$ pip3 show eisenradio

>$ pip3 uninstall eisenradio

Location: ... /python310/site-packages

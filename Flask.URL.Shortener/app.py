from flask import Flask, render_template, request, redirect, url_for, flash, abort, session,jsonify
import json
import os.path
from werkzeug.utils import secure_filename

#Definition of libraries used:
"""
return redirect(url_for('home'))
	#redirect URL
	#url_for calls the function home defined in app.route('/')

render_template - render the html page 
request - working with HTTP protocol
flash - inserting messages/error on page
abort - allows to send error messages
session - interact with cookies 
jsonify - simple API to display output to browser in json format

os.path - checking presence of specific files in the underlying OS

"""

# 'app' is special word in FLASK. __name__ is the name of the file converted to app 
app = Flask(__name__)

# This key is used to securely transfer flash messages to end user. This also avoids snooping of the 
# messages
app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'

@app.route('/')
def home():
    #You can pass variable into templates. Example is session keys from codes set by user
    return render_template('home.html', codes=session.keys())  #codes here is input to home.html

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        #Checks if a file names urls.json already exists  
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                #Deserialise the JSON file into a JSON OBJECT (Can be dict or list depending on the format)
                urls = json.load(urls_file)


        #Sample POST and see home.html for the "code"         
        #url=hxxp://go5.com&code=go5
        #Checks if the code is in the JSON file already. If it is, redirect to home page
        if request.form['code'] in urls.keys():
            #This flash message is handled in the HTML page 
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home'))

        #Check if url is sent OR file
        #url=hxxp://go5.com&code=go5 Keys here are "url" and "code"
        if 'url' in request.form.keys():
            #Update dictionary object 
            urls[request.form['code']] = {'url':request.form['url']}
        else:  #Assumes file is sent 
            #file=Screen1.png  code=screen1
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            #Filename saved as "screen1Screen1.png"
            f.save('/Users/monkeyfilo/Desktop/TRASH/myFLASK/url-shortener/Myworking/static/user_files/' + full_name)
            #JSON entry {"screen1": {"file": "screen1Screen1.png"}}
            urls[request.form['code']] = {'file':full_name}
        
        #Write the urls object to urls.json (i.e. url_file) - AKA serialisation or written to file
        with open('urls.json','w') as url_file:
            #Dump or write the urls (object) to urls.json file - AKA serialisation or written to file
            json.dump(urls, url_file)
            #Set the value of session key to the value of the code (I think session is a key/pair)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code']) #code here is input to html page
    else:
        return redirect(url_for('home'))

#Enables shorten URL code to access real URL
#'/<string:code>' is used as a random string which is checked in url.keys file
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'): #Does urls.json file is existing?  
        with open('urls.json') as urls_file:
            urls = json.load(urls_file) #Deserialise urls.json
            #Sample {"kaw": {"url": "https://kawili.net"}}
            if code in urls.keys():  #Is the "code" input from the function in the existing keys?  
                if 'url' in urls[code].keys(): #Sample {"kaw": {"url": "https://kawili.net"}}
                    return redirect(urls[code]['url']) #http://localhost:5000/kaw -> https://kawili.net
                else:
                    #{"house": {"file": "house67_Cherry_Lane.jpg"}}
                    #url_for('static) = means I am looking for a static file  
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return (abort(404))


#Defines custom error handler for abort(404) instead of the default error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404  #404 here is optional, but good bec it informs browser


#Simple API to display output to browser in json format
@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


from flask import Flask, render_template, request, redirect, url_for, flash, abort
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
abort - 

os.path - checking presence of specific files in the underlying OS

"""

# 'app' is special word in FLASK. __name__ is the name of the file converted to app 
app = Flask(__name__)

# This key is used to securely transfer flash messages to end user. This also avoids snooping of the 
# messages
app.secret_key = 'h432hi5ohi3h5i5hi3o2hi'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        #Checks if a file names urls.json already exists  
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                #Deserialise the JSON file into a JSON OBJECT
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
            f.save('/Users/monkeyfilo/Desktop/TRASH/myFLASK/url-shortener/02_08/url-shortener/' + full_name)
            #JSON entry {"screen1": {"file": "screen1Screen1.png"}}
            urls[request.form['code']] = {'file':full_name}

        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))

#Enables shorten URL code to access real URL
#'/<string:code>' is used as a random string which is checked in url.keys file
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
            #I have added this to catch error in case non-existent code is used
            else:
                return redirect(url_for('home'))



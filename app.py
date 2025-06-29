from datetime import datetime
from flask import Flask, render_template, request

from flask_migrate import Migrate, migrate


import requests
import re

# create flask app
app = Flask(__name__)









def get_projects():
    api_url = f'https://api.github.com/users/akashzamnani05/repos'
    cards_list = requests.get(api_url).json()
    return cards_list


@app.errorhandler(Exception)
def handle_exception(message):
    return render_template('error.html', message="Bad Request"), 400


@app.errorhandler(404)
def err_404(message):
    return render_template('error.html', message='404 Page Not Found'), 404


@app.route('/')
def main_page():
    return render_template('index.html', title='Akash Zamnani')


@app.route('/home')
def home():
    return render_template('base.html', title='Base')


@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    contact_info_included = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        reason = request.form.get('reason', '').strip()

        # check phone number
        contact_info_included = False
        if 10 <= len(phone) <= 13 and re.fullmatch(r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$', phone):
            entry = Contact(name, phone, email, reason)
            db.session.add(entry)
            db.session.commit()
            contact_info_included = True

    return render_template('contact.html', title='Contact Page', contact_status=contact_info_included)


@app.route('/projects')
def projects_page():
    return render_template('projects.html', title="Projects", cards=get_projects())

@app.route('/resume')
def resume_page():
    return render_template('resume.html', title="Projects")

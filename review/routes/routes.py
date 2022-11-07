import datetime

from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required
from review.models.models import Company, Platform, Theme

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    return render_template('main_page.html')


@main.route('/add', methods=['GET'])
@login_required
def add_request_form():
    companies = Company.query.all()
    platforms = Platform.query.all()
    themes = Theme.query.all()

    return render_template('add_request.html', companies=companies, platforms=platforms, themes=themes)


@main.route('/add', methods=['POST'])
@login_required
def add_request():
    company = request.form.get('company')
    platforms = request.form.getlist('platform')
    datebegin = request.form.get('datebegin')
    dateend = request.form.get('dateend')
    themes = request.form.getlist('themes')

    if not datebegin == '' or not dateend == '':
        try:
            datebegin_datetime = datetime.datetime.strptime(datebegin, "%d.%m.%Y")
            dateend_datetime = datetime.datetime.strptime(dateend, "%d.%m.%Y")
        except:
            return redirect(url_for('main.add_request_form'))
    else:
        datebegin_datetime = ''
        dateend_datetime = ''

    return render_template('schedule.html',
                           company=company,
                           platforms=platforms,
                           datebegin=datebegin_datetime,
                           dateend=dateend_datetime,
                           themes=themes)


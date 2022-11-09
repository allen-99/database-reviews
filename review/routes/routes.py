import datetime

from bson import json_util
import json

from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required, current_user

from review.models.getters import get_themes_name, get_company_name, get_platforms_name
from review.models.models import Company, Platform, Theme
from review.diagrams.create_diagrame import create_diagram


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

    if not datebegin == '' and not dateend == '':
        try:
            datebegin_datetime = datetime.datetime.strptime(datebegin, "%d.%m.%Y")
            dateend_datetime = datetime.datetime.strptime(dateend, "%d.%m.%Y")
        except:
            return redirect(url_for('main.add_request_form'))
    else:
        datebegin_datetime = None
        dateend_datetime = None

    create_diagram(themes, datebegin_datetime, dateend_datetime, company, platforms)
    data = json.dumps((themes, datebegin, dateend, company, platforms), default=json_util.default)
    return redirect(url_for('main.result', data=data))


@main.route('/result/<data>', methods=['GET'])
@login_required
def result(data):
    data = json.loads(data, object_hook=json_util.object_hook)
    themes = get_themes_name(data[0])
    company = get_company_name(data[3])
    platforms = get_platforms_name(data[4])
    print(platforms)
    path = f'${current_user.id}.png'
    return render_template('schedule.html',
                           path=path,
                           name=current_user.name,
                           platforms=platforms,
                           themes=themes,
                           company=company)

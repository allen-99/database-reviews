from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required
from review.models.models import Company, Platform, Theme

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    return render_template('main_page.html')


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_request():
    companies = Company.query.all()
    platforms = Platform.query.all()
    themes = Theme.query.all()

    return render_template('add_request.html', companies=companies, platforms=platforms, themes=themes)



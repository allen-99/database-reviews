import pandas as pd

from review import db
from sqlalchemy import select

from review.models.models import Theme, Company, Platform
from flask_login import login_required, current_user


def get_themes_name(list_of_themes_id):
    data = select(Theme.theme_name).where(Theme.theme_id.in_(list_of_themes_id))
    return db.session.execute(data).all()


def get_company_name(company_id):
    return db.session.execute(select(Company.company_name).where(Company.company_id == company_id)).all()


def get_platforms_name(list_of_platforms_id):
    return db.session.execute(select(Platform.platform_name).where(Platform.platform_id.in_(list_of_platforms_id))).all()
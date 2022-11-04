from review import db


class Platform(db.Model):
    __tablename__ = 'platform'

    platform_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    platform_name = db.Column(db.String)


class Company(db.Model):
    __tablename__ = 'company'

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String)


class Theme(db.Model):
    __tablename__ = 'theme'

    theme_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theme_name = db.Column(db.String)


class BlockOfText(db.Model):
    __tablename__ = 'block_of_text'

    block_id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    text_id = db.Column(db.Integer,  db.ForeignKey('text.id'))
    theme_id = db.Column(db.Integer,  db.ForeignKey('theme.theme_id'))
    block_text = db.Column(db.String)
    sa_value = db.Column(db.Float)


class Text(db.Model):
    __tablename__ = 'text'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String)
    date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.platform_id'))


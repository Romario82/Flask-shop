from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class SeoSettingsForm(FlaskForm):
    site_name = StringField('Site name', validators=[DataRequired(), Length(max=100)])
    default_title = StringField('Default page title', validators=[DataRequired(), Length(max=150)])
    default_description = TextAreaField('Default meta description', validators=[DataRequired(), Length(max=300)])
    default_keywords = StringField('Default meta keywords', validators=[Optional(), Length(max=300)])
    home_title = StringField('Home page title', validators=[DataRequired(), Length(max=150)])
    home_description = TextAreaField('Home page description', validators=[DataRequired(), Length(max=300)])
    robots = StringField('Robots meta', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Save settings')

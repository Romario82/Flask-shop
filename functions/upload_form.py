from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, InputRequired, Length, NumberRange
from db.config import Config


class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Upload')

    def validate_file(self, field):
        filename = field.data.filename
        if '.' not in filename or filename.rsplit('.', 1)[1].lower() not in Config.ALLOWED_EXTENSIONS:
            raise ValidationError('Invalid file extension. Allowed extensions are: csv, xlsx')


class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=80)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    description = StringField('Description', validators=[DataRequired(), Length(max=80)])
    stock = IntegerField('Stock', default=0, validators=[NumberRange(min=0)])
    manufacturer = StringField('Manufacturer', validators=[Length(max=80)])
    characteristics = StringField('Characteristics', validators=[DataRequired(), Length(max=80)])
    category = StringField('Category', validators=[DataRequired(), Length(max=80)])
    seo_title = StringField('SEO Title', validators=[Length(max=80)])
    seo_description = StringField('SEO Description', validators=[Length(max=80)])
    promotion = StringField('Promotion', validators=[Length(max=80)])
    image = StringField('Image', validators=[Length(max=80)])
    submit = SubmitField('Add Product')


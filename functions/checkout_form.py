from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class CheckoutForm(FlaskForm):
    customer_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(max=100),
            Regexp(
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message='Invalid email address.',
            ),
        ],
    )
    phone = StringField('Phone', validators=[DataRequired(), Length(max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    notes = TextAreaField('Order Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Place order')

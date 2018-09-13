from flask_wtf import FlaskForm

from wtforms import StringField, RadioField, BooleanField, SubmitField
#from wtforms.validators import DataRequired

class RandomForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    color_restrictions = RadioField('Color Identity Restrictions', choices=[('value', 'None'), ('value_two', 'Multicolored'), ('value_three', 'Monocolored')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Generate Commander')
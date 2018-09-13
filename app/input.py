from flask_wtf import FlaskForm

from wtforms import StringField, RadioField, BooleanField, SubmitField
#from wtforms.validators import DataRequired

class RandomForm(FlaskForm):
    #username = StringField('Username', validators=[DataRequired()])
    color_restrictions = RadioField('Color Identity Restrictions', choices=[('none', 'None'), ('multicolored', 'Multicolored'), ('monocolored', 'Monocolored')], default='none')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Generate Commander')
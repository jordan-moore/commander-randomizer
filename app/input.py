from flask_wtf import FlaskForm

from wtforms import StringField, RadioField, BooleanField, SubmitField
#from wtforms.validators import DataRequired

class RandomForm(FlaskForm):
    color_restrictions = RadioField('Color Identity Restrictions',
                                    choices=[('none', 'None'), ('multicolored', 'Multicolored'),
                                             ('monocolored', 'Monocolored')], default='none')
    edhrec_restrictions = RadioField('Popularity Filter',
                                    choices=[('none', 'None'), ('bad', 'Only Bad (Hard Mode)'),
                                             ('decent', 'Decent or Better'), ('good', 'Good')], default='none')
    cmc_max = RadioField('Max Converted Mana Cost',
                                    choices=[('none', 'None'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'),
                                             ('5', 'Five'), ('6', 'Six')], default='none')

    usd_max = RadioField('Max Price USD',
                         choices=[('none', 'None'), ('25', '$25'), ('10', '$10'), ('5', '$5'),
                                  ('1', '$1')], default='none')

    tix_max = RadioField('Max Price Tix',
                         choices=[('none', 'None'), ('25', '25 Tix'), ('10', '10 Tix'), ('5', '5 Tix'),
                                  ('1', '1 Tix')], default='none')

    mtgo_only = BooleanField('Only MTGO Available Cards')
    f_white_borders = BooleanField('F White Borders In Particular')

    submit = SubmitField('Generate Commander!')

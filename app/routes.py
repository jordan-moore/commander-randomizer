from flask import render_template, redirect
from app import app
from app.input import RandomForm
import card_generator

card_generator.initialize()

@app.route('/')
@app.route('/index')
def index():
    return render_template('/home.html', title='Home')


@app.route('/random-commander', methods=['GET', 'POST'])
def login():
    form = RandomForm()

    if form.validate_on_submit():
        print(form.color_restrictions.data)

        if form.color_restrictions.data == 'none':
            return redirect('/random/no-restrictions')
        if form.color_restrictions.data == 'multicolored':
            return redirect('/index')
        if form.color_restrictions.data == 'monocolored':
            return redirect('/index')

        return redirect('/index')

    return render_template('random.html', title='Random Commander', form=form)


@app.route('/random/no-restrictions')
def no_restrictions():
    print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(card_generator.get_all_commanders())
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)

from flask import render_template, redirect, url_for
from app import app
from app.input import RandomForm
import card_generator

card_generator.initialize()


@app.route('/')
@app.route('/index')
def index():
    return render_template('/home.html', title='Home')


@app.route('/health', methods=['GET', 'POST'])
def hello_world():
    return '200', 200


@app.route('/random-commander', methods=['GET', 'POST'])
def login():
    form = RandomForm()

    if form.validate_on_submit():
        print(form.color_restrictions.data)

        if form.color_restrictions.data == 'none':
            return redirect(url_for('no_restrictions'))
        if form.color_restrictions.data == 'multicolored':
            return redirect('/random/multicolored')
        if form.color_restrictions.data == 'monocolored':
            return redirect('/random/monocolored')

        return redirect('/index')

    return render_template('random.html', title='Random Commander', form=form)


@app.route('/random/no-restrictions')
def no_restrictions():
    # print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(card_generator.get_all_commanders())
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)


@app.route('/random/monocolored')
def monocolored():
    # print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(card_generator.get_monocolored_commanders())
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)


@app.route('/random/multicolored')
def multicolored():
    # print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(card_generator.get_multicolored_commanders())
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)
from flask import render_template, redirect, url_for, request
from app import app
from app.input import RandomForm
import card_generator
import enums

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
        # print(form.color_restrictions.data)

        usd_max = form.usd_max.data
        tix_max = form.tix_max.data
        popularity = form.edhrec_restrictions.data
        cmc_max = form.cmc_max.data
        on_mtgo = form.mtgo_only.data
        f_white_borders = form.f_white_borders.data

        if form.color_restrictions.data == 'none':
            return redirect(url_for('no_restrictions', usd_max=usd_max, tix_max=tix_max, popularity=popularity, cmc_max=cmc_max, on_mtgo=on_mtgo, f_white_borders=f_white_borders))
        if form.color_restrictions.data == 'multicolored':
            return redirect(
                url_for('multicolored', usd_max=usd_max, tix_max=tix_max, popularity=popularity, cmc_max=cmc_max,
                        on_mtgo=on_mtgo, f_white_borders=f_white_borders))
        if form.color_restrictions.data == 'monocolored':
            return redirect(
                url_for('monocolored', usd_max=usd_max, tix_max=tix_max, popularity=popularity, cmc_max=cmc_max,
                        on_mtgo=on_mtgo, f_white_borders=f_white_borders))

        return redirect('/index')

    return render_template('random.html', title='Random Commander', form=form)


@app.route('/random/no-restrictions')
def no_restrictions():

    # print('Request Args:' + str(request.args))

    usd_filter = request.args.get('usd_max')
    if usd_filter == '25':
        usd_filter = enums.PriceUSD.UNDER_25
    elif usd_filter == '10':
        usd_filter = enums.PriceUSD.UNDER_10
    elif usd_filter == '5':
        usd_filter = enums.PriceUSD.UNDER_5
    elif usd_filter == '1':
        usd_filter = enums.PriceUSD.UNDER_1
    else:
        usd_filter = enums.PriceUSD.NO_LIMIT

    tix_filter = request.args.get('tix_max')
    if tix_filter == '25':
        tix_filter = enums.PriceTIX.UNDER_25
    elif tix_filter == '10':
        tix_filter = enums.PriceTIX.UNDER_10
    elif tix_filter == '5':
        tix_filter = enums.PriceTIX.UNDER_5
    elif tix_filter == '1':
        tix_filter = enums.PriceTIX.UNDER_1
    else:
        tix_filter = enums.PriceTIX.NO_LIMIT

    popularity_filter = str(request.args.get('popularity')).upper()
    if popularity_filter == 'GOOD':
        popularity_filter = enums.Popularity.GOOD
    elif popularity_filter == 'BAD':
        popularity_filter = enums.Popularity.BAD
    elif popularity_filter == 'DECENT':
        popularity_filter = enums.Popularity.DECENT
    else:
        popularity_filter = enums.Popularity.NONE

    cmc_filter = str(request.args.get('cmc_max')).upper()
    if cmc_filter == '6':
        cmc_filter = enums.CMC.SIX
    elif cmc_filter == '5':
        cmc_filter = enums.CMC.FIVE
    elif cmc_filter == '4':
        cmc_filter = enums.CMC.FOUR
    elif cmc_filter == '3':
        cmc_filter = enums.CMC.THREE
    elif cmc_filter == '2':
        cmc_filter = enums.CMC.TWO
    else:
        cmc_filter = enums.CMC.NONE

    on_mtgo_bool = 'TRUE' == str(request.args.get('on_mtgo')).upper()
    f_white_borders_bool = 'TRUE' == str(request.args.get('f_white_borders')).upper()

    commanders = card_generator.filter_commanders(card_generator.get_all_commanders(), usd_filter, tix_filter, popularity_filter, cmc_filter, on_mtgo_bool, f_white_borders_bool)

    # print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(commanders)
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)


@app.route('/random/monocolored')
def monocolored():

    # print('Request Args:' + str(request.args))

    usd_filter = request.args.get('usd_max')
    if usd_filter == '25':
        usd_filter = enums.PriceUSD.UNDER_25
    elif usd_filter == '10':
        usd_filter = enums.PriceUSD.UNDER_10
    elif usd_filter == '5':
        usd_filter = enums.PriceUSD.UNDER_5
    elif usd_filter == '1':
        usd_filter = enums.PriceUSD.UNDER_1
    else:
        usd_filter = enums.PriceUSD.NO_LIMIT

    tix_filter = request.args.get('tix_max')
    if tix_filter == '25':
        tix_filter = enums.PriceTIX.UNDER_25
    elif tix_filter == '10':
        tix_filter = enums.PriceTIX.UNDER_10
    elif tix_filter == '5':
        tix_filter = enums.PriceTIX.UNDER_5
    elif tix_filter == '1':
        tix_filter = enums.PriceTIX.UNDER_1
    else:
        tix_filter = enums.PriceTIX.NO_LIMIT

    popularity_filter = str(request.args.get('popularity')).upper()
    if popularity_filter == 'GOOD':
        popularity_filter = enums.Popularity.GOOD
    elif popularity_filter == 'BAD':
        popularity_filter = enums.Popularity.BAD
    elif popularity_filter == 'DECENT':
        popularity_filter = enums.Popularity.DECENT
    else:
        popularity_filter = enums.Popularity.NONE

    cmc_filter = str(request.args.get('cmc_max')).upper()
    if cmc_filter == '6':
        cmc_filter = enums.CMC.SIX
    elif cmc_filter == '5':
        cmc_filter = enums.CMC.FIVE
    elif cmc_filter == '4':
        cmc_filter = enums.CMC.FOUR
    elif cmc_filter == '3':
        cmc_filter = enums.CMC.THREE
    elif cmc_filter == '2':
        cmc_filter = enums.CMC.TWO
    else:
        cmc_filter = enums.CMC.NONE

    on_mtgo_bool = 'TRUE' == str(request.args.get('on_mtgo')).upper()
    f_white_borders_bool = 'TRUE' == str(request.args.get('f_white_borders')).upper()

    commanders = card_generator.filter_commanders(card_generator.get_monocolored_commanders(), usd_filter, tix_filter, popularity_filter, cmc_filter, on_mtgo_bool, f_white_borders_bool)

    # print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(commanders)
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)


@app.route('/random/multicolored')
def multicolored():

    # print('Request Args:' + str(request.args))

    usd_filter = request.args.get('usd_max')
    if usd_filter == '25':
        usd_filter = enums.PriceUSD.UNDER_25
    elif usd_filter == '10':
        usd_filter = enums.PriceUSD.UNDER_10
    elif usd_filter == '5':
        usd_filter = enums.PriceUSD.UNDER_5
    elif usd_filter == '1':
        usd_filter = enums.PriceUSD.UNDER_1
    else:
        usd_filter = enums.PriceUSD.NO_LIMIT

    tix_filter = request.args.get('tix_max')
    if tix_filter == '25':
        tix_filter = enums.PriceTIX.UNDER_25
    elif tix_filter == '10':
        tix_filter = enums.PriceTIX.UNDER_10
    elif tix_filter == '5':
        tix_filter = enums.PriceTIX.UNDER_5
    elif tix_filter == '1':
        tix_filter = enums.PriceTIX.UNDER_1
    else:
        tix_filter = enums.PriceTIX.NO_LIMIT

    popularity_filter = str(request.args.get('popularity')).upper()
    if popularity_filter == 'GOOD':
        popularity_filter = enums.Popularity.GOOD
    elif popularity_filter == 'BAD':
        popularity_filter = enums.Popularity.BAD
    elif popularity_filter == 'DECENT':
        popularity_filter = enums.Popularity.DECENT
    else:
        popularity_filter = enums.Popularity.NONE

    cmc_filter = str(request.args.get('cmc_max')).upper()
    if cmc_filter == '6':
        cmc_filter = enums.CMC.SIX
    elif cmc_filter == '5':
        cmc_filter = enums.CMC.FIVE
    elif cmc_filter == '4':
        cmc_filter = enums.CMC.FOUR
    elif cmc_filter == '3':
        cmc_filter = enums.CMC.THREE
    elif cmc_filter == '2':
        cmc_filter = enums.CMC.TWO
    else:
        cmc_filter = enums.CMC.NONE

    on_mtgo_bool = 'TRUE' == str(request.args.get('on_mtgo')).upper()
    f_white_borders_bool = 'TRUE' == str(request.args.get('f_white_borders')).upper()

    commanders = card_generator.filter_commanders(card_generator.get_multicolored_commanders(), usd_filter, tix_filter, popularity_filter, cmc_filter, on_mtgo_bool, f_white_borders_bool)

    # print(card_generator.get_all_commanders())
    commander = card_generator.get_commander(commanders)
    commander_description = commander.description
    commander_image = commander.png
    commander_name = commander.name
    return render_template('/no-restrictions.html', title='Random Commander', name=commander_name, image_png=commander_image, description=commander_description, url=commander.scryfall_uri)
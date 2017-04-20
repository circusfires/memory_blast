import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("YesIntent")
def sel_level():
    sel_lvl_msg = render_template('sel_level')
    
    return question(sel_lvl_msg)


@ask.intent("LevelIntent", convert={'lvl': int})
def next_round(lvl):
    max_level = 10
    if lvl >= 10 :
        
        sel_lvl_msg = render_template('sel_level_repromt_h')
        return question(sel_lvl_msg)
        
    elif lvl < 2:
        
        sel_lvl_msg = render_template('sel_level_repromt_l')
        return question(sel_lvl_msg)
    
    else:
        
        session.attributes['level'] = lvl   #store level
    
        numbers = [randint(0, 9) for _ in range(lvl)]

        
        lvl_indicator = render_template('lvl_ind', lvl=lvl)
        round_msg = render_template('round', numbers=numbers)

        session.attributes['numbers'] = numbers

        round_msg = lvl_indicator + round_msg
        return question(round_msg)


@ask.intent("NoIntent")
def exit_app():
    bye_msg = render_template('goodbye')
    
    return statement(bye_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int, 'fifth': int, 'sixth': int, 'seventh': int, 'eighth': int, 'ninth': int, 'tenth': int})
def answer(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth):

    winning_numbers = session.attributes['numbers']
    
    usr_ans = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth]
    usr_ans = usr_ans[0:(session.attributes['level'])]
    session.attributes['usr_ans'] = usr_ans
    

    if usr_ans == winning_numbers:

        msg = render_template('win')
        lvl_up(session.attributes['level'])

    else:

        msg = render_template('lose')
        lvl_down(session.attributes['level'])

    #do next round    
    next_round(session.attributes['level']);   
    
    return question(msg)


def lvl_up(lvl):
    if lvl < 10:
        session.attributes['level'] += 1
    else:
        session.attributes['level'] = 10
        
    return

def lvl_down(lvl):
    if lvl > 1:
        session.attributes['level'] -= 1
    else:
        session.attributes['level'] = 1
        
    return

        
if __name__ == '__main__':

    app.run(debug=True)
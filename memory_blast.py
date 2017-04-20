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
    welcome_rempromt_msg = render_template('welcome_reprompt')

    return question(welcome_msg)


@ask.intent("LevelIntent", convert={'lvl': int})
def first_round(lvl):
    if (lvl > 10) or (lvl < 1):
        
        sel_lvl_msg = render_template('welcome_repromt')
        return question(sel_lvl_msg)
    
    else:
        
        numbers = [randint(0, 9) for _ in range(lvl+1)]
        
        #store session variables
        session.attributes['level'] = lvl   
        session.attributes['numbers'] = numbers 

        round_msg = render_template('round', lvl=lvl, numbers=numbers)

        return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int, 'fifth': int, 'sixth': int, 'seventh': int, 'eighth': int, 'ninth': int, 'tenth': int, 'eleventh': int})
def answer(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh):

    winning_numbers = session.attributes['numbers']
    
    usr_ans = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh]
    usr_ans = usr_ans[0:(session.attributes['level']+1)]
    session.attributes['usr_ans'] = usr_ans
    

    if usr_ans == winning_numbers:

        msg = render_template('win')
        lvl_up(session.attributes['level'])

    else:

        msg = render_template('lose')
        lvl_down(session.attributes['level'])


    return next_round(msg, session.attributes['level'])

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('goodbye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('goodbye')
    return statement(bye_text)


@ask.session_ended
def session_ended():
    return "{}", 200


def next_round(msg, lvl):
    numbers = [randint(0, 9) for _ in range(lvl+1)]

    #store session variables
    session.attributes['level'] = lvl   
    session.attributes['numbers'] = numbers 

    round_msg = msg + render_template('round', lvl=lvl, numbers=numbers)

    return question(round_msg)


#helper functions
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
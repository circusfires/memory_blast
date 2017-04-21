import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def new_game():
    
    session.attributes['high_score'] = 0
    
    welcome_msg = render_template('welcome')
    welcome_rempromt_msg = render_template('welcome_reprompt')

    return question(welcome_msg).reprompt(welcome_rempromt_msg)


@ask.intent("LevelIntent", convert={'lvl': int})
def first_round(lvl):
    if (lvl > 19) or (lvl < 1):
        
        sel_lvl_msg = render_template('welcome_reprompt')
        return question(sel_lvl_msg).reprompt(sel_lvl_msg)
    
    else:
        
        numbers = [randint(0, 9) for _ in range(lvl+1)]
        
        #store session variables
        session.attributes['level'] = lvl   
        session.attributes['numbers'] = numbers 

        round_msg = render_template('round', lvl=lvl, numbers=numbers)

        return question(round_msg).reprompt(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int, 'fifth': int, 'sixth': int, 'seventh': int, 'eighth': int, 'ninth': int, 'tenth': int, 'eleventh': int, 'twelfth': int, 'thirteenth': int, 'fourteenth': int, 'fifteenth': int, 'sixteenth': int, 'seventeenth': int, 'eighteenth': int, 'nineteenth': int, 'twentieth': int})
def answer(first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth, seventeenth, eighteenth, nineteenth, twentieth):

    winning_numbers = session.attributes['numbers']
    
    usr_ans = [first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth, eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth, seventeenth, eighteenth, nineteenth, twentieth]
    usr_ans = usr_ans[0:(session.attributes['level']+1)]
    usr_ans = translate_nums(usr_ans)
    session.attributes['usr_ans'] = usr_ans
    
    

    if usr_ans == winning_numbers:

        #save high score for this session
        session.attributes['high_score'] = session.attributes['level']
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
    bye_text = high_score()
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = high_score()
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
    if lvl < 19:
        session.attributes['level'] += 1
    else:
        session.attributes['level'] = 19
        
    return

def lvl_down(lvl):
    if lvl > 1:
        session.attributes['level'] -= 1
    else:
        session.attributes['level'] = 1
        
    return

def translate_nums(numbers):
    for i in xrange(len(numbers)):
        if numbers[i] == "oh":
            numbers[i] = 0
            
    return numbers
            
def high_score():
    if session.attributes['high_score'] > 0:
        msg = render_template('goodbye_high', score = (session.attributes['high_score'] + 1))
    
    else:
        msg = render_template('goodbye')
        
    return msg

        
if __name__ == '__main__':

    app.run(debug=True)
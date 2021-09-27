from otree.api import *

c = Currency

doc = """
Your app description
"""

#creating the roles of bad tip, middle tip, and good tip
class Constants(BaseConstants):
    name_in_url = 'stonkz'
    instructions_template = 'stonkz/instructions.html'
    players_per_group = None
    num_rounds = 1
    bad_tip_role = 'Bad tip'
    middle_tip_role = 'Middle tip'
    good_tip_role = 'Good tip'







class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_price = models.IntegerField(initial=100)
    new_price = models.IntegerField(initial=100)
    auction_timeout = models.FloatField()

def get_state(group: Group):
    return dict(
        current_price=group.current_price,
        new_price=group.new_price,

    )

class Player(BasePlayer):
    pass


class Intro(Page):
    pass

#Waits for all players to arrive and sets the time of the round to 120 seconds
class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        import time

        group.auction_timeout = time.time() + 120


# PAGES
class Bid(Page):
    @staticmethod
    def get_timeout_seconds(player: Player):
        import time

        group = player.group
        return group.auction_timeout - time.time()

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)



#figure out what has to happen here to change the variables
    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        my_id = player.id_in_group
        if data:
            if data > group.current_price:
                group.new_price = group.current_price
                group.current_price = data
                return {0: get_state(group)}
            elif data < group.current_price:
                group.new_price = group.current_price
                group.current_price = data
                return {0: get_state(group)}
        else:
            return {0: get_state(group)}



class Results(Page):
    pass


page_sequence = [Intro, WaitToStart, Bid, Results]

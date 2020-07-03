from . import schema, models
from random import choices


def get_subset(hand: schema.Hand, n: int) -> schema.Hand:
    new_hand = schema.Hand(
        relationships=choices(hand.relationships, k=n),
        possessions=choices(hand.possessions, k=n),
        actions=choices(hand.actions, k=n),
        feelings=choices(hand.feelings, k=n),
    )
    return new_hand


async def round_one(game_round: schema.Round, who: schema.PlayerType):
    states = schema.GameState

    f: schema.GameState = game_round.state
    response = []
    if who == schema.PlayerType.changeling:
        if not (f & states.changeling_other_cards_chosen):
            hand = game_round.child_hand
            hand_to_choose_from = hand
            number_to_choose = 2
            new_flags = states.child_other_cards_chosen
            response = (hand_to_choose_from, number_to_choose, new_flags)

    return response


async def play(game_round: schema.Round, who: schema.PlayerType):
    round_number = game_round.round_number

    round_logic = {1: round_one}

    results = await round_logic[round_number](game_round, who)

    return results

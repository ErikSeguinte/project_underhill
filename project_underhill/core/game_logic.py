from . import schema, models


async def round_one(game_round: schema.Round, who: schema.PlayerType):
    states = schema.GameState

    f: schema.GameState = game_round.state
    if who == schema.PlayerType.changeling:
        if not (f & states.changeling_other_cards_chosen):
            hand = game_round.child_hand
            hand.relationships = hand.relationships[:2]
            hand_to_choose_from = hand
            number_to_choose = 2
            new_flags = states.child_other_cards_chosen

    return hand_to_choose_from, number_to_choose, new_flags


async def play(game_round: schema.Round, who: schema.PlayerType):
    round_number = game_round.round_number

    round_logic = {1: round_one}

    results = await round_logic[round_number](game_round, who)

    return results

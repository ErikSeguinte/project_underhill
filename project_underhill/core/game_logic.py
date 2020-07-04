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


async def round_three(game_round: schema.Round, who: schema.PlayerType):
    states = schema.GameState

    f: schema.GameState = game_round.state
    response = []
    if who == schema.PlayerType.changeling:
        if f & states.changeling_complete:
            return response
        phase = [
            states.changeling_self_cards_chosen,
            states.changeling_self_cards_chosen | states.child_self_cards_chosen,
            states.changeling_self_cards_chosen
            | states.child_self_cards_chosen
            | states.changeling_other_cards_chosen,
        ]
        if not (f & phase[0]):

            response = process_phase(
                hand=game_round.changeling_hand,
                owner=schema.PlayerType.changeling,
                n=1,
                next_phase=states.changeling_self_cards_chosen,
            )
        elif f & phase[2] == phase[2]:
            response = "ready"
        elif f & phase[1] == phase[1]:
            response = process_phase(
                hand=game_round.child_hand,
                owner=schema.PlayerType.child,
                n=1,
                next_phase=states.changeling_other_cards_chosen,
            )

    else:
        if f & states.child_complete:
            return response
        phase = [
            states.child_self_cards_chosen,
            states.child_self_cards_chosen
            | states.changeling_other_cards_chosen
            | states.changeling_self_cards_chosen,
        ]
        if not (f & phase[0]):
            response = process_phase(
                hand=game_round.child_hand,
                owner=schema.PlayerType.child,
                n=2,
                next_phase=states.child_self_cards_chosen,
            )
        elif f & phase[1] == phase[1]:
            response = "ready"

    return response


async def round_two(game_round: schema.Round, who: schema.PlayerType):
    states = schema.GameState

    f: schema.GameState = game_round.state
    response = []
    if who == schema.PlayerType.changeling:
        if f & states.changeling_complete:
            return response
        phase = [
            states.changeling_other_cards_chosen,
            states.changeling_other_cards_chosen | states.child_other_cards_chosen,
            states.changeling_other_cards_chosen
            | states.child_other_cards_chosen
            | states.changeling_self_cards_chosen,
        ]
        if not (f & phase[0]):

            response = process_phase(
                hand=game_round.child_hand,
                owner=schema.PlayerType.child,
                n=1,
                next_phase=states.changeling_other_cards_chosen,
            )
        elif f & phase[2] == phase[2]:
            response = "ready"
        elif f & phase[1] == phase[1]:
            response = process_phase(
                hand=game_round.changeling_hand,
                owner=schema.PlayerType.changeling,
                n=1,
                next_phase=states.changeling_self_cards_chosen,
            )

    else:
        if f & states.child_complete:
            return response
        phase = [
            states.child_other_cards_chosen,
            states.child_other_cards_chosen | states.changeling_other_cards_chosen,
        ]
        if not (f & phase[0]):
            response = process_phase(
                hand=game_round.changeling_hand,
                owner=schema.PlayerType.changeling,
                n=2,
                next_phase=states.child_other_cards_chosen,
            )
        elif f & phase[1] == phase[1]:
            response = "ready"

    return response


async def round_one(game_round: schema.Round, who: schema.PlayerType):
    states = schema.GameState

    f: schema.GameState = game_round.state
    response = []
    if who == schema.PlayerType.changeling:
        if f & states.changeling_complete:
            return response
        phase = [
            states.changeling_other_cards_chosen,
            states.changeling_other_cards_chosen | states.child_other_cards_chosen,
        ]
        if not (f & phase[0]):

            response = process_phase(
                hand=game_round.child_hand,
                owner=schema.PlayerType.child,
                n=2,
                next_phase=states.changeling_other_cards_chosen,
            )
        elif f & phase[1] == phase[1]:
            response = "ready"

    else:
        if f & states.child_complete:
            return response
        phase = [
            states.child_other_cards_chosen,
            states.child_other_cards_chosen | states.changeling_other_cards_chosen,
            states.child_other_cards_chosen
            | states.changeling_other_cards_chosen
            | states.child_self_cards_chosen,
        ]
        if not (f & phase[0]):
            response = process_phase(
                hand=game_round.changeling_hand,
                owner=schema.PlayerType.changeling,
                n=1,
                next_phase=states.child_other_cards_chosen,
            )
        elif f & phase[2] == phase[2]:
            response = "ready"
        elif f & phase[1] == phase[1]:
            response = process_phase(
                hand=game_round.child_hand,
                owner=schema.PlayerType.child,
                n=1,
                next_phase=states.child_self_cards_chosen,
            )

    return response


def process_phase(hand: schema.Hand, owner: schema.PlayerType, n, next_phase):
    hand_to_choose_from = hand
    number_to_choose = n
    new_flags = next_phase
    response = (hand_to_choose_from, number_to_choose, new_flags, owner)
    return response


async def play(game_round: schema.Round, who: schema.PlayerType):
    round_number = game_round.round_number

    round_logic = {1: round_one, 2: round_two, 3: round_three}

    results = await round_logic[round_number](game_round, who)

    return results

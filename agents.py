import random
import time


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    @classmethod
    def get_chosen_action(cls, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(cls, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(cls, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action

class MaxNAgent(Agent):
    def get_chosen_action(cls, state, max_depth):
        time.sleep(0.5)
        score, action = cls.max_n(state, max_depth)
        return action

    @classmethod
    def max_n(cls, state, depth):
        if depth == 0 or state.is_goal_state():
            return state.get_scores(), None

        best_score, best_action = None, None

        player = state.get_on_move_chr()
        actions = state.get_legal_actions() or []

        if not actions:
            return state.get_scores(), None

        for action in actions:
            new_state = state.generate_successor_state(action)
            score, move = cls.max_n(new_state, depth - 1)

            if best_score is None or score[player] > best_score[player]:
                best_score = score
                best_action = action

        return best_score, best_action

class MinimaxAgent(Agent):
    def get_chosen_action(cls, state, max_depth):
        time.sleep(0.5)
        score, action = cls.minimax(state, max_depth, state.get_on_move_chr())
        return action

    @classmethod
    def get_opponents(cls, state, player):
        return list(filter(lambda x: x != player, state.get_scores().keys()))

    @classmethod
    def evaluate(cls, state, player):
        return state.get_score(player) - state.get_score(cls.get_opponents(state, player)[0])

    @classmethod
    def minimax(cls, state, depth, player):
        if depth == 0 or state.is_goal_state():
            return cls.evaluate(state, player), None

        if state.get_on_move_chr() == player:
            best_result = float("-inf")
            best_action = None

            actions = state.get_legal_actions()
            if not actions:
                return cls.evaluate(state, player), None

            for action in actions:
                new_state = state.generate_successor_state(action)
                result, move = cls.minimax(new_state, depth - 1, player)

                if result > best_result:
                    best_result = result
                    best_action = action

            return best_result, best_action
        else:
            best_result = float("+inf")
            best_action = None

            actions = state.get_legal_actions()
            if not actions:
                return cls.evaluate(state, player), None

            for action in actions:
                new_state = state.generate_successor_state(action)
                result, move = cls.minimax(new_state, depth - 1, player)

                if result < best_result:
                    best_result = result
                    best_action = action

            return best_result, best_action
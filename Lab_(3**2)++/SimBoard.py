import numpy as np

from itertools import product
from copy import deepcopy
from collections import defaultdict


class Board():
    '''
    Initialize a `Board` for playing Tic-Tac-Toe.
    '''
    def __init__(self):
        # Canonical states, where everything begins. The agent will
        # use a canonical version of the board, that is a standard
        # version from which every other configuration can be
        # obtained by rotating and mirroring.
        self.canonical_corner = np.array([[1, 0, 0],
                                          [0, 0, 0],
                                          [0, 0, 0]], dtype=np.int8)
        self.canonical_middle = np.array([[0, 0, 0],
                                          [1, 0, 0],
                                          [0, 0, 0]], dtype=np.int8)
        self.canonical_center = np.array([[0, 0, 0],
                                          [0, 1, 0],
                                          [0, 0, 0]], dtype=np.int8)
        
        # Scores associated to each position.
        self.magic_square = np.array([[2, 7, 6],
                                      [9, 5, 1],
                                      [4, 3, 8]], dtype=np.int8)
        
        # How many times a state is hit and the associated expected
        # reward.
        self.hit_state = defaultdict(int)
        self.value_state = defaultdict(float)

    def __rotate_board__(self, idx: tuple, player: int, learned: bool=False, not_random: bool=False):
            '''
            Receives a move and apply it, handling both the real,
            where the players effectively play, and the canonical
            board, where the agent has learned to play.

            Parameters

            ---
            idx : `tuple`,
                The index of the board where to place the marker;
            
            player : `int`,
                Which player is making the move;
            
            learned : `bool`, default = `False`
                Whether the agent or a random player is making the move;
            
            not_random : `bool`, default = `False`
                Whether the opponent is playing in a random way.
            '''
            
            # Initialize an empty board and make the move.
            pos = np.zeros(shape=(3, 3), dtype=np.int8)

            # Only for random players.
            if not learned:
                row, column = idx
            marker = 1 if player == 0 else -1

            # Only for not random agents.
            if learned:
                learned_move = idx[0]
                decoded_move = idx[1]
                row, column = decoded_move
            pos[row, column] = marker

            # Update the real board with the real move.
            self.real_board[row, column] = marker

            # Update the canonical board.
            if not learned:
                s = idx[0] + idx[1]
            else:
                s = learned_move[0] + learned_move[1]
            count = 0
            canonical_move = deepcopy(pos)

            # This is the case for every random player, since it has to mutate its move.
            if not learned:
                
                # Checks whether it is the first move.
                first = np.sum(np.abs(self.canonical_board)) == 0 or (self.canonical_board[1, 1] == 1 
                                                                    and np.sum(np.abs(self.canonical_board)) == 1)
                if first:
                    # Corner, adapt the move to a canonical one.
                    if (s % 2 == 0) and (idx[0] != 1):
                        while (canonical_move[0, 0] != marker):
                            count += 1
                            canonical_move = np.array(list(zip(*canonical_move[::-1])), dtype=np.int8)
                
                    # Middle, adapt the move to a canonical one.
                    elif s % 2 != 0:
                        while canonical_move[1, 0] != marker:
                            count += 1
                            canonical_move = np.array(list(zip(*canonical_move[::-1])), dtype=np.int8)
                    
                    # Store number of rotations only the first time. This is needed to compute the inverse of
                    # the canonization.
                    self.count = count if first else self.count

                else:
                    # Corner, adapt the move to a canonical one, considering the precomputednumber of rotations.
                    if (s % 2 == 0) and (idx[0] != 1):
                        while (bool(count < self.count)):
                            count += 1
                            canonical_move = np.array(list(zip(*canonical_move[::-1])), dtype=np.int8)
                
                    # Middle, adapt the move to a canonical one, considering the precomputednumber of rotations.
                    elif (s % 2 != 0) and (count < self.count):
                        while (bool(count < self.count)):
                                count += 1
                                canonical_move = np.array(list(zip(*canonical_move[::-1])), dtype=np.int8)

                # Once a random player has computed the canonical move, update the canonical trajectory,
                # the canonical board and the hit canonical state.
                self.canonical_trajectory.append(tuple(np.argwhere(canonical_move != 0)[0]))
                self.canonical_board += canonical_move
                self.hit_state[tuple(self.canonical_trajectory)] += 1

                # If playing against a not random agent, it is necessary to also update the canonical
                # available moves.
                if not_random:
                    self.available_canonical.remove(self.canonical_trajectory[-1])

            # Only when referring to the moves of a not random agent.
            else:
                row, column = learned_move
                pos = np.zeros(shape=(3, 3), dtype=np.int8)
                pos[row, column] = marker
                canonical_move = deepcopy(pos)
                self.canonical_trajectory.append(learned_move)
                self.canonical_board += canonical_move
                self.hit_state[tuple(self.canonical_trajectory)] += 1
                self.available_canonical.remove(self.canonical_trajectory[-1])
            
    def __check_symmetry__(self):
        # Mirror the board if convenient.
        n_upper_states = np.int8(np.triu(self.canonical_board > 0, k=1))
        n_lower_states = np.int8(np.tril(self.canonical_board > 0, k=-1)) 
        if np.sum(n_upper_states - n_lower_states) > 0:
            self.canonical_board = self.canonical_board.T
    
    def __random_move__(self, player:int, available:list = [], vs_policy: bool=False):
        '''
        Choose a random move from those available.

        Parameters

        ---
        player : `int`,
            The player making the move;
        
        available : `list`, default = `[]`
            A list of available moves;
        
        vs_policy : `bool`, default = `False`
            Whether the random player is playing against a one with a policy.
        '''

        if not vs_policy:
            # Simply consider one list of real states.
            idx = np.random.randint(0, len(available))
            move = available.pop(idx)
            self.real_trajectory.append(move)
            self.__rotate_board__(move, player)
        else:
            # Consider two lists, one for the real and one for the canonical board.
            idx = np.random.randint(0, len(self.available_real))
            move = self.available_real.pop(idx)

            self.real_trajectory.append(move)
            self.__rotate_board__(idx=move, player=player, not_random=True)

    def random_game(self, epsilon: float=0.001):
        '''
        A game in which both the players play randomly. This is used to train
        the agent.

        Parameters

        ---
        epsilon : `float`, default = 0.001
            A value smaller than 1 impacting on the evaluation of the reward.
        '''

        self.real_trajectory = []
        self.canonical_trajectory = []
        self.canonical_board = np.zeros(shape=(3, 3), dtype=np.int8)
        self.real_board = np.zeros(shape=(3, 3), dtype=np.int8)

        available = list(product([0, 1, 2], [0, 1, 2]))
        player = 0
        while len(available) != 0:
            self.__random_move__(player, available)
            reward = self.win()
            if reward != 0:
                # print(f'Player{player} won!')
                break
            player = 1 - player 
        # self.__check_symmetry__()
        
        # After having checked for an eventual mirroring, evaluate all the states in the canonical trajectory.
        for state in tuple(tuple(self.canonical_trajectory[0: i+1]) for i in range(0, len(self.canonical_trajectory))):
            frozen = frozenset(state)
            self.value_state[frozen] = self.value_state[frozen] + epsilon*(reward - self.value_state[frozen])

    def win(self):
        '''
        Checks whether a player won by exploiting the properties of the magic square.
        '''
        score_board = self.magic_square * self.canonical_board
        magic = np.hstack((np.sum(score_board, axis=0), np.sum(score_board, axis=1),
                           np.trace(score_board), np.trace(score_board[:, ::-1])))
        if 15 in magic:
            return 1
        elif -15 in magic:
            return -1
        else:
            return 0

    def policy_game(self, epsilon: float=0.001, agent: str='greedy'):
        '''
        A game in which one players plays randomly and the other one adopting a
        policy. This is used to test the agent.

        Parameters

        ---
        epsilon : `float`, default = 0.001
            A value smaller than 1 impacting on the evaluation of the reward, eventually
            used for updating the reward.
        '''

        self.real_trajectory = []
        self.canonical_trajectory = []
        self.canonical_board = np.zeros(shape=(3, 3), dtype=np.int8)
        self.real_board = np.zeros(shape=(3, 3), dtype=np.int8)

        # Define the available states both in the real board and in the canonical one.
        self.available_real = list(product([0, 1, 2], [0, 1, 2]))
        self.available_canonical = list(product([0, 1, 2], [0, 1, 2]))
        
        # Initialize an agent with a learned strategy.
        if agent == 'greedy':
            agent = ArgMaxAgent(self.value_state)
        elif agent == 'patient':
            agent = PatientAgent(self.value_state)
        else:
            raise('Choose between greedy and patient.')
        player = 0

        # Continue until it is no more possible to play.
        while min(len(self.available_real), len(self.available_canonical)):
            if player == 0:
                # The random player makes a move. Here we consider it playing versus an
                # intelligent player.
                self.__random_move__(player=player, vs_policy=True)
            else:
                # Provide the learned agent the available moves.
                agent.__update_availability__(self.available_real, self.available_canonical)

                # Choose the best canonical move and decode into a real one as well.
                learned_move, decoded_move = agent.move(self.canonical_trajectory, self.count)
                self.real_trajectory.append(decoded_move)
                self.available_real.remove(self.real_trajectory[-1])
                self.__rotate_board__(idx=[learned_move, decoded_move], player=player, learned=True, not_random=True)
                row, column = decoded_move
                self.real_board[row, column] = -1
            reward = self.win()
            if reward != 0:
                # print(f'Player{player} won!')
                break
            player = 1 - player
        self.reward = reward
        # self.__check_symmetry__()
        
        for state in tuple(tuple(self.canonical_trajectory[0: i+1]) for i in range(0, len(self.canonical_trajectory))):
            frozen = frozenset(state)
            self.value_state[frozen] = self.value_state[frozen] + epsilon*(reward - self.value_state[frozen])

class ArgMaxAgent():
    '''
    Agent that chooses the next state in a greedy fashion.
    '''
    def __init__(self, value_state):
        self.value_state = value_state
    
    def __update_availability__(self, available_real: list, available_canonical: list):
        '''
        Pass the lists of real and canonical moves still available.

        Parameters
        ---
        available_real : `list`,
            A list containing available moves in the real board;
        
        available_canonical : `list`,
            A list containing available moves in the canonical board.
        '''

        self.available_real = available_real
        self.available_canonical = available_canonical

    def move(self, canonical_trajectory: list, n_rotations: int):
        '''
        The agent chooses the best possible move considering only the actual
        and the next state.

        Parameters
        ---
        canonical_trajectory : `list`,
            The list of moves done so far in the canonical board.
        
        n_rotations : `int`,
            Number of rotations to compute the inverse of the canonization.
        '''

        # Filter moves of the same length + 1 from the database, regarding the next state.
        possible = {c : self.value_state[c] for c in self.value_state.keys() if len(c) == len(canonical_trajectory)+1}
        # Filter moves related to the specific path, considering the past moves.
        moves = {c.difference(frozenset(canonical_trajectory)) : possible[c] for c in possible.keys() if frozenset(canonical_trajectory).issubset(c)}
        # Select the move with the highest reward.
        best_move = tuple(sorted(moves, reverse=False, key = lambda x : moves[x])[0])[0]
        return best_move, self.__decode_move__(best_move, k = n_rotations)
    
    def __decode_move__(self, move: tuple, k: int):
        '''
        Take a move in the canonical board and return a move in the real board by
        computing the inverse.

        Parameters
        ---
        move : `tuple`,
            A `tuple` containing the indices of the move in the canonical board;

        k : `int`,
            How many times it is necessary to rotate in the opposite sense to
            compute the inverse.
        '''

        zeros = np.zeros(shape=(3, 3), dtype=np.int8)
        zeros[move] = -1
        return tuple(np.argwhere(np.rot90(zeros, k=k) != 0)[0])

class PatientAgent():
    '''
    Agent that chooses the next state in a greedy fashion.
    '''
    def __init__(self, value_state):
        self.value_state = value_state
    
    def __update_availability__(self, available_real: list, available_canonical: list):
        '''
        Pass the lists of real and canonical moves still available.

        Parameters
        ---
        available_real : `list`,
            A list containing available moves in the real board;
        
        available_canonical : `list`,
            A list containing available moves in the canonical board.
        '''

        self.available_real = available_real
        self.available_canonical = available_canonical

    def move(self, canonical_trajectory: list, n_rotations: int):
        '''
        The agent chooses the best possible move considering only the actual
        and the next state.

        Parameters
        ---
        canonical_trajectory : `list`,
            The list of moves done so far in the canonical board.
        
        n_rotations : `int`,
            Number of rotations to compute the inverse of the canonization.
        '''

        # Filter moves of the same length + 2 from the database.
        possible = {c: self.value_state[c] for c in self.value_state.keys() if len(c) == len(canonical_trajectory) + 2}
        # Filter only the moves coherent with the actual path.
        moves = {c.difference(frozenset(canonical_trajectory)) : possible[c] for c in possible.keys() if frozenset(canonical_trajectory).issubset(c)}
        expected = {}

        for key, value in moves.items():
            second_position = tuple(key)[np.random.choice([0, 1])]
            if second_position not in expected:
                expected[second_position] = [value]
            else:
                expected[second_position].append(value)
          # Calculate the mean for each second position
        for position, values in expected.items():
            expected[position] = sum(values) / len(values)
        # From these moves, only consider the ones that are still available.
        # Select the move with the highest expected reward.
        best_move = sorted(expected, reverse=False, key = lambda x : expected[x])[-1]
        return best_move, self.__decode_move__(best_move, k = n_rotations)
    
    def __decode_move__(self, move: tuple, k: int):
        '''
        Take a move in the canonical board and return a move in the real board by
        computing the inverse.

        Parameters
        ---
        move : `tuple`,
            A `tuple` containing the indices of the move in the canonical board;

        k : `int`,
            How many times it is necessary to rotate in the opposite sense to
            compute the inverse.
        '''

        zeros = np.zeros(shape=(3, 3), dtype=np.int8)
        zeros[move] = -1
        return tuple(np.argwhere(np.rot90(zeros, k=k) != 0)[0])
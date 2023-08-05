import numpy as np
import numpy.typing as npt

from pathlib import Path


_chars = ' abcdefghijklmnopqrstuvwxyz'
_char_d = {c: i for i, c in enumerate(_chars)}


def to_english(array: npt.NDArray[np.int64]) -> str:
    """Converts a numpy integer array into a corresponding English string.

    Args:
        array: Word in array (int) form. It is assumed that each integer in the
          array is between 0,...,26 (inclusive).

    Returns:
        A (lowercase) string representation of the word.    
    """
    return ''.join(_chars[i] for i in array)


def to_array(word: str) -> npt.NDArray[np.int64]:
    """Converts a string of characters into a corresponding numpy array.

    Args:
        word: Word in string form. It is assumed that each character in the
          string is either an empty space ' ' or lowercase alphabetical
          character.

    Returns:
        An array representation of the word.
    """
    return np.array([_char_d[c] for c in word])


def get_words(category: str, build: bool=False) -> npt.NDArray[np.int64]:
    """Loads a list of words in array form. 

    If specified, this will recompute the list from the human-readable list of
    words, and save the results in array form.

    Args:
        category: Either 'guess' or 'solution', which corresponds to the list
          of acceptable guess words and the list of acceptable solution words.
        build: If True, recomputes and saves the array-version of the computed
          list for future access.

    Returns:
        An array representation of the list of words specified by the category.
        This array has two dimensions, and the number of columns is fixed at
        five.
    """
    assert category in {'guess', 'solution'}
    
    arr_path = Path(__file__).parent / f'dictionary/{category}_list.npy'
    if build:
       list_path = Path(__file__).parent / f'dictionary/{category}_list.csv'

       with open(list_path, 'r') as f:
           words = np.array([to_array(line.strip()) for line in f])
           np.save(arr_path, words)

    return np.load(arr_path)


def play():
    """Play Wordle yourself!"""
    import gym
    import gym_wordle
    
    env = gym.make('Wordle-v0')  # load the environment
    
    env.reset()
    solution = to_english(env.unwrapped.solution_space[env.solution]).upper()  # no peeking!

    done = False
    
    while not done:
        action = -1 

        # in general, the environment won't be forgiving if you input an
        # invalid word, but for this function I want to let you screw up user
        # input without consequence, so just loops until valid input is taken
        while not env.action_space.contains(action):
            guess = input('Guess: ')
            action = env.unwrapped.action_space.index_of(to_array(guess))
    
        state, reward, done, info = env.step(action)
        env.render()
    
    print(f"The word was {solution}")


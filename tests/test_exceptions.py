'''
    Tests for exceptions.py
'''
import pytest

from exceptions import Impossible, QuitWithoutSaving


def test_impossible_is_raisable_as_an_exception():
    ''' Impossible should behave like a normal raisable exception '''
    with pytest.raises(Impossible):
        raise Impossible("cannot do that")


def test_quit_without_saving_is_a_system_exit():
    ''' QuitWithoutSaving should be a SystemExit so it skips save-on-exit '''
    assert issubclass(QuitWithoutSaving, SystemExit)

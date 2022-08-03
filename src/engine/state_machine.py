import enum

from src.managers.event_manager import *


class StateMachine(object):
    """
    Stack-based state machine.
    peek() allow to witness the current state.
    pop() removes the current state from the stack.
    push() add new state on top of the stack.
    """

    class State(enum.Enum):
        # STATES CONST VALUES
        MAIN_MENU = 0,
        MAIN_GAME = 1,
        PAUSE = 2

    def __init__(self, event_manager: EventManager):
        self._event_manager = event_manager
        self._event_manager.register_listener(self)

        self._states_stack = []
        # Allow/Forbid the state machine to push multiple times the same state on top of each other.
        self.allow_similar_state_stacking = False

    def notify(self, event: Event):
        # Mandatory to allow the state machine to send events
        pass

    def on_state_changed(self):
        """ Sends an new event to the event manager everytime an event is popped or pushed. """
        self._event_manager.post(StateChangeEvent(self.peek()))

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if it is currently empty.
        """
        try:
            return self._states_stack[-1]
        except IndexError:
            return None

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if it is currently empty.
        """
        try:
            self._states_stack.pop()
            self.on_state_changed()
            return len(self._states_stack) > 0
        except IndexError:
            return None

    def push(self, state: State):
        """ Appends a new state in the stack. """
        # Compare the current state and the new state. If they are similar, do not push it.
        if not self.allow_similar_state_stacking:
            if state != self.peek():
                self._states_stack.append(state)
            else:
                print("Couldn't push the same state twice.")
        else:
            self._states_stack.append(state)
        self.on_state_changed()

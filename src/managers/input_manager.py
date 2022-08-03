from dataclasses import dataclass
from typing import Optional

from src.managers.event_manager import *


class InputManager(object):
    """
    The input manager receives symbols from the Engine (arcade input methods).
    withhold input data, implement some logic (pressed button, dragged mouse) and send events
    based on the received inputs.
    """

    class InputData(object):
        """ Stores input data of a key everytime engine.py fires an input. """

        def __init__(self, symbol: int, modifier: int):
            # Int used as an ID to identify the key pressed.
            self.symbol = symbol
            # Is pressed state. By default, always False.
            self.hold = False
            # Bitwise ‘and’ of all modifiers (shift, ctrl, num lock) pressed during this event.
            self.modifier = modifier

        def __eq__(self, other):
            # Checks if another InputData class holds the same symbol
            return self.symbol == other

        def __str__(self):
            return 'Input {self.symbol}, hold = {self.hold}'.format(self=self)

    @dataclass
    class Mouse:
        button: int = None
        coords: tuple = (0, 0)
        coords_buffer: tuple = (0, 0)
        down: bool = False

    def __init__(self, event_manager: EventManager):

        # --- Managers ---
        self._event_manager = event_manager
        self._event_manager.register_listener(self)

        # --- Symbols/Keys References ---
        self._input_data_queue: Optional[list[InputManager.InputData]] = []

        # --- Mouse References ---
        self._mouse = InputManager.Mouse()

    @property
    def mouse_screen_position(self) -> tuple:
        """ Return the current X and Y position of the mouse """
        return self._mouse.coords

    def notify(self, event: Event):
        """ Default 'notify' method for all registered listeners of the event manager. """

        if isinstance(event, TickEvent):
            # --- KEYBOARD INPUTS ---
            for input in self._input_data_queue:
                self._event_manager.post(InputEvent(input.symbol, input.modifier, input.hold))
                # Changes the status to down after one event is fired.
                input.hold = True

            # --- MOUSE INPUTS ---
            if self._mouse.button is not None:
                # Compare the buffer to the actual mouse coordinates.
                if self._mouse.coords_buffer is not None:
                    if self._mouse.coords_buffer[0] != self._mouse.coords[0] \
                            or self._mouse.coords_buffer[1] != self._mouse.coords[1]:
                        # If there is a difference, sends a drag event
                        self._event_manager.post(MouseInputEvent(self._mouse.button, self._mouse.coords[0],
                                                                 self._mouse.coords[1], True,
                                                                 self._mouse.down))
                    else:
                        # Else, same event without the drag
                        self._event_manager.post(MouseInputEvent(self._mouse.button, self._mouse.coords[0],
                                                                 self._mouse.coords[1], False,
                                                                 self._mouse.down))

                # Update the mouse coordinates buffer after an event was fired.
                self._mouse.coords_buffer = self._mouse.coords

                # Set the mouse_down to True to avoid multiple calls but still allows for mouse position and drag
                # update.
                self._mouse.down = True

    def assert_input_data(self, symbol: int, modifier: int):
        i_data = InputManager.InputData(symbol, modifier)
        self._input_data_queue.append(i_data)

    def remove_input_data(self, symbol: int):
        for input in self._input_data_queue:
            if input == symbol:
                self._input_data_queue.remove(input)

    def update_mouse(self, button: int, x: int, y: int):
        self._mouse.button = button
        self._mouse.coords = (x, y)

    def reset_mouse(self, mouse_button):
        self._mouse.button = None
        self._mouse.coords_buffer = None
        self._mouse.down = False

        # Send an event anytime any mouse button is released
        self._event_manager.post(ReleaseMouseEvent(mouse_button))

    def update_mouse_coords(self, x: int, y: int):
        self._mouse.coords = (x, y)

    def update_mouse_wheel(self, value: int):
        self._event_manager.post(MouseWheelEvent(value))

import abc
import arcade
from typing import Optional

from src.managers.event_manager import *
from src.engine.state_machine import StateMachine


class Viewport(object):
    """
    Viewport superclass. Every viewport used should derive from this base class.
    Implement event_manager methods as well as some commonly used methods (viewport_draw, viewport_inputs).
    """
    def __init__(self, engine):
        self.window_size = engine.window_size

        # --- Managers / Singleton ---
        self._engine = engine
        self._event_manager = engine.event_manager
        self._event_manager.register_listener(self)

        # --- Cameras ---
        self._camera = arcade.Camera(self.window_size[0], self.window_size[1])
        self._camera_gui = arcade.Camera(self.window_size[0], self.window_size[1])

        # --- State Machine Params ---
        self._current_state: Optional[StateMachine.State] = None
        # The link state is used to determine whether this a viewport subclass should be in use right now
        self._linked_state: Optional[StateMachine.State] = None

    @abc.abstractmethod
    def notify(self, event: Event):
        """
        Super Method 'notify' is tied to the event manager. The base implementation takes in charge the initialisation
        of the viewport, as well as the drawing and viewport-related inputs.
        """
        # Fetch the current state of the engine.py state machine.
        self._current_state = self._engine.state_machine.peek()

        if isinstance(event, InitializeEvent):
            self.initialize()

        if self._current_state == self._linked_state:
            if isinstance(event, InputEvent):
                self.viewport_inputs(event)
            if isinstance(event, DrawEvent):
                self.viewport_draw()

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def viewport_draw(self):
        arcade.start_render()
        self._camera_gui.use()
        self.dev_guizmo()

    @abc.abstractmethod
    def viewport_inputs(self, event: Event):
        pass

    def dev_guizmo(self):
        # Current state of the state machine.
        arcade.draw_text(str(self._current_state), 10, self.window_size[1] - 50, arcade.color.GREEN, 14,
                         anchor_x="left", anchor_y="baseline")
        # Delta Time.
        dt_string = f"Δt: {round(self._engine.delta_time, 5)}"
        arcade.draw_text(dt_string, 10, self.window_size[1] - 30, arcade.color.GREEN_YELLOW, 16)

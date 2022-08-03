import arcade

from src.managers.event_manager import *
from src.managers.input_manager import InputManager
from src.engine.state_machine import StateMachine
from src.viewports.viewport_menu import ViewportMainMenu
from src.viewports.viewport_game import ViewportMainGame


class Engine(arcade.Window):
    def __init__(self, cfg_dat: dict, title, input_manager: InputManager, event_manager: EventManager):
        super().__init__(width=cfg_dat.get('video').get('width'),
                         height=cfg_dat.get('video').get('height'),
                         title=title,
                         resizable=False,
                         fullscreen=cfg_dat.get('video').get('full_screen'),
                         vsync=cfg_dat.get('video').get('v_sync'),
                         antialiasing=cfg_dat.get('video').get('anti_aliasing'))

        # Config .yaml file
        self.cfg = cfg_dat

        # --- MANAGERS ---
        self.event_manager = event_manager
        self.event_manager.register_listener(self)
        self._input_manager = input_manager

        # --- INSTANCES ---
        # --- Main Components ---
        self.state_machine = StateMachine(self.event_manager)
        # --- ViewPorts ---
        self.viewports = (ViewportMainMenu(self), ViewportMainGame(self))

        # --- Engine Params ---
        self._running = False
        self.delta_time = 0.0

    @property
    def window_size(self) -> tuple:
        return self.width, self.height

    def starter(self):
        """
        First method called from __main__.py. Push the InitializeEvent() to the event_manager
        to initialize all listeners.
        Push the first State to the State Machine.
        At last, run arcade.
        """
        self.set_mouse_visible(True)
        # Post the InitializeEvent() to initialize all the listeners.
        self.event_manager.post(InitializeEvent())
        # Push the first state of the state machine and post the concordant event.
        self.state_machine.push(StateMachine.State.MAIN_MENU)
        # Use the peek function to push the new (last added) state to the event manager.
        self.event_manager.post(StateChangeEvent(self.state_machine.peek()))

        self._running = True
        print('Engine initialized. Launching Arcade.')

        # Initialize Arcade Library, always in last.
        arcade.run()

    def notify(self, event: Event):
        """
        As the registered instance, the Engine will be notified by the event manager each time a new event is pushed
        to the events' queue. Each listener has a different implement of the notify method which encompass their
        purposes and often calls methods within the class.
        """
        # Last event to be called before the program closes.
        if isinstance(event, QuitEvent):
            self._running = False
            arcade.exit()

        # Input based event (exclusively Keyboard)
        if isinstance(event, InputEvent):
            # On Key Down. (only triggers once when the key is pressed).
            if not event.pressed:
                # Escape Key.
                if event.symbol == 65307:
                    self.state_machine.pop()
                # Space bar Key.
                if event.symbol == 32:
                    # If we are not in the current running state.
                    # self.state_machine.push(StateMachine.State.MAIN_GAME)
                    pass

        if isinstance(event, StateChangeEvent):
            # If the states stack is empty, quit the program.
            if self.state_machine.peek() is None:
                self.event_manager.post(QuitEvent())

    def on_update(self, delta_time: float):
        # Each update, send an Event.TickEvent that will allow listeners of the event manager to update themselves.
        if self._running:
            self.delta_time = delta_time
            self.event_manager.post(TickEvent(delta_time))

    def on_draw(self):
        if self._running:
            self.event_manager.post(DrawEvent())

    # region --- Arcade Input Methods 2 Input Manager ---

    def on_key_press(self, symbol: int, modifiers: int):
        """ Create a new InputManager.InputData """
        self._input_manager.assert_input_data(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        """ Remove the InputData from the Input Manager queue """
        self._input_manager.remove_input_data(symbol)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ Assert button and mouse coordinates """
        self._input_manager.update_mouse(button, x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """ Reset mouse, the coordinates buffer and send an event from the Input Manager """
        self._input_manager.reset_mouse(button)

    def on_mouse_motion(self, x: int, y: int, dx: float, dy: float):
        """ Solely updates mouse screen coordinates """
        self._input_manager.update_mouse_coords(x, y)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """ Sends a scroll wheel event from the Input Manager """
        self._input_manager.update_mouse_wheel(scroll_y)

    # endregion

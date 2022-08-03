from abc import ABC
from typing import Optional

import arcade

from src.managers.event_manager import *
from src.engine.state_machine import StateMachine
from src.engine.viewport import Viewport


class MenuEntry(object):
    def __init__(self, name: str, linked_state: StateMachine.State):
        self.name = name
        self.state = linked_state
        self.screen_position: Optional[tuple] = (0, 0)


class MenuSelector:
    def __init__(self, viewport: Viewport, entries: list[MenuEntry]):
        # --- Managers / Singletons ---
        self.viewport = viewport

        # --- Menus Entries ---
        self.entries = entries
        self.selector_index = 0

        # --- Figure out positions for the menu entries ---
        for index, entry in enumerate(self.entries):
            position = (self.viewport.window_size[0] // 2, (self.viewport.window_size[1] // 2) - index * 50)
            entry.screen_position = position

    @property
    def current_state(self):
        return self.entries[self.selector_index].state

    def update_index(self, value: int):
        new_index = self.selector_index + value
        if new_index <= 0:
            self.selector_index = 0
        elif new_index >= (len(self.entries) - 1):
            self.selector_index = (len(self.entries) - 1)
        else:
            self.selector_index = new_index
        print(new_index)
        print(len(self.entries))

    def draw_menu(self):
        for entry in self.entries:
            arcade.draw_text(str(entry.name), entry.screen_position[0], entry.screen_position[1],
                             arcade.color.WHITE_SMOKE, 24, anchor_x='center')

        # Draw the selector based on the current index
        selector_position = self.entries[self.selector_index].screen_position
        selector_width = len(self.entries[self.selector_index].name) * 24
        selector_height = 24 * 1.35
        arcade.draw_rectangle_outline(selector_position[0], selector_position[1] + 12,
                                      selector_width,
                                      selector_height, arcade.color.WHITE, border_width=2)


class ViewportMainMenu(Viewport, ABC):
    def __init__(self, engine):
        super().__init__(engine)
        # --- Engine's State that allow this viewport to update itself. ---
        self._linked_state = StateMachine.State.MAIN_MENU

        # --- Menu Constructs ---
        self.menu_entries: Optional[list[MenuEntry]] = []
        self.selector: Optional[MenuSelector] = None

    def initialize(self):
        self.menu_entries = [MenuEntry('PLAY', StateMachine.State.MAIN_GAME),
                             MenuEntry('OPTIONS', StateMachine.State.MAIN_GAME),
                             MenuEntry('THIS IS JUST A TEST.', StateMachine.State.MAIN_GAME),
                             MenuEntry('CREDITS', StateMachine.State.MAIN_GAME)]

        self.selector = MenuSelector(self, self.menu_entries)

    def viewport_draw(self):
        super().viewport_draw()
        self.selector.draw_menu()

    def viewport_inputs(self, event: InputEvent):
        # On Key Down. (only triggers once when the key is pressed).
        if not event.pressed:
            # W Key
            if event.symbol == 119:
                self.selector.update_index(-1)
            # S Key
            if event.symbol == 115:
                self.selector.update_index(1)
            # Space bar Key
            if event.symbol == 32:
                state = self.selector.current_state
                self._engine.state_machine.push(state)

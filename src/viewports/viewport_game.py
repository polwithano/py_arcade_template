from abc import ABC

import arcade

from src.engine.state_machine import StateMachine
from src.engine.viewport import Viewport


class ViewportMainGame(Viewport, ABC):
    def __init__(self, engine):
        super().__init__(engine)
        # --- Engine's State that allow this viewport to update itself. ---
        self._linked_state = StateMachine.State.MAIN_GAME

    def initialize(self):
        pass

    def viewport_draw(self):
        super().viewport_draw()

        arcade.draw_text('GAME', self.window_size[0] // 2, self.window_size[1] // 2,
                         arcade.color.WHITE_SMOKE, 24, anchor_x='center')

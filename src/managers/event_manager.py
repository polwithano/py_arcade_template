class Event(object):
    """
    A superclass for any events that might be generated bu
    an object and sent to the event manager
    """
    def __init(self):
        self.name = "Event Name"

    def __str__(self):
        return self.name


class TickEvent(Event):
    """ Posted by the arcade.Window class each update loop. (on_update method) """
    def __init__(self, dt: float):
        self.name = "Tick Event"
        self.dt = dt


class DrawEvent(Event):
    """ Posted by the arcade.Window class each update loop. (on_draw method) """
    def __init__(self):
        self.name = "Draw Event"


class InitializeEvent(Event):
    """
    Initialize all registered listener that implement the method init.
    This includes loading libraries and resources.

    Avoid initializing such things within listener __init__ calls
    to minimize snafus (if some rely on others being yet created.)
    """
    def __init__(self):
        self.name = "Initialize Event"


class QuitEvent(Event):
    """ Last Event to be called before the program is closed"""
    def __init__(self):
        self.name = "Quit Event"


class InputEvent(Event):
    """
    Keyboard input event.
    """
    def __init__(self, int_key, modifier, is_pressed: bool):
        self.name = "Input Key"
        self.symbol = int_key
        self.modifier = modifier
        self.pressed = is_pressed

    def __str__(self):
        return '%s [char=%s, hold=%s, mod=%s]' % (self.name, self.symbol, self.pressed, self.modifier)


class MouseInputEvent(Event):
    """ Mouse input event. """
    def __init__(self, button: int, x: int, y: int, drag: bool, press: bool):
        self.name = "Input Mouse"
        self.button = button
        self.x = x
        self.y = y
        self.drag = drag
        self.pressed = press

    def __str__(self):
        return "B%s [(%s, %s), hold=%s, drag=%s]" % (self.button, self.x, self.y, self.pressed, self.drag)


class MouseWheelEvent(Event):
    """ Returns the new scroll value of the scroll wheel. """
    def __init__(self, wheel_value: int):
        self.wheel_value = wheel_value

    def __str__(self):
        return "scroll value = %s" % self.wheel_value


class ReleaseMouseEvent(Event):
    """ Send when mouse button is released. """
    def __init__(self, button_released: int):
        self.button = button_released
        self.name = "Release Mouse Event"

    def __str__(self):
        return "released button = %s" % self.button


class StateChangeEvent(Event):
    """
    Change the model state machine.
    Given a None state will pop() instead of push.
    """

    def __init__(self, state):
        self.name = "State Change Event"
        self.state = state

    def __str__(self):
        if self.state:
            return '%s pushed %s' % (self.name, self.state)
        else:
            return '%s popped' % self.name


class EventManager(object):
    """
    Coordinate communication between Model, View and Controller
    """

    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def register_listener(self, listener):
        """
        Adds a listener to our spam list.
        It will receive Post()ed events through it's notify(event) call.
        """

        self.listeners[listener] = 1

    def unregister_listener(self, listener):
        """
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """

        if listener in self.listeners.keys():
            del self.listeners[listener]

    def post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """

        # Don't print the redundant Tick Event.
        if not isinstance(event, TickEvent) and not isinstance(event, DrawEvent):
            print(event)

        # Broadcast the event to all subscribed listeners.
        for listener in self.listeners.copy().keys():
            listener.notify(event)

class Observable:
    """Wrap a value in an object that can be monitored for changes.
    If the value changes, notify all the listeners of the object.
    """

    def __init__(self, initial_value = None):
        self._value = initial_value
        self.observers = set()

    def get_value(self):
        return self._value

    def set_value(self, value):
        if self._value != value:
            self._value = value
            self.notify()

    def subscribe(self, handler_function):
        if not callable(handler_function):
            raise Exception('subscribe() must take a function')

        self.observers.add(handler_function)

    def unsubscribe(self, handler_function):
        self.observers.remove(handler_function)

    def notify(self):
        for observer in self.observers:
            observer(self._value)
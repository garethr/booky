"Utility class for booky. Used to manage registration and loading of callbacks"

class Builder:
    """
    A basic processing queue. Register a series of callback functions
    and then call run to execute them in the order they where registered.
    All callbacks should take and return a string, allowing for chained text
    processing
    """
    
    def __init__(self):
        "Start off with no callbacks and no content"
        self.callbacks = []
        self.content = ""
    
    def register(self, callback):
        "Registers a callback into the callback queue"
        if callback not in self.callbacks:
            self.callbacks.append(callback)
            return True
        else:
            return False, "A callback called '%s' has already been "\
                "registered" % callback

    def get_callbacks(self):
        "Returns the list of callbacks"
        return self.callbacks
        
    def run(self):
        "Note no return value as all output is done via callbacks"
        for callback in self.callbacks:
            self.content = callback(self.content)
class player:

    def __init__(self):
        self.on = False
        self.timer = False

    
    def switch_on(self, value):
        self.on = value

    def get_on(self):
        return self.on
    
    def start_timer(self):
        self.timer = True

    def stop_timer(self):
        self.timer = False

    def get_timer(self):
        return self.timer    
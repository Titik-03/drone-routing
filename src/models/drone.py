class Drone:
    def __init__(self, id, path, departure):
        self.id = id
        self.path = path              
        self.departure = departure    
        self.current_zone = path[0]   
        self.step = 0
        self.arrived = False
        self.in_transit = False
        self.waiting_turns = 0        
    def __repr__(self):
        return (
            f"Drone({self.id}), "
            f"path= {self.path}, turn {self.departure} \n"
        )
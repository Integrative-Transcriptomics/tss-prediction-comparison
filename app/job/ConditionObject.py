import uuid

class ConditionObject:
    def __init__(self, name, forward_id, backward_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.forward_id = forward_id
        self.backward_id = backward_id

    def get_jobids(self):
        return self.forward_id, self.backward_id
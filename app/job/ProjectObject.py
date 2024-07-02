import uuid

class ProjectObject:
    def __init__(self, project_name, condition_dict):
        self.id = str(uuid.uuid4())
        self.project_name = project_name
        self.condition_registry = condition_dict

    def get_conditions(self):
        return self.condition_registry
class Departamento:
    def __init__(self, department_id, display_name):
        self.department_id = department_id
        self.display_name = display_name

    def show(self):
        print(f"ID: {self.department_id} - Departamento: {self.display_name}")
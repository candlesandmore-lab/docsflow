
from python.gui.model import Model
from python.gui.projectTreeController import ProjectTreeController
from python.gui.view import View


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.projectTreeController = ProjectTreeController(model, view)
        
        self.model.projectModel.add_event_listener(
            "projectNodeChanged", self.projectTreeController.setProjectNode
        )

    def start(self) -> None:
        self.view.startMainloop()

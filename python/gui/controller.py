
from python.gui.model import Model
from python.gui.nodeViewController import NodeViewController
from python.gui.projectTreeController import ProjectTreeController
from python.gui.view import View


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.projectTreeController = ProjectTreeController(model, view)
        self.nodeViewController = NodeViewController(model, view)
        
        self.model.projectModel.add_event_listener(
            "projectNodeChanged", self.setProjectNode
        )
        self._bind()

    # bind events that occure in one controller and need action in another controller
    def _bind(self):
        # TODO: bind selection in tree to to nodeSelected
        self.view.frames['tree'].treeview.bind(
            '<<TreeviewSelect>>', 
            self.treeNodeSelected
        )

    # update detail view if tree node is selected
    def treeNodeSelected(self, event):
        frame_id = self.view.frames['tree'].treeview.selection()
        # frame_id is tuple('<node.name>', )
        #self.display_frame.change_frame(frame_id)
        print("*DEB* : selected [{}]".format(frame_id[0]))
        newFocusNode = self.model.projectModel.getNodeByUUID(frame_id[0])

        self.nodeViewController.parentChanged(newFocusNode)

    # new project selected in model
    def setProjectNode(self, model : Model) -> None:
        self.nodeViewController.setProjectNode(model)
        self.projectTreeController.setProjectNode(model)

    def start(self) -> None:
        self.view.startMainloop()

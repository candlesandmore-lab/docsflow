
from python.gui.model import Model
from python.gui.view import View


class ProjectTreeController():
    def __init__(self, model : Model, view : View) -> None:
        self.model = model
        self.view = view
        self._bind()

    def _bind(self):
        # TODO: bind selection in tree to to nodeSelected
        self.view.frames['tree'].treeview.bind(
            '<<TreeviewSelect>>', 
            self.nodeSelected
        )

    def nodeSelected(self, event):
        # TODO: change data in nodeView
        frame_id = self.view.frames['tree'].treeview.selection()
        # frame_id is tuple('<node.name>', )
        #self.display_frame.change_frame(frame_id)
        print("*DEB* : selected [{}]".format(frame_id[0]))

        # TODO: replace all data
        newFocusNode = self.model.projectModel.getNodeByUUID(frame_id[0])
        self.view.frames['details'].nodeData = newFocusNode
        self.view.frames['details'].refresh()

    # TODO: bind to GUI operation
    def setProjectNode(self, model : Model) -> None:
        self.view.frames['tree'].projectData = self.model.projectModel.projectNode
        self.view.frames['tree'].refresh()

        self.view.frames['details'].nodeData = self.model.projectModel.projectNode
        self.view.frames['details'].refresh()



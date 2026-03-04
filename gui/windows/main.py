from functools import partial

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import (
    QDockWidget,
    QLayout,
    QMainWindow,
    QPushButton,
    QToolBar,
    QToolBox,
    QVBoxLayout,
    QWidget,
)
from quantsim.core import Qubit
from quantsim.gates import InverseS

from .widgets.editor.hadamarad import HadamaradCADItem
from .widgets.editor.inverses import InverseSCADItem
from .widgets.editor.pauliy import PauliYCADItem
from .widgets.editor.pauliz import PauliZCADItem
from .widgets.editor.s import SCADItem
from .widgets.blochsphere import BlochSphere
from .widgets.editor import Editor
from .widgets.editor.caditem import CADItem
from .widgets.editor.editor import Tools
from .widgets.editor.observer import ObserverCADItem
from .widgets.editor.paulix import PauliXCADItem
from .widgets.editor.qubit import QubitCADItem


class MainWindow(QMainWindow):
    docks: dict[str, QDockWidget] = {}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantum Circuit Designer")
        self.setMinimumSize(QSize(1200, 800))
        self.add_widgets()
        self.add_dockables()

        _ = self.editor.qubititem_selected.connect(self.bloch.set_qubit)
        _ = self.editor.observeritem_selected.connect(self.bloch.set_observedvalue)

    def simulate(self):
        self.editor.circuit.calculate()

    def add_widgets(self):
        self.editor: Editor = Editor()
        self.toolbar: QToolBar = QToolBar("Tool Bar")

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_new = QAction("&New", self)
        file_menu.addAction(file_new)

        self.view_menu = menu.addMenu("&View")
        self.simulation_menu = menu.addMenu("&Simulate")
        simulation_action = QAction("Simulate", self)
        simulation_action.triggered.connect(self.simulate)
        self.simulation_menu.addAction(simulation_action)

        wire_action = QAction("&Wire tool", self.toolbar)
        _ = wire_action.triggered.connect(self.wire_selected)
        self.toolbar.addAction(wire_action)
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.editor)

    def wire_selected(self) -> None:
        if self.editor.tool == Tools.WIRE:
            self.editor.tool = Tools.NONE
        else:
            self.editor.set_tool(Tools.WIRE)
        self.editor.cadItem = None

    def item_selected(self, caditem: type[CADItem]) -> None:
        if self.editor.tool == Tools.PLACE:
            if self.editor.cadItem.__class__ != caditem:
                self.editor.cadItem = caditem()
            else:
                self.editor.tool = Tools.NONE
        else:
            self.editor.set_tool(Tools.PLACE)
            self.editor.cadItem = caditem()

    def add_dockables(self):
        """
        adds dockable widgets to the main window

        :param self: Description
        """
        toolboxdock = QDockWidget("Tool box")
        blochsphere = QDockWidget("Bloch Sphere")
        self.toolbox: QToolBox = QToolBox()
        self.toolbox.setMinimumWidth(100)

        core_page = QWidget()
        core_grid = QVBoxLayout()
        core_grid.setContentsMargins(0, 0, 0, 0)
        core_grid.setSpacing(0)
        core_page.setLayout(core_grid)

        gates_page = QWidget()
        gates_grid = QVBoxLayout()
        gates_page.setLayout(gates_grid)

        def add_buttons(itemtypes: list[type[CADItem]], layout: QLayout):
            for i in range(len(itemtypes)):
                button = QPushButton()
                button.setText(itemtypes[i].__name__.removesuffix("CADItem"))

                ico = QPixmap(itemtypes[i]().path).scaled(QSize(64, 64))  # pyright: ignore[reportCallIssue, reportAttributeAccessIssue, reportUnknownArgumentType]
                button.setIcon(ico)
                button.setIconSize(QSize(64, 64))

                _ = button.clicked.connect(partial(self.item_selected, itemtypes[i]))
                layout.addWidget(button)

        add_buttons(
            [QubitCADItem, ObserverCADItem],
            core_grid,
        )
        add_buttons(
            [
                PauliXCADItem,
                PauliYCADItem,
                PauliZCADItem,
                HadamaradCADItem,
                SCADItem,
                InverseSCADItem,
            ],
            gates_grid,
        )

        _ = self.toolbox.addItem(core_page, "Core")
        _ = self.toolbox.addItem(gates_page, "Gates")

        self.bloch = BlochSphere()
        self.bloch.setMinimumWidth(400)
        blochsphere.setWidget(self.bloch)
        toolboxdock.setWidget(self.toolbox)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, toolboxdock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, blochsphere)

        view_toolbox = toolboxdock.toggleViewAction()
        view_bloch = blochsphere.toggleViewAction()
        self.view_menu.addActions([view_bloch, view_toolbox])
        self.docks["toolbox"] = toolboxdock
        self.docks["bloch"] = blochsphere

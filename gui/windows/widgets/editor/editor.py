from enum import Enum
from math import isclose
from typing import override

from PySide6 import QtGui
from PySide6.QtCore import QPointF, QRect, QRectF, Qt, Signal
from PySide6.QtGui import (
    QAction,
    QKeyEvent,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QGraphicsView,
    QMenu,
)
from quantsim.circuit.circuit import Circuit
from quantsim.circuit.observer import Observer
from quantsim.core import Qubit

from .observer import ObserverCADItem

from .caditem import CADItem
from .paulix import PauliXCADItem
from .qubit import QubitCADItem


class Tools(Enum):
    NONE = 0
    WIRE = 1
    PLACE = 3


class Editor(QGraphicsView): ...


class GraphicsCanvas(QGraphicsScene):
    previous_click: QPointF
    current_pos: QPointF
    editor: Editor
    selected_caditem: CADItem | None = None
    selected_input: bool | None = None
    temp_paths: list[QGraphicsItem] = []
    temp_caditems: list[CADItem] = []
    wires: list[QGraphicsItem] = []
    cad_items: list[CADItem] = []
    first_press: bool = True

    def __init__(self, editor: Editor) -> None:
        super().__init__()
        self.editor = editor
        self.setBackgroundBrush(Qt.GlobalColor.white)

    def add_caditem(self, item: CADItem) -> None:
        self.addItem(item)
        self.cad_items.append(item)
        self.editor.circuit.add(item.component())

    def snap(self, pos: QPointF) -> QPointF:
        for caditem in self.cad_items:
            if caditem.input:
                _pos = caditem.mapToScene(caditem.input)
                if isclose(_pos.x(), pos.x(), rel_tol=1e-2) and isclose(
                    _pos.y(), pos.y(), rel_tol=1e-2
                ):
                    return _pos
            elif caditem.output:
                _pos = caditem.mapToScene(caditem.output)
                if (
                    _pos
                    and isclose(_pos.x(), pos.x(), rel_tol=1e-2)
                    and isclose(_pos.y(), pos.y(), rel_tol=1e-2)
                ):
                    return _pos

        point = pos.toPoint()
        if point.x() % 100 < 15:
            point.setX(point.x() - point.x() % 100)

        if point.y() % 100 < 15:
            point.setY(point.y() - point.y() % 100)

        return point.toPointF()

    @override
    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent, /) -> None:
        for item in self.cad_items:

            def selected_input():
                self.selected_input = True
                self.selected_caditem = item

            def selected_ouput():
                self.selected_input = False
                self.selected_caditem = item

            def connect_input():
                assert self.selected_caditem is not None
                assert self.selected_caditem.outputItems is not None
                assert item.inputItems is not None

                assert self.selected_caditem.output is not None
                assert item.input is not None

                input_pos = item.mapToScene(item.input)
                output_pos = self.selected_caditem.mapToScene(
                    self.selected_caditem.output
                )

                self.selected_caditem.outputItems.append(item)
                item.inputItems.append(self.selected_caditem)
                self.selected_caditem.component().connect_ouput(item.component())
                self.draw_wire(output_pos, input_pos)

            def connect_output():
                assert self.selected_caditem is not None
                assert self.selected_caditem.inputItems is not None
                assert item.outputItems is not None

                assert self.selected_caditem.input is not None
                assert item.output is not None

                input_pos = self.selected_caditem.mapToScene(
                    self.selected_caditem.input
                )
                output_pos = item.mapToScene(item.output)

                self.selected_caditem.inputItems.append(item)
                item.outputItems.append(self.selected_caditem)
                self.selected_caditem.component().connect_input(item.component())
                self.draw_wire(input_pos, output_pos)

            if item.contains(item.mapFromScene(event.scenePos())):
                menu = QMenu(title="Editor menu")
                if (
                    self.selected_caditem is not None
                    and self.selected_caditem is not item
                ):
                    connect_menu = menu.addMenu("Connect")
                    if item.inputItems is not None:
                        connect_input_action = QAction(text="input")
                        _ = connect_input_action.triggered.connect(connect_input)
                        connect_menu.addAction(connect_input_action)
                    if item.outputItems is not None:
                        connect_output_action = QAction("ouput")
                        _ = connect_output_action.triggered.connect(connect_output)
                        connect_menu.addAction(connect_output_action)
                else:
                    select_menu = menu.addMenu("Select")
                    if item.inputItems is not None:
                        select_input_action = QAction(text="input")
                        _ = select_input_action.triggered.connect(selected_input)
                        select_menu.addAction(select_input_action)
                    if item.outputItems is not None:
                        select_output_action = QAction(text="output")
                        _ = select_output_action.triggered.connect(selected_ouput)
                        select_menu.addAction(select_output_action)
                _ = menu.exec(event.screenPos())

    @override
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        # remove temp items
        paths = len(self.temp_paths)
        for _ in range(paths):
            self.removeItem(self.temp_paths.pop())

        items = len(self.temp_caditems)
        for _ in range(items):
            self.removeItem(self.temp_caditems.pop())
        self.invalidate()
        match self.editor.tool:
            case Tools.WIRE:
                path = QPainterPath()

                if not self.first_press:
                    path.moveTo(self.snap(self.previous_click))
                    pos = self.snap(event.scenePos())
                    if abs(pos.x()) >= abs(pos.y()):
                        path.lineTo(QPointF(pos.x(), self.previous_click.y()))
                        path.moveTo(QPointF(pos.x(), self.previous_click.y()))
                        path.lineTo(QPointF(pos.x(), pos.y()))
                    else:
                        path.lineTo(QPointF(self.previous_click.x(), pos.y()))
                        path.moveTo(QPointF(self.previous_click.x(), pos.y()))
                        path.lineTo(QPointF(pos.x(), pos.y()))

                    self.temp_paths.append(self.addPath(path))

            case Tools.PLACE:
                self.first_press = True
                if self.editor.cadItem:
                    self.editor.cadItem.setPos(
                        QPointF(
                            event.scenePos().toPoint().x() - 32,
                            event.scenePos().toPoint().y() - 32,
                        )
                    )
                    self.addItem(self.editor.cadItem)
                    self.temp_caditems.append(self.editor.cadItem)
                    self.editor.cadItem = type(self.editor.cadItem)()

            case Tools.NONE:
                pass

    def draw_wire(self, p1: QPointF, p2: QPointF):
        path = QPainterPath()
        p1 = self.snap(p1)
        p2 = self.snap(p2)

        path.moveTo(p1)

        if abs(p2.x()) >= abs(p2.y()):
            path.lineTo(QPointF(p2.x(), p1.y()))

            path.moveTo(QPointF(p2.x(), p1.y()))
            path.lineTo(QPointF(p2.x(), p2.y()))
        else:
            path.lineTo(QPointF(p1.x(), p2.y()))

            path.moveTo(QPointF(p1.x(), p2.y()))
            path.lineTo(QPointF(p2.x(), p2.y()))

        self.wires.append(self.addPath(path))

    @override
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        match self.editor.tool:
            case Tools.WIRE:
                if self.first_press:
                    self.previous_click = event.scenePos()
                    self.first_press = False

                else:
                    self.draw_wire(self.previous_click, event.scenePos())
                    self.first_press = True

            case Tools.PLACE:
                if self.editor.cadItem:
                    self.editor.cadItem.setPos(
                        QPointF(
                            event.scenePos().toPoint().x() - 32,
                            event.scenePos().toPoint().y() - 32,
                        )
                    )
                    self.add_caditem(self.editor.cadItem)
                    self.editor.cadItem = type(self.editor.cadItem)()

            case Tools.NONE:
                for item in self.cad_items:
                    if item.contains(item.mapFromScene(event.scenePos())):
                        self.selected_caditem = item

                        if isinstance(self.selected_caditem, QubitCADItem):
                            self.editor.qubititem_selected.emit(
                                self.selected_caditem.qubit
                            )
                        elif isinstance(self.selected_caditem, ObserverCADItem):
                            if self.selected_caditem.observer.value is not None:
                                self.editor.observeritem_selected.emit(
                                    self.selected_caditem.observer
                                )


class Editor(QGraphicsView):
    """
    Custom editor widget which draws all the symbols and connections
    """

    tool: Tools = Tools.NONE
    cadItem: CADItem | None = None
    grid_step: int = 100
    grid_pen: QPen = QPen(Qt.GlobalColor.lightGray)
    qubititem_selected: Signal = Signal(Qubit)
    observeritem_selected: Signal = Signal(Observer)
    circuit: Circuit = Circuit()
    _scene: GraphicsCanvas

    def __init__(self):
        self._scene = GraphicsCanvas(self)

        super().__init__(self._scene)
        self.setGeometry(QRect(0, 0, 800, 600))
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)

    def set_tool(self, tool: Tools) -> None:
        self.tool = tool

    @override
    def drawBackground(self, painter: QtGui.QPainter, rect: QRectF | QRect, /) -> None:
        painter.translate(0.5, 0.5)
        painter.setPen(self.grid_pen)
        painter.fillRect(rect, Qt.GlobalColor.white)

        rect = rect.toRect() if isinstance(rect, QRectF) else rect
        y = rect.y()
        x = rect.x()

        right = rect.right()
        bottom = rect.bottom()

        top = y
        left = x
        step = self.grid_step

        yrest = y % step
        if yrest:
            y += step - yrest
        for y in range(y, bottom, step):
            painter.drawLine(left, y, right, y)

        xrest = x % step
        if xrest:
            x += step - xrest
        for x in range(x, right, step):
            painter.drawLine(x, top, x, bottom)

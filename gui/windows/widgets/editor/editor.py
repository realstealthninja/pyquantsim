from enum import Enum
from math import isclose
from typing import override
from PySide6 import QtGui
from PySide6.QtCore import QPointF, QRect, QRectF, Qt, Signal
from PySide6.QtGui import (
    QAction,
    QContextMenuEvent,
    QKeyEvent,
    QPainter,
    QPainterPath,
    QPen,
    Qt,
)
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsSceneContextMenuEvent,
    QGraphicsSceneMouseEvent,
    QGraphicsView,
    QMenu,
)
from quantsim.core import Qubit

from .caditem import CADItem
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
    temp_paths: list[QGraphicsItem] = []
    temp_caditems: list[CADItem] = []
    wires: list[QGraphicsItem] = []
    cad_items: list[CADItem] = []
    first_press: bool = True

    def __init__(self, editor: Editor) -> None:
        super().__init__()
        self.editor = editor
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.add_caditem(QubitCADItem())

    def add_caditem(self, item: CADItem) -> None:
        self.addItem(item)
        self.cad_items.append(item)

    def snap(self, pos: QPointF) -> QPointF:
        for caditem in self.cad_items:
            _pos = caditem.input
            if (
                _pos
                and isclose(_pos.x(), pos.x(), rel_tol=1e-1)
                and isclose(_pos.y(), pos.y(), rel_tol=1e-1)
            ):
                return _pos
            _pos = caditem.output
            if (
                _pos
                and isclose(_pos.x(), pos.x(), rel_tol=1e-1)
                and isclose(_pos.y(), pos.y(), rel_tol=1e-1)
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
            if item.contains(item.mapFromScene(event.scenePos())):
                menu = QMenu(title="Editor menu")
                menu.addAction(QAction(parent=self, text="Connect"))
                _ = menu.exec(event.screenPos())

    @override
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        # remove temp items
        for _ in range(len(self.temp_paths)):
            self.removeItem(self.temp_paths.pop())

        for _ in range(len(self.temp_caditems)):
            self.removeItem(self.temp_caditems.pop())

        print(self.temp_caditems)
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
                    self.editor.cadItem = QubitCADItem()

            case Tools.NONE:
                pass

    @override
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent, /) -> None:
        match self.editor.tool:
            case Tools.WIRE:
                if self.first_press:
                    self.previous_click = event.scenePos()
                    self.first_press = False

                else:
                    path = QPainterPath()
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
                    self.wires.append(self.addPath(path))
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
                    self.editor.cadItem = QubitCADItem()

            case Tools.NONE:
                for item in self.cad_items:
                    if item.contains(item.mapFromScene(event.scenePos())):
                        self.selected_caditem = item

                        if isinstance(self.selected_caditem, QubitCADItem):
                            self.editor.qubititem_selected.emit(
                                self.selected_caditem.qubit
                            )

    @override
    def keyReleaseEvent(self, event: QKeyEvent, /) -> None:
        pass


class Editor(QGraphicsView):
    """
    Custom editor widget which draws all the symbols and connections
    """

    tool: Tools = Tools.NONE
    cadItem: CADItem | None = None
    grid_step: int = 100
    grid_pen: QPen = QPen(Qt.GlobalColor.lightGray)
    qubititem_selected: Signal = Signal(Qubit)
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

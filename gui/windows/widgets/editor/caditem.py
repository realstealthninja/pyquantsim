from typing import override
from PySide6.QtCore import QRectF, QSize, QPointF
from PySide6.QtGui import QPainterPath, QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneHoverEvent
from quantsim.circuit.component import Component


class CADItem(QGraphicsPixmapItem): ...


class CADItem(QGraphicsPixmapItem):
    input: QPointF | None
    output: QPointF | None
    path: str
    inputItems: list[CADItem] | None = None
    outputItems: list[CADItem] | None = None

    def __init__(
        self, path: str, input: QPointF | None, output: QPointF | None
    ) -> None:
        super().__init__(QPixmap(path).scaled(QSize(64, 64)))
        self.path = path
        self.input = input
        self.output = output
        self.setAcceptHoverEvents(True)
        self.setToolTip("Component")

    @override
    def shape(self, /) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def component(self) -> Component: ...

    @override
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent, /) -> None:
        self.setToolTip(self.toolTip())

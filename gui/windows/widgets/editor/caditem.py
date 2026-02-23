from PySide6.QtCore import QSize, QPointF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem


class CADItem(QGraphicsPixmapItem): ...


class CADItem(QGraphicsPixmapItem):
    input: QPointF | None
    output: QPointF | None

    inputItems: list[CADItem] | None = None
    ouputItems: list[CADItem] | None = None

    def __init__(
        self, path: str, input: QPointF | None, output: QPointF | None
    ) -> None:
        super().__init__(QPixmap(path).scaled(QSize(64, 64)))

        self.input = self.mapToScene(input) if input is not None else None
        self.output = self.mapToScene(output) if output is not None else None

        print(self.input)
        print(self.output)

from typing import Any

from PyQt5 import QtCore, QtWidgets

from pyou_ui.custom_widgets import utils
from pyou_ui.img import img


class NavBar(QtWidgets.QFrame):
    def __init__(self, height_: int, style_sheet: Any) -> None:
        super().__init__()

        # Frame Attributes
        self.setFixedHeight(height_)
        self.setStyleSheet(style_sheet.NAVBAR)
        # ----------------

        self.nav_bar_layout = utils.set_horizontal_layout(self)

        # Left Nav Bar
        # A width of 80 is perfect for the left nav bar
        self.left_nav_bar = utils.add_frame(set_width=80)
        self.left_nav_bar_layout = utils.set_horizontal_layout(
            self.left_nav_bar)

        # Hamburger Menu
        self.hamburger_menu = utils.add_button(
            set_height=height_ - 20, set_width=26,
            icon_path=":/hamburger_menu.svg", icon_size=26,
            icon_color=style_sheet.NAVBAR_ICON_COLOR)

        self.left_nav_bar_layout.addWidget(self.hamburger_menu)
        self.nav_bar_layout.addWidget(self.left_nav_bar)
        # ----------------

        # Mid Nav Bar
        self.mid_nav_bar = utils.add_frame()
        self.mid_nav_bar_layout = utils.set_horizontal_layout(
            self.mid_nav_bar)
        self.mid_nav_bar_layout.setAlignment(QtCore.Qt.AlignHCenter)

        # Search Bar
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setFixedHeight(height_ - 20)
        self.search_bar.setPlaceholderText("Search")

        # Search Button
        self.search_button = utils.add_button(
            set_height=height_ - 20, icon_path=":/search_icon.svg",
            icon_size=20, icon_color=style_sheet.NAVBAR_ICON_COLOR,
            style_sheet=style_sheet.NAVBAR_SEARCH_BUTTON_BG_COLOR)

        self.mid_nav_bar_layout.addWidget(self.search_bar)
        self.mid_nav_bar_layout.addWidget(self.search_button)
        self.nav_bar_layout.addWidget(self.mid_nav_bar)
        # ----------------

        # Right Nav Bar
        # A width of 100 is perfect for the right nav bar
        self.right_nav_bar = utils.add_frame(set_width=100)
        self.right_nav_bar_layout = utils.set_horizontal_layout(
            self.right_nav_bar)

        # Vertical Menu
        self.vertical_menu = utils.add_button(
            set_height=height_ - 20, set_width=26,
            icon_path=":/menu_vertical.svg", icon_size=26,
            icon_color=style_sheet.NAVBAR_ICON_COLOR)

        # User Button
        self.user_button = utils.add_button(
            set_height=height_ - 20, set_width=26,
            icon_path=":/user_icon.svg", icon_size=26,
            icon_color=style_sheet.NAVBAR_ICON_COLOR)

        self.right_nav_bar_layout.addWidget(
            self.vertical_menu, alignment=QtCore.Qt.AlignCenter)
        self.right_nav_bar_layout.addWidget(
            self.user_button, alignment=QtCore.Qt.AlignCenter)
        self.nav_bar_layout.addWidget(self.right_nav_bar)
        # ----------------

"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
import time
import webbrowser
from typing import TYPE_CHECKING

from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

from napari_chatgpt.omega.napari_bridge import NapariBridge
from napari_chatgpt.omega.omega_init import initialize_omega_agent

if TYPE_CHECKING:
    import napari

from queue import Queue
from threading import Thread

from arbol import aprint



class OmegaQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Start Omega")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        aprint("Starting Omega!")

        # Instantiates a napari bridge:
        self.bridge = NapariBridge(self.viewer)

        def omega_thread(to_napari_queue: Queue,
                         from_napari_queue: Queue):

            agent_chain = initialize_omega_agent(
                to_napari_queue=to_napari_queue,
                from_napari_queue=from_napari_queue,
                )
            while True:
                query = input()
                if query == 'quit':
                    break
                try:
                    result = agent_chain.run(input=query)
                    aprint(result)
                except Exception as e:
                    return f"Exception: {type(e).__name__} with message: {e.args[0]}"

        # Create and start the thread that will run Omega:
        self.omega_thread = Thread(target=omega_thread,  args=(
        self.bridge.to_napari_queue, self.bridge.from_napari_queue), daemon=True)
        self.omega_thread.start()

        # time.sleep(2)
        # Open browser:
        # url = "http://0.0.0.0:9000 "
        # webbrowser.open(url, new=0, autoraise=True)


"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from deconsim import phantoms
from deconsim.forward import forward
from deconsim.psfs import paraxial_psf
from deconsim.psfs import gibson_lanni_3D
import numpy as np
from qtpy.QtWidgets import QSpinBox, QDoubleSpinBox


class Plugin(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn_2dlines = QPushButton("2D Lines")
        btn_2dlines.clicked.connect(self._on_click_2dlines)

        btn_3dsphere = QPushButton("3D Sphere")
        btn_3dsphere.clicked.connect(self._on_click_3dsphere)

        self.background_sp = QSpinBox()
        self.background_sp.setMinimum(0)
        self.background_sp.setMaximum(1000)
        self.background_sp.setValue(100)
        self.background_sp.valueChanged.connect(self._background_changed)        

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn_2dlines)
        self.layout().addWidget(btn_3dsphere)
        self.layout().addWidget(self.background_sp)

    def _on_click_2dlines(self):
        print("napari has", len(self.viewer.layers), "layers")

        n=512
        spacing_px=4
        wavelength = 500
        na=1.4
        pixel_size = 20

        field = phantoms.lines(n,spacing_px)
        self.field = self.viewer.add_image(field)
        self.psf=paraxial_psf(n, wavelength, na, pixel_size)
        imaged = forward(field, self.psf, 100, self.background_sp.value()) 
        self.imaged=self.viewer.add_image(imaged)

    def _on_click_3dsphere(self):

        size=[50,100,100]
        pixel_size = 0.05

        zv = np.arange(-size[0]*pixel_size/2, size[0]*pixel_size/2, pixel_size)

        field = phantoms.sphere3d(size,20) #rg.sphere(size, 20).astype(np.float32)

        self.field=self.viewer.add_image(field)
        
        self.psf = gibson_lanni_3D(1.4, 1.53, 1.4, pixel_size, 100, zv, 0.1)
        imaged = forward(field, self.psf, 100, self.background_sp.value())
        self.imaged = self.viewer.add_image(imaged)

    def _background_changed(self):
        print(self.background_sp.value())
        imaged = forward(self.field.data, self.psf, 100, self.background_sp.value()) 
        self.imaged.data = imaged

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return Plugin

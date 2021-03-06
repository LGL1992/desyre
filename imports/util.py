import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import *


class Util:
    def __init__(self):
        pass

    @staticmethod
    def cosine_decay(epoch, total, initial=1e-3):
        return initial / 2. * (1 + np.cos(np.pi * epoch / total))

    @staticmethod
    def project(x):
        return np.clip(x, 0, 1)

    @staticmethod
    def psnr(y_true, y_pred):
        return tf.image.psnr(y_true, y_pred, max_val=1.0)

    @staticmethod
    def nmse(y_true, y_pred):
        m = tf.reduce_mean(tf.squared_difference(y_true, y_pred))
        n = tf.reduce_mean(tf.squared_difference(y_true, 0))
        return m / n

    @staticmethod
    def psnr_numpy(x, xhat, maxvalue=1.):
        return 10 * np.log10(maxvalue / np.mean((x - xhat) ** 2))

    @staticmethod
    def nmse_numpy(x, x_hat):
        error = np.mean((x - x_hat) ** 2)
        normalizer = np.mean(x ** 2)
        return error / normalizer

    @staticmethod
    def _mark_inset(parent_axes, inset_axes, **kwargs):
        # This code is copied from the matplotlib source code and slightly modified.
        # This is done to avoid the 'connection lines'.
        rect = TransformedBbox(inset_axes.viewLim, parent_axes.transData)

        if 'fill' in kwargs:
            pp = BboxPatch(rect, **kwargs)
        else:
            fill = bool({'fc', 'facecolor', 'color'}.intersection(kwargs))
            pp = BboxPatch(rect, fill=fill, **kwargs)
        parent_axes.add_patch(pp)

        p1 = BboxConnector(inset_axes.bbox, rect, loc1=1, **kwargs)
        p1.set_clip_on(False)

        p2 = BboxConnector(inset_axes.bbox, rect, loc1=1, **kwargs)
        p2.set_clip_on(False)

        return pp, p1, p2

    def zoomed_plot(self, x, xlim, ylim, zoom=2, text=None, textloc=[], fsize=18, cmap='bone'):

        # This function allows one to create plots with "zoomed in" windows.
        # The rectangle where one desires to zoom in is given using the xlim and ylim arguments.
        # xlim and ylim should contain pixel values, e.g. if we haven an image of size 512 x 512 then
        # xlim = [100, 150] and ylim = [100, 150] shows a zoomed in version of the pixels at locations in xlim and ylim.

        color = 'orange'
        fig, ax = plt.subplots()
        ax.imshow(np.flipud(x), cmap=cmap, vmin=0.0, vmax=1.0, origin="lower")
        ax.axis('off')

        axins = zoomed_inset_axes(ax, zoom, loc=4)

        axins.set_xlim(xlim[0], xlim[1])
        axins.set_ylim(ylim[0], ylim[1])

        self._mark_inset(ax, axins, fc='none', ec=color)

        axins.imshow(np.flipud(x), cmap=cmap, vmin=0.0, vmax=1.0, origin="lower")
        axins.patch.set_edgecolor(color)
        axins.patch.set_linewidth('3')
        axins.set_xticks([], [])
        axins.set_yticks([], [])
        # axins.axis('off')

        if not (text is None):
            ax.text(textloc[0], textloc[1], text, color=color, fontdict={'size': fsize}, transform=ax.transAxes)
        pass

    @staticmethod
    def setup_path(path, verbose=0):
        if not os.path.exists(path):
            os.mkdir(path)

            if verbose:
                print("Created new path %s." % path)

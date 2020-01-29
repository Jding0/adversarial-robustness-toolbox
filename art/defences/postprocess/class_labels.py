# MIT License
#
# Copyright (C) IBM Corporation 2020
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
This module implements class labels added to the classifier output.
"""
import logging

import numpy as np

from art.defences.postprocess.postprocessor import Postprocessor

logger = logging.getLogger(__name__)


class ClassLabels(Postprocessor):
    """
    Implementation of a postprocessor based on adding class labels to classifier output.
    """

    def __init__(self, apply_fit=False, apply_predict=True):
        """
        Create a ClassLabels postprocessor.

        :param apply_fit: True if applied during fitting/training.
        :type apply_fit: `bool`
        :param apply_predict: True if applied during predicting.
        :type apply_predict: `bool`
        """
        super(ClassLabels, self).__init__()
        self._is_fitted = True
        self._apply_fit = apply_fit
        self._apply_predict = apply_predict

    @property
    def apply_fit(self):
        return self._apply_fit

    @property
    def apply_predict(self):
        return self._apply_predict

    def __call__(self, preds):
        """
        Perform model postprocessing and return postprocessed output.

        :param preds: model output to be postprocessed.
        :type preds: `np.ndarray`
        :return: Postprocessed model output.
        :rtype: `np.ndarray`
        """
        class_labels = np.zeros_like(preds)
        if preds.shape[1] > 1:
            index_labels = np.argmax(preds, axis=1)
            class_labels[:, index_labels] = 1
        else:
            class_labels[preds > 0.5] = 1

        return class_labels

    def estimate_gradient(self, x, grad):
        """
        Provide an estimate of the gradients of the defence for the backward pass. If the defence is not differentiable,
        this is an estimate of the gradient, most often replacing the computation performed by the defence with the
        identity function.

        :param x: Input data for which the gradient is estimated. First dimension is the batch size.
        :type x: `np.ndarray`
        :param grad: Gradient value so far.
        :type grad: `np.ndarray`
        :return: The gradient (estimate) of the defence.
        :rtype: `np.ndarray`
        """
        raise NotImplementedError

    def fit(self, preds, **kwargs):
        """
        No parameters to learn for this method; do nothing.
        """
        pass
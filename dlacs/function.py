# -*- coding: utf-8 -*-
"""
Copyright Netherlands eScience Center
Function        : Functions used by the module
Author          : Yang Liu (y.liu@esciencecenter.nl)
First Built     : 2019.07.26
Last Update     : 2020.02.20
Contributor     :
Description     : This scripts provides the basic functions, which will be used by other modules.
Return Values   : time series / array
Caveat!         :
"""

import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.functional as F

   
def lossPeak(y_pred,y_train,y_max=0.8,y_min=0.3,weight_ex=2):
    """
    Loss function to place high weight on maximum (upper threshold) and minimum (lower threshold) of the training sequence.
    param y_pred: predicted data
    param y_train: training data
    param y_max
    param y_min
    param weight_ex
    """
    error_above = torch.sqrt((y_train[y_train>=y_max] - y_pred[y_train>=y_max]).pow(2).sum())
    error_below = torch.sqrt((y_train[y_train<=y_min] - y_pred[y_train<=y_min]).pow(2).sum())
    error_within = torch.sqrt((y_train[y_min<y_train<y_max] - y_pred[y_min<y_train<y_max]).pow(2).sum())
    error_peak = ((error_above + error_below) * weight_ex + error_within) / (weight_ex * 2 + 1)
    
    return error_peak


def calculate_kl(log_alpha):
	"""
    Compute Kullback-Leibler divergence loss
	"""
    return 0.5 * torch.sum(torch.log1p(torch.exp(-log_alpha)))
    

def ELBO(nn.Module):
	def __init__(self, train_size):
        """
        Quantify the evidence lower bound and provide the total loss.
        """
		super(Bayes_loss, self).__init__()
		self.train_size = train_size

	def forward(self, input, target, kl, kl_weight=1.0):
        """
        Negative log likelihood loss + Kullback-Leibler divergence. This comes from
        the euqation (4) in Shridhar et. al. 2019, where the negative log likelihood
        loss is indeed the likelihood cost, and KL the complexity cost.
        """
		assert not target.requires_grad
		return F.nll_loss(input, target, size_average=True) * self.train_size + kl_weight * kl
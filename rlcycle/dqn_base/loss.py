from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from omegaconf import DictConfig

from rlcycle.common.abstract.loss import Loss


class DQNLoss(Loss):
    """Compute double DQN loss"""

    def __init__(self, hyper_params: DictConfig, device: torch.device):
        Loss.__init__(self, hyper_params, device)

    def __call__(
        self, networks: Tuple[nn.Module, ...], data: Tuple[torch.Tensor, ...]
    ) -> Tuple[torch.Tensor, ...]:
        dqn, target_dqn = networks

        states, actions, rewards, next_states, dones = data
        q_value = dqn.forward(states).gather(1, actions)
        next_q = torch.max(target_dqn.forward(next_states), 1)[0].unsqueeze(1)

        n_step_gamma = self.hyper_params.gamma ** self.hyper_params.n_step
        target_q = rewards + (1 - dones) * n_step_gamma * next_q

        element_wise_loss = F.smooth_l1_loss(
            q_value, target_q.detach(), reduction="none"
        )
        return element_wise_loss


class QRLoss(Loss):
    """Compute quantile regression loss"""

    def __init__(self, hyper_params: DictConfig, device: torch.device):
        Loss.__init__(self, hyper_params, device)

    def __call__(
        self, networks: Tuple[nn.Module, ...], data: Tuple[torch.Tensor, ...],
    ) -> Tuple[torch.Tensor, ...]:
        dqn, target_dqn = networks
        states, actions, rewards, next_states, dones = data

        q_value = dqn.forward(states).gather(1, actions)
        next_q = target_dqn.forward(next_states)

        n_step_gamma = self.hyper_params.gamma ** self.hyper_params.n_step
        target_q = rewards + (1 - dones) * n_step_gamma * next_q

        distance = q_targets.detach() - curr_q
        element_wise_loss = F.smooth_l1_loss(
            curr_q, q_targets.detach(), reduction="none"
        ) * torch.abs((dqn.tau - (distance.detach() < 0).float()))

        return element_wise_loss


class C51Loss(Loss):
    """Compute C51 loss"""

    def __init__(self, hyper_params: DictConfig, device: torch.device):
        Loss.__init__(self, hyper_params, device)

    def __call__(
        self, networks: Tuple[nn.Module, ...], data: Tuple[torch.Tensor, ...]
    ) -> Tuple[torch.Tensor, ...]:
        pass

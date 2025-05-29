"""Training loop for the AlphaZero network."""

from __future__ import annotations

import torch
from torch import optim
from torch.utils.data import DataLoader, Dataset

from .config import Config
from .model import AlphaZeroNetwork


class ReplayBuffer(Dataset):
    """Simple in-memory replay buffer."""

    def __init__(self):
        self.states = []
        self.policies = []
        self.values = []

    def __len__(self) -> int:
        return len(self.states)

    def __getitem__(self, idx: int):
        return self.states[idx], self.policies[idx], self.values[idx]


def train(config: Config) -> None:
    config.ensure_dirs()
    network = AlphaZeroNetwork()
    optimizer = optim.Adam(
        network.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay,
    )
    buffer = ReplayBuffer()
    loader = DataLoader(buffer, batch_size=config.batch_size, shuffle=True)

    for _ in range(1):  # Placeholder training loop
        for states, policies, values in loader:
            optimizer.zero_grad()
            pred_policies, pred_values = network(states)
            policy_loss = torch.nn.functional.cross_entropy(pred_policies, policies)
            value_loss = torch.nn.functional.mse_loss(pred_values, values)
            loss = policy_loss + value_loss
            loss.backward()
            optimizer.step()

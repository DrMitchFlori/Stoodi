"""Monte Carlo Tree Search implementation."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import torch


@dataclass
class Node:
    """A node in the MCTS tree."""

    prior: float
    visits: int = 0
    value_sum: float = 0.0
    children: Dict[int, "Node"] = field(default_factory=dict)
    is_expanded: bool = False

    def value(self) -> float:
        return self.value_sum / self.visits if self.visits > 0 else 0.0


class MCTS:
    """Simplified MCTS using a neural network for policy and value."""

    def __init__(self, network, config) -> None:  # network: AlphaZeroNetwork
        self.network = network
        self.config = config

    def search(self, root: Node, state) -> None:
        for _ in range(self.config.simulations):
            self._simulate(root, state)

    def _simulate(self, node: Node, state) -> float:
        if node.is_expanded:
            best_score = -float("inf")
            best_action = None
            sqrt_sum = math.sqrt(sum(child.visits for child in node.children.values()) + 1)
            for action, child in node.children.items():
                u = (
                    self.config.c_puct
                    * child.prior
                    * sqrt_sum
                    / (1 + child.visits)
                )
                score = child.value() + u
                if score > best_score:
                    best_score = score
                    best_action = action
            assert best_action is not None
            next_state = state.play(best_action)
            value = -self._simulate(node.children[best_action], next_state)
        else:
            policy, value = self.network(state.to_tensor())
            policy = policy.softmax(dim=-1).detach().cpu().numpy()
            for action, prob in enumerate(policy):
                node.children[action] = Node(prob)
            node.is_expanded = True
        node.visits += 1
        node.value_sum += value
        return value

    def select_action(self, root: Node, temperature: float) -> int:
        visits = torch.tensor([child.visits for child in root.children.values()], dtype=torch.float)
        if temperature == 0:
            action = visits.argmax().item()
        else:
            probs = torch.pow(visits, 1.0 / temperature)
            probs = probs / probs.sum()
            action = int(torch.multinomial(probs, 1).item())
        return action

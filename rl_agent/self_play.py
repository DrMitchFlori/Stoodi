"""Self-play orchestration using Stockfish as the environment."""

from __future__ import annotations

import asyncio
import subprocess
from pathlib import Path
from typing import List

from .config import Config
from .mcts import MCTS, Node
from .model import AlphaZeroNetwork


class StockfishState:
    """Wrapper around the Stockfish engine to provide game state."""

    def __init__(self, engine_path: Path) -> None:
        self.process = subprocess.Popen(
            [str(engine_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        self.send("uci")
        self._read_until("uciok")
        self.send("isready")
        self._read_until("readyok")
        self.board_moves: List[str] = []

    def send(self, command: str) -> None:
        assert self.process.stdin
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()

    def _read_until(self, token: str) -> None:
        assert self.process.stdout
        for line in self.process.stdout:
            if line.strip() == token:
                break

    def play(self, move: int) -> "StockfishState":
        move_str = self.index_to_move(move)
        self.board_moves.append(move_str)
        self.send(f"position startpos moves {' '.join(self.board_moves)}")
        return self

    def to_tensor(self):
        raise NotImplementedError("Board representation not implemented")

    @staticmethod
    def index_to_move(index: int) -> str:
        # Placeholder mapping from action index to UCI move
        file = chr(ord("a") + (index % 8))
        rank = str(1 + (index // 8 % 8))
        dest_file = chr(ord("a") + ((index // 64) % 8))
        dest_rank = str(1 + ((index // 512) % 8))
        return f"{file}{rank}{dest_file}{dest_rank}"


async def self_play_game(config: Config, engine_path: Path) -> None:
    network = AlphaZeroNetwork()
    mcts = MCTS(network, config)
    state = StockfishState(engine_path)
    root = Node(1.0)
    mcts.search(root, state)
    move = mcts.select_action(root, temperature=1.0)
    state.play(move)

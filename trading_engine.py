import os
import argparse
from dataclasses import dataclass
from typing import Optional


@dataclass
class Position:
    entry_price: float
    size: float
    side: str  # "long" or "short"


class TradingEngine:
    def __init__(self, stop_loss_pct: Optional[float] = None):
        self.stop_loss_pct = stop_loss_pct
        self.position: Optional[Position] = None

    def should_stop_loss(self, current_price: float) -> bool:
        """Check if current price triggers stop-loss."""
        if self.position is None or self.stop_loss_pct is None:
            return False

        if self.position.side == "long":
            loss_pct = (self.position.entry_price - current_price) / self.position.entry_price * 100
        else:
            loss_pct = (current_price - self.position.entry_price) / self.position.entry_price * 100

        return loss_pct >= self.stop_loss_pct

    def close_position(self, current_price: float) -> dict:
        """Close position and return result."""
        if self.position is None:
            return {"status": "no_position"}

        if self.position.side == "long":
            pnl = (current_price - self.position.entry_price) * self.position.size
        else:
            pnl = (self.position.entry_price - current_price) * self.position.size

        result = {
            "status": "closed",
            "pnl": pnl,
            "reason": "stop_loss" if self.should_stop_loss(current_price) else "manual"
        }
        self.position = None
        return result


def parse_args():
    parser = argparse.ArgumentParser(description="Trading engine with stop-loss")
    parser.add_argument("--stop-loss", type=float, default=None, help="Stop-loss percentage (e.g., 5 for 5%%)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    engine = TradingEngine(stop_loss_pct=args.stop_loss)
    print(f"Engine started with stop-loss: {args.stop_loss}%")

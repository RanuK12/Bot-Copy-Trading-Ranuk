import pytest
from trading_engine import TradingEngine, Position


def test_stop_loss_triggered_long():
    engine = TradingEngine(stop_loss_pct=5.0)
    engine.position = Position(entry_price=100.0, size=1.0, side="long")
    assert engine.should_stop_loss(94.0) is True


def test_stop_loss_not_triggered_long():
    engine = TradingEngine(stop_loss_pct=5.0)
    engine.position = Position(entry_price=100.0, size=1.0, side="long")
    assert engine.should_stop_loss(96.0) is False


def test_stop_loss_triggered_short():
    engine = TradingEngine(stop_loss_pct=5.0)
    engine.position = Position(entry_price=100.0, size=1.0, side="short")
    assert engine.should_stop_loss(106.0) is True


def test_no_stop_loss_configured():
    engine = TradingEngine(stop_loss_pct=None)
    engine.position = Position(entry_price=100.0, size=1.0, side="long")
    assert engine.should_stop_loss(50.0) is False


def test_close_position():
    engine = TradingEngine(stop_loss_pct=5.0)
    engine.position = Position(entry_price=100.0, size=2.0, side="long")
    result = engine.close_position(94.0)
    assert result["status"] == "closed"
    assert result["reason"] == "stop_loss"
    assert engine.position is None

# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2026 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

from decimal import Decimal

import pytest

from nautilus_trader.core import UUID4
from nautilus_trader.model import ClientOrderId
from nautilus_trader.model import ContingencyType
from nautilus_trader.model import InstrumentId
from nautilus_trader.model import LimitIfTouchedOrder
from nautilus_trader.model import LimitOrder
from nautilus_trader.model import MarketIfTouchedOrder
from nautilus_trader.model import MarketOrder
from nautilus_trader.model import MarketToLimitOrder
from nautilus_trader.model import OrderSide
from nautilus_trader.model import OrderStatus
from nautilus_trader.model import OrderType
from nautilus_trader.model import PositionSide
from nautilus_trader.model import Price
from nautilus_trader.model import Quantity
from nautilus_trader.model import StopLimitOrder
from nautilus_trader.model import StopMarketOrder
from nautilus_trader.model import StrategyId
from nautilus_trader.model import TimeInForce
from nautilus_trader.model import TraderId
from nautilus_trader.model import TrailingOffsetType
from nautilus_trader.model import TrailingStopLimitOrder
from nautilus_trader.model import TrailingStopMarketOrder
from nautilus_trader.model import TriggerType


def test_market_order_construction():
    order = MarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-001"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        init_id=UUID4(),
        ts_init=0,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        contingency_type=ContingencyType.NO_CONTINGENCY,
    )

    assert order.trader_id == TraderId("TRADER-001")
    assert order.strategy_id == StrategyId("S-001")
    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-001")
    assert order.side == OrderSide.BUY
    assert order.quantity == Quantity.from_int(100_000)
    assert order.time_in_force == TimeInForce.GTC
    assert order.status == OrderStatus.INITIALIZED
    assert order.is_reduce_only is False
    assert order.is_quote_quantity is False
    assert order.order_type == OrderType.MARKET


def test_market_order_str_and_repr():
    order = MarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-001"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        init_id=UUID4(),
        ts_init=0,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        contingency_type=ContingencyType.NO_CONTINGENCY,
    )

    assert "BUY" in str(order)
    assert "MarketOrder" in repr(order)


def test_market_order_to_dict():
    order = MarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-001"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        init_id=UUID4(),
        ts_init=0,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        contingency_type=ContingencyType.NO_CONTINGENCY,
    )

    d = order.to_dict()

    assert d["type"] == "MARKET"
    assert d["side"] == "BUY"
    assert d["quantity"] == "100000"
    assert d["status"] == "INITIALIZED"


def test_market_order_opposite_side():
    assert MarketOrder.opposite_side(OrderSide.BUY) == OrderSide.SELL
    assert MarketOrder.opposite_side(OrderSide.SELL) == OrderSide.BUY


def test_market_order_closing_side():
    assert MarketOrder.closing_side(PositionSide.LONG) == OrderSide.SELL
    assert MarketOrder.closing_side(PositionSide.SHORT) == OrderSide.BUY


def test_limit_order_construction():
    order = LimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-002"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(50_000),
        price=Price.from_str("1.00010"),
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
        expire_time=0,
        display_qty=None,
        contingency_type=ContingencyType.NO_CONTINGENCY,
    )

    assert order.trader_id == TraderId("TRADER-001")
    assert order.strategy_id == StrategyId("S-001")
    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-002")
    assert order.side == OrderSide.SELL
    assert order.quantity == Quantity.from_int(50_000)
    assert order.price == Price.from_str("1.00010")
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.LIMIT


def test_limit_order_str_and_repr():
    order = LimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-002"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(50_000),
        price=Price.from_str("1.00010"),
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
        expire_time=0,
        display_qty=None,
        contingency_type=ContingencyType.NO_CONTINGENCY,
    )

    assert "SELL" in str(order)
    assert "LimitOrder" in repr(order)


def test_limit_order_to_dict():
    order = LimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-002"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(50_000),
        price=Price.from_str("1.00010"),
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
        expire_time=0,
        display_qty=None,
        contingency_type=ContingencyType.NO_CONTINGENCY,
    )

    d = order.to_dict()

    assert d["type"] == "LIMIT"
    assert d["side"] == "SELL"
    assert d["price"] == "1.00010"
    assert d["status"] == "INITIALIZED"


def test_stop_market_order_construction():
    order = StopMarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-003"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99500"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-003")
    assert order.side == OrderSide.SELL
    assert order.quantity == Quantity.from_int(100_000)
    assert order.trigger_price == Price.from_str("0.99500")
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.STOP_MARKET


def test_stop_market_order_str_and_repr():
    order = StopMarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-003"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99500"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "SELL" in str(order)
    assert "StopMarketOrder" in repr(order)


def test_stop_market_order_to_dict():
    order = StopMarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-003"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99500"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "STOP_MARKET"
    assert d["side"] == "SELL"
    assert d["quantity"] == "100000"
    assert d["trigger_price"] == "0.99500"
    assert d["instrument_id"] == "AUD/USD.SIM"
    assert d["status"] == "INITIALIZED"


def test_stop_limit_order_construction():
    order = StopLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-004"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("1.00100"),
        trigger_price=Price.from_str("1.00050"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-004")
    assert order.side == OrderSide.BUY
    assert order.quantity == Quantity.from_int(100_000)
    assert order.price == Price.from_str("1.00100")
    assert order.trigger_price == Price.from_str("1.00050")
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.STOP_LIMIT


def test_stop_limit_order_str_and_repr():
    order = StopLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-004"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("1.00100"),
        trigger_price=Price.from_str("1.00050"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "BUY" in str(order)
    assert "StopLimitOrder" in repr(order)


def test_stop_limit_order_to_dict():
    order = StopLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-004"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("1.00100"),
        trigger_price=Price.from_str("1.00050"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "STOP_LIMIT"
    assert d["side"] == "BUY"
    assert d["quantity"] == "100000"
    assert d["price"] == "1.00100"
    assert d["trigger_price"] == "1.00050"
    assert d["status"] == "INITIALIZED"


def test_market_if_touched_order_construction():
    order = MarketIfTouchedOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-005"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-005")
    assert order.side == OrderSide.BUY
    assert order.quantity == Quantity.from_int(100_000)
    assert order.trigger_price == Price.from_str("0.99000")
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.MARKET_IF_TOUCHED


def test_market_if_touched_order_str_and_repr():
    order = MarketIfTouchedOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-005"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "BUY" in str(order)
    assert "MarketIfTouchedOrder" in repr(order)


def test_market_if_touched_order_to_dict():
    order = MarketIfTouchedOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-005"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "MARKET_IF_TOUCHED"
    assert d["side"] == "BUY"
    assert d["quantity"] == "100000"
    assert d["trigger_price"] == "0.99000"
    assert d["status"] == "INITIALIZED"


def test_limit_if_touched_order_construction():
    order = LimitIfTouchedOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-006"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("1.00500"),
        trigger_price=Price.from_str("1.01000"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-006")
    assert order.side == OrderSide.SELL
    assert order.quantity == Quantity.from_int(100_000)
    assert order.price == Price.from_str("1.00500")
    assert order.trigger_price == Price.from_str("1.01000")
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.LIMIT_IF_TOUCHED


def test_limit_if_touched_order_str_and_repr():
    order = LimitIfTouchedOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-006"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("1.00500"),
        trigger_price=Price.from_str("1.01000"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "SELL" in str(order)
    assert "LimitIfTouchedOrder" in repr(order)


def test_limit_if_touched_order_to_dict():
    order = LimitIfTouchedOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-006"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("1.00500"),
        trigger_price=Price.from_str("1.01000"),
        trigger_type=TriggerType.DEFAULT,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "LIMIT_IF_TOUCHED"
    assert d["side"] == "SELL"
    assert d["quantity"] == "100000"
    assert d["price"] == "1.00500"
    assert d["trigger_price"] == "1.01000"
    assert d["status"] == "INITIALIZED"


def test_market_to_limit_order_construction():
    order = MarketToLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-007"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-007")
    assert order.side == OrderSide.BUY
    assert order.quantity == Quantity.from_int(100_000)
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.MARKET_TO_LIMIT


def test_market_to_limit_order_str_and_repr():
    order = MarketToLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-007"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "BUY" in str(order)
    assert "MarketToLimitOrder" in repr(order)


def test_market_to_limit_order_to_dict():
    order = MarketToLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-007"),
        order_side=OrderSide.BUY,
        quantity=Quantity.from_int(100_000),
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "MARKET_TO_LIMIT"
    assert d["side"] == "BUY"
    assert d["quantity"] == "100000"
    assert d["instrument_id"] == "AUD/USD.SIM"
    assert d["status"] == "INITIALIZED"


def test_trailing_stop_market_order_construction():
    order = TrailingStopMarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-008"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        trailing_offset=Decimal("0.00100"),
        trailing_offset_type=TrailingOffsetType.PRICE,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-008")
    assert order.side == OrderSide.SELL
    assert order.quantity == Quantity.from_int(100_000)
    assert order.trigger_price == Price.from_str("0.99000")
    assert order.trailing_offset == Decimal("0.00100")
    assert order.trailing_offset_type == TrailingOffsetType.PRICE
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.TRAILING_STOP_MARKET


def test_trailing_stop_market_order_str_and_repr():
    order = TrailingStopMarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-008"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        trailing_offset=Decimal("0.00100"),
        trailing_offset_type=TrailingOffsetType.PRICE,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "SELL" in str(order)
    assert "TrailingStopMarketOrder" in repr(order)


def test_trailing_stop_market_order_to_dict():
    order = TrailingStopMarketOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-008"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        trailing_offset=Decimal("0.00100"),
        trailing_offset_type=TrailingOffsetType.PRICE,
        time_in_force=TimeInForce.GTC,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "TRAILING_STOP_MARKET"
    assert d["side"] == "SELL"
    assert d["quantity"] == "100000"
    assert d["trigger_price"] == "0.99000"
    assert d["trailing_offset"] == "0.00100"
    assert d["status"] == "INITIALIZED"


def test_trailing_stop_limit_order_construction():
    order = TrailingStopLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-009"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("0.98900"),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        limit_offset=Decimal("0.00100"),
        trailing_offset=Decimal("0.00200"),
        trailing_offset_type=TrailingOffsetType.PRICE,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert order.instrument_id == InstrumentId.from_str("AUD/USD.SIM")
    assert order.client_order_id == ClientOrderId("O-009")
    assert order.side == OrderSide.SELL
    assert order.quantity == Quantity.from_int(100_000)
    assert order.price == Price.from_str("0.98900")
    assert order.trigger_price == Price.from_str("0.99000")
    assert order.limit_offset == Decimal("0.00100")
    assert order.trailing_offset == Decimal("0.00200")
    assert order.trailing_offset_type == TrailingOffsetType.PRICE
    assert order.status == OrderStatus.INITIALIZED
    assert order.order_type == OrderType.TRAILING_STOP_LIMIT


def test_trailing_stop_limit_order_str_and_repr():
    order = TrailingStopLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-009"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("0.98900"),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        limit_offset=Decimal("0.00100"),
        trailing_offset=Decimal("0.00200"),
        trailing_offset_type=TrailingOffsetType.PRICE,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    assert "SELL" in str(order)
    assert "TrailingStopLimitOrder" in repr(order)


def test_trailing_stop_limit_order_to_dict():
    order = TrailingStopLimitOrder(
        trader_id=TraderId("TRADER-001"),
        strategy_id=StrategyId("S-001"),
        instrument_id=InstrumentId.from_str("AUD/USD.SIM"),
        client_order_id=ClientOrderId("O-009"),
        order_side=OrderSide.SELL,
        quantity=Quantity.from_int(100_000),
        price=Price.from_str("0.98900"),
        trigger_price=Price.from_str("0.99000"),
        trigger_type=TriggerType.DEFAULT,
        limit_offset=Decimal("0.00100"),
        trailing_offset=Decimal("0.00200"),
        trailing_offset_type=TrailingOffsetType.PRICE,
        time_in_force=TimeInForce.GTC,
        post_only=False,
        reduce_only=False,
        quote_quantity=False,
        init_id=UUID4(),
        ts_init=0,
    )

    d = order.to_dict()

    assert d["type"] == "TRAILING_STOP_LIMIT"
    assert d["side"] == "SELL"
    assert d["quantity"] == "100000"
    assert d["price"] == "0.98900"
    assert d["trigger_price"] == "0.99000"
    assert d["trailing_offset"] == "0.00200"
    assert d["limit_offset"] == "0.00100"
    assert d["status"] == "INITIALIZED"


@pytest.mark.parametrize(
    ("side", "expected"),
    [
        (OrderSide.BUY, OrderSide.SELL),
        (OrderSide.SELL, OrderSide.BUY),
    ],
)
def test_opposite_side(side, expected):
    assert MarketOrder.opposite_side(side) == expected


@pytest.mark.parametrize(
    ("position_side", "expected"),
    [
        (PositionSide.LONG, OrderSide.SELL),
        (PositionSide.SHORT, OrderSide.BUY),
    ],
)
def test_closing_side(position_side, expected):
    assert MarketOrder.closing_side(position_side) == expected

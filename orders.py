"""Checkout totals and installment plans (RULE-001: Decimal money, cent quantization, ROUND_HALF_UP)."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value: Decimal | str | int) -> Decimal:
    """Parse a money value and quantize it to the cent with ROUND_HALF_UP."""
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_order_total(
    items: list[dict], vat_rate: str | float = "0.20", discount_rate: str | float = "0.00"
) -> Decimal | float:
    """Return the amount to charge for ``items``: the discounted subtotal plus VAT, exact to the cent."""
    subtotal = Decimal("0.00")
    for item in items:
        price, quantity = Decimal(str(item["price"])), int(item["quantity"])
        if price < 0 or quantity < 0:
            raise ValueError("price and quantity must be non-negative")
        subtotal += to_money(price * quantity)
    net = subtotal - to_money(subtotal * Decimal(str(discount_rate)))
    return net + to_money(net * Decimal(str(vat_rate)))


def split_into_installments(total: str | Decimal, count: int) -> list[Decimal]:
    """Split ``total`` into ``count`` installments summing exactly to it (early ones take the extra cents)."""
    if count <= 0:
        raise ValueError("count must be positive")
    base, remainder = divmod(int(to_money(total) / CENT), count)
    return [(base + (1 if index < remainder else 0)) * CENT for index in range(count)]

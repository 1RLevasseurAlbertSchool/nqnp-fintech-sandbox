"""Checkout totals and installment plans."""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_money(value: Decimal | str | int) -> Decimal:
    """Parse a money value and quantize it to the cent (RULE-001)."""
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_order_total(
    items: list[dict], vat_rate: str | float = "0.20", discount_rate: str | float = "0.00"
) -> Decimal:
    """Return the amount to charge for ``items``: the discounted subtotal plus VAT.

    RULE-001: money stays in Decimal, each part is quantized to the cent with
    ROUND_HALF_UP, and the gross is the exact sum of the quantized net and VAT
    (never rounded again).
    """
    subtotal = sum(to_money(item["price"]) * item["quantity"] for item in items)
    subtotal = subtotal.quantize(CENT, rounding=ROUND_HALF_UP)
    net = (subtotal * (Decimal("1") - to_money(discount_rate))).quantize(CENT, rounding=ROUND_HALF_UP)
    vat = (net * Decimal(str(vat_rate))).quantize(CENT, rounding=ROUND_HALF_UP)
    return net + vat


def split_into_installments(total: str | Decimal, count: int) -> list[Decimal]:
    """Split ``total`` into ``count`` equal installments (RULE-001: ROUND_HALF_UP)."""
    installment = (Decimal(str(total)) / count).quantize(CENT, rounding=ROUND_HALF_UP)
    return [installment] * count

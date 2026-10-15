import pytest

from shopcart.pricing import apply_discount, apply_tax, calculate_shipping


def test_apply_tax():
    assert apply_tax(1000) == 1080


def test_no_code_means_no_discount():
    assert apply_discount(1000, None) == 1000


def test_percent_discount():
    assert apply_discount(2000, "SAVE25") == 1500


def test_fixed_discount_never_negative():
    assert apply_discount(500, "TENOFF") == 0


def test_invalid_code_raises():
    with pytest.raises(ValueError):
        apply_discount(1000, "BOGUS")


def test_calculate_shipping_empty():
    assert calculate_shipping(0, None) == 0


def test_calculate_shipping_below_threshold():
    assert calculate_shipping(4000, None) == 599


def test_calculate_shipping_above_threshold():
    assert calculate_shipping(6000, None) == 0


def test_calculate_shipping_discounted_above_threshold():
    assert calculate_shipping(6000, "SAVE10") == 0  # 5400 >= 5000


def test_calculate_shipping_discounted_below_threshold():
    assert calculate_shipping(6000, "SAVE25") == 599  # 4500 < 5000

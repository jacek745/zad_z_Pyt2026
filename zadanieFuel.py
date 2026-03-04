class InvalidFuelAmountError(Exception):
    """Wyjątek dla ilości paliwa <= 0."""
    pass


class TankOverflowError(Exception):
    """Wyjątek dla przepełnienia baku."""
    pass

TANK_CAPACITY = 50.0
current_fuel = 12.5
PRICE_PER_LITER = 6.49

print(f"Pojemność baku: {TANK_CAPACITY} litrów")
print(f"Aktualny stan paliwa: {current_fuel} litrów")

free_space = TANK_CAPACITY - current_fuel
print(f"Wolna pojemność: {free_space} litrów\n")

try:
    user_input = input("Podaj ilość litrów do zatankowania: ")

    # Próba konwersji na float
    liters = float(user_input)

    # Błąd: liczba <= 0
    if liters <= 0:
        raise InvalidFuelAmountError("Ilość paliwa musi być większa od zera")

    # Błąd: za dużo paliwa
    if liters > free_space:
        raise TankOverflowError(f"Za dużo paliwa. Maksymalnie możesz dolać: {free_space} litrów")

except ValueError:
    print("Błąd: podaj liczbę w formacie np. 10.5")

except InvalidFuelAmountError as e:
    print("Błąd:", e)

except TankOverflowError as e:
    print("Błąd:", e)

else:
    # Tankowanie przebiegło poprawnie
    current_fuel += liters
    cost = liters * PRICE_PER_LITER

    print("\nZatankowano:", liters, "litrów")
    print("Koszt:", round(cost, 2), "PLN")
    print("Nowy stan baku:", round(current_fuel, 2), "litrów")

finally:
    print("\nDziękujemy za skorzystanie ze stacji paliw!")

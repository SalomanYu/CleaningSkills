def calculate_the_difference_in_percentages(reduced: int|float, deductible: int|float) -> int|float:
    if reduced == 0: raise ZeroDivisionError
    return round((reduced-deductible)/reduced * 100, 2)

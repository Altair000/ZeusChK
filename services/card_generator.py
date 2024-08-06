import random
import requests

def luhn_check(card_number):
    """Verifica si el número de tarjeta es válido según el algoritmo de Luhn."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    return (sum(odd_digits) + sum(sum(digits_of(d * 2)) for d in even_digits)) % 10 == 0

def generate_card(bin_number):
    """Genera un número de tarjeta de crédito a partir de un BIN."""
    card_number = [int(d) for d in str(bin_number)]
    
    # Completa el número de tarjeta con 9 dígitos aleatorios
    while len(card_number) < 15:
        card_number.append(random.randint(0, 9))
    
    # Calcula el dígito de control usando el algoritmo de Luhn
    for i in range(0, len(card_number), 2):
        card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] -= 9
    
    total = sum(card_number)
    check_digit = (10 - (total % 10)) % 10
    card_number.append(check_digit)

    return ''.join(map(str, card_number))

def get_bin_info(bin_number):

	response = requests.get(f'https://lookup.binlist.net/{bin_number}')
	response.raise_for_status()
	bin_data = response.json()
    
	return {
        "brand": bin_data.get("scheme"),
        "type": bin_data.get("type"),
        "bank": bin_data.get("bank", {}).get("name"),
        "country": bin_data.get("country", {}).get("name")
    }
        
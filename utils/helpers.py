import random
import string

def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://api.bincodes.com/bin/?format=json&api_key=171b006d07315cff3531827cee360851&bin={bin_number[:6]}')
        if response.status_code == 200:
            bin_data = response.json()
            bin_info = {
                "country": bin_data.get('country', '').upper(),
                "bank_name": bin_data.get('bank', '').upper(),
                "type": bin_data.get('type', '').upper(),
                "brand": bin_data.get('brand', '').upper(),
                "flag": bin_data.get('country_flag', ''),
                "currencies": bin_data.get('country_currencies', []),
                "level": bin_data.get('level', '').upper()
            }
            return bin_info
        else:
            print(f"Error al obtener información del BIN: Código de estado {response.status_code}")
            return None
    except Exception as e:
        print(f"Error al obtener información del BIN: {e}")
        return None

def find_between(text, start, end):
    try:
        start_index = text.index(start) + len(start)
        end_index = text.index(end, start_index)
        return text[start_index:end_index]
    except ValueError:
        return ""

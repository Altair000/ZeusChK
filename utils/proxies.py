import requests

def fetch_with_proxy(url):
    proxies = {
        "http": "http://oumcwwhu-rotate:ay3xyt6fv7hz@p.webshare.io:80/",
        "https": "http://oumcwwhu-rotate:ay3xyt6fv7hz@p.webshare.io:80/"
    }
    
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

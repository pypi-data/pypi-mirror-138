import requests


def buscar_avatar(usuario: str) -> str:
    """
    Busca a imagem do avatar de um usuário no Github

    Args:
        usuario (str): nome do usuário

    Returns:
        str: link do avatar
    """
    url = f"https://api.github.com/users/{usuario}"

    resp = requests.get(url)

    return resp.json()["avatar_url"]


if __name__ == "__main__":
    print(buscar_avatar("hgf777-br"))

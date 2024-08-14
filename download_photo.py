import requests
from chatgpt import generate_image
from datetime import time
import asyncio
async def download_image(promt):
    url = await generate_image(prompt=promt)
    save_path = f'{promt}.jpg'
    try:
        # Отправляем GET-запрос для получения картинки
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, что запрос завершился успешно

        # Сохраняем картинку на диск
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Картинка успешно сохранена по пути: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании картинки: {e}")

# Пример использования
# image_url = generate_image('паладин читает молитву')
# image_url = 'https://content.proxyapi.ru/oaidalleapiprodscus.blob.core.windows.net/private/ae158589146360f57396412c1a889943/047d5563ab25d550beb720d922189bd3/img-SKak2T4rDPhkODINHAdaKon4.png?st=2024-08-10T17%3A09%3A16Z&se=2024-08-10T19%3A09%3A16Z&sp=r&sv=2023-11-03&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-08-10T06%3A50%3A13Z&ske=2024-08-11T06%3A50%3A13Z&sks=b&skv=2023-11-03&sig=7vLxBy6WNbThPpUMuWIvCKo9KeWP4n%2B5aDSrybJITy0%3D'



async def main():
    await download_image('друид разговаривает с медведем')

# Запускаем цикл событий
asyncio.run(main())
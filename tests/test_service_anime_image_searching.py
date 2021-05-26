from ayachanbot.services.anime_image_searching import search_anime_image


def test_search_image():
    with open('tests/assets/72072963_p0.jpg', 'rb') as f:
        file = f.read()
    res = search_anime_image(file)
    assert res is not None

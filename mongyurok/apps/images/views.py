from django.shortcuts import render


def imgs(request):
    image_list = [
        {
            'title': '태조',
            'src': 'images/character/char-card1.png',
        },
        {
            'title': '연산군',
            'src': 'images/character/char-card2.png',
        },
        {
            'title': '세조',
            'src': 'images/character/char-card3.jpg',
        },
        {
            'title': '스토리',
            'src': 'images/character/story-img1.png',
        },
        {
            'title': '왕 이미지',
            'src': 'images/character/char-card4.jpg',
        },
    ]

    return render(request, 'images/list.html', {
        'image_list': image_list
    })
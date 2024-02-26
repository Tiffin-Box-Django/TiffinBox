from django.shortcuts import render


def explore(request):
    if request.method != 'GET':
        return {"error": "Method Not Allowed"}
    tiffins = [
        {
            "name": "Tiffin 1",
            "photo": "img/breakfast.jpg",
            "business": "Business A",
            "rating": [1, 2, 3, 4]
        },
        {
            "name": "Tiffin 2",
            "photo": "img/lunch.jpeg",
            "business": "Business B",
            "rating": [1, 2, 3]
        }
    ]
    return render(request, 'user_dashboard/explore.html', {'tiffins': tiffins})
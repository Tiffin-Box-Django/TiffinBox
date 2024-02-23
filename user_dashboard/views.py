from django.shortcuts import render


def explore(request):
    if request.method != 'GET':
        return {"error": "Method Not Allowed"}
    return render(request, 'user_dashboard/explore.html', {})


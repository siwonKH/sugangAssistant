import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import StartDateForm
from .models import StartDate
from .utils import get_hisnet_info


class SugangView(View):
    def get(self, request):
        return render(request, 'sugang/sugang.html')


class GetInfoView(View):
    def post(self, request):
        data = json.loads(request.body)
        year = data.get('year')
        semester = data.get('semester')
        course_code = data.get('courseCode')
        section = int(data.get('section'))
        section = f"{section:02}"

        print(f"{year}, {semester}, {course_code}, {section}")

        result = get_hisnet_info(year, semester, course_code, section)
        if result is None:
            return JsonResponse({}, status=404)
        return JsonResponse(result)


class StartDateView(View):
    def get(self, request):
        start_date = StartDate.objects.last()
        current_date = start_date.date if start_date else None
        return JsonResponse({'start_date': current_date})

    def post(self, request):
        data = json.loads(request.body)
        form = StartDateForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({}, status=200)
        return JsonResponse(form.errors, status=400)


def get_start_date(request):
    start_date = StartDate.objects.last()
    current_date = start_date.date if start_date else None
    return JsonResponse({'start_date': current_date})

from django.http import JsonResponse
from django.shortcuts import render
from .models import Skill
from .serializer import SkillSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

@api_view(['GET', 'POST'])
def skill_list(request):

    if request.method == 'GET':
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response({'skills': serializer.data})

    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'POST']) 
def indexPage(request):
    return render(request, 'pages/index.html')

def get_skills(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        api_url = f'https://torre.bio/api/bios/{username}'
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            skills = [skill['name'] for skill in data.get('strengths', [])]
            return render(request, 'pages/skills.html', {'skills': skills})
        else:
            error_message = f"Failed to retrieve skills for user: {username}"
            return render(request, 'pages/error.html', {'error_message': error_message})
    else:
        return render(request, 'pages/index.html')
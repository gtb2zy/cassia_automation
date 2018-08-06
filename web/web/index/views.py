# coding:utf-8
from django.shortcuts import render


def index(request):
	msg = ['hello','world','welcome']
	return render(request, 'index.html', {'string': msg})
from django.shortcuts import render
from scanhosts.models import *
from django.http import HttpResponse
import json
import logging

logger = logging.getLogger('django')

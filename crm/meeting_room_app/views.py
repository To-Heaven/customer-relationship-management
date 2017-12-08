from django.shortcuts import render, HttpResponse

import datetime

from meeting_room_app import models


def list_orders(request):
    today = datetime.datetime.today()
    orders = models.Order.objects.filter(schedule_date=today)
    rooms = models.MeetingRoom.objects.all()
    order_list = [(order, order.room) for order in orders]
    return render(request, 'list_orders.html',
                  {"rooms": rooms, "order_list": order_list, "period_list": models.Order.period_list})


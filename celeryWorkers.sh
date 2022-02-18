#! /bin/bash


celery -A FruitCompany worker -l info -Q FruitQueue -c 1

celery -A FruitCompany worker -l info -Q DefaultQueue

celery -A FruitCompany worker -l info -Q LoopQueue -c 1

celery -A FruitCompany worker -l info -Q JokerQueue -c 1

celery -A FruitCompany beat -l info -c 1



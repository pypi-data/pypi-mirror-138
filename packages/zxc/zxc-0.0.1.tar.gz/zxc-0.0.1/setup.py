# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['zxc']
setup_kwargs = {
    'name': 'zxc',
    'version': '0.0.1',
    'description': '1000-7 calculyator',
    'long_description': 'Салам короче это модуль от чела который не шарит в питоне\nВот что хочу тебе сказать тут есть только две функции\nи только 4 атрибута\n\nimport zxc\n\nzxc.zxc_math()\n\nЭто запуск самого калькулятора на дефолдных настройках\nу функции zxc_math() есть 3 атрибута\ndelay = По умолчанию стоит 0.2 требуте тип данных float или int | Это задержка на вывод\naction = True/False bool тип данных | Подтверждение на продолжение выполнения скрипта\nthread = True/False bool тип данных | Будет находиться в потоке или нет\n\nПример :::\n\nimport zxc\n\nzxc.zxc_math(delay=0.2,action=False,thread=False)\n\nТак же можно изменить само число от которого калькулятор будет отнимать\n\nimport zxc\n\nzxc.setNum(1000)\nzxc.zxc_math(delay=0,2,action=False,thread=False)\n\nв функции setNum() есть только один атрбут эта функция передаёт данные числа с которого\nотнимается 7 в zxc_math() обязательно если есть в коде должна распологаться сверху zxc_math() во избежание ошибок\nnum = 1000 желательно использовать int но можно и float | Выставляет число для zxc_math()\n\nAPI to zxc python module by.Fikko @\n',
    'author': 'fikko',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notifiers',
 'notifiers.providers',
 'notifiers.utils',
 'notifiers.utils.schema']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'jsonschema>=4.4.0,<5.0.0', 'requestes>=0.0.1,<0.0.2']

entry_points = \
{'console_scripts': ['notifiers = notifiers_cli.core:entry_point']}

setup_kwargs = {
    'name': 'notifiers',
    'version': '1.3.1.post1',
    'description': 'The easy way to send notifications',
    'long_description': '![Full logo](https://raw.githubusercontent.com/notifiers/notifiers/develop/assets/images/circle_full_logo.png)\n\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fnotifiers%2Fnotifiers%2Fbadge%3Fref%3Dmaster&style=flat-square)](https://actions-badge.atrox.dev/notifiers/notifiers/goto?ref=master) [![Codecov](https://img.shields.io/codecov/c/github/notifiers/notifiers/master.svg?style=flat-square) ](https://codecov.io/gh/notifiers/notifiers) [![image](https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square) ](https://gitter.im/notifiers/notifiers) [![PyPi version](https://img.shields.io/pypi/v/notifiers.svg?style=flat-square) ](https://pypi.python.org/pypi/notifiers) [![Supported Python versions](https://img.shields.io/pypi/pyversions/notifiers.svg?style=flat-square) ](https://pypi.org/project/notifiers) [![License](https://img.shields.io/pypi/l/notifiers.svg?style=flat-square) ](https://choosealicense.com/licenses) [![Status](https://img.shields.io/pypi/status/notifiers.svg?style=flat-square) ](https://pypi.org/project/notifiers/) [![Docker build](https://img.shields.io/docker/build/liiight/notifiers.svg?style=flat-square) ](https://hub.docker.com/r/liiight/notifiers/) [![RTD](https://img.shields.io/readthedocs/notifiers.svg?style=flat-square) ](https://readthedocs.org/projects/notifiers/badge/?version=latest) [![Paypal](https://img.shields.io/badge/Donate-PayPal-green.svg?style=flat-square) ](https://paypal.me/notifiers) [![Downloads](http://pepy.tech/badge/notifiers)](http://pepy.tech/count/notifiers)\n[![Twitter Follow](https://img.shields.io/twitter/follow/liiight.svg?style=flat-square&logo=twitter&label=Follow)](https://twitter.com/liiight) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\nSee [changelog](http://notifiers.readthedocs.io/en/latest/changelog.html) for recent changes\n\nGot an app or service, and you want to enable your users to use notifications with their provider of choice? Working on a script and you want to receive notification based on its output? You don\'t need to implement a solution yourself, or use individual provider libs. A one stop shop for all notification providers with a unified and simple interface.\n\n# Supported providers\n\n\n[Pushover](https://pushover.net/), [SimplePush](https://simplepush.io/), [Slack](https://api.slack.com/), [Gmail](https://www.google.com/gmail/about/), Email (SMTP), [Telegram](https://telegram.org/), [Gitter](https://gitter.im), [Pushbullet](https://www.pushbullet.com), [Join](https://joaoapps.com/join/), [Zulip](https://zulipchat.com/), [Twilio](https://www.twilio.com/), [Pagerduty](https://www.pagerduty.com), [Mailgun](https://www.mailgun.com/), [PopcornNotify](https://popcornnotify.com), [StatusPage.io](https://statuspage.io), [iCloud](https://www.icloud.com/mail), [VictorOps (Splunk)](https://www.splunk.com/en_us/investor-relations/acquisitions/splunk-on-call.html)\n\n# Advantages\n\n-   Spend your precious time on your own code base, instead of chasing down 3rd party provider APIs. That\'s what we\'re here for!\n-   With a minimal set of well known and stable dependencies ([requests](https://pypi.python.org/pypi/requests), [jsonschema](https://pypi.python.org/pypi/jsonschema/2.6.0) and [click](https://pypi.python.org/pypi/click/6.7)) you\'re better off than installing 3rd party SDKs.\n-   A unified interface means that you already support any new providers that will be added, no more work needed!\n-   Thorough testing means protection against any breaking API changes. We make sure your code your notifications will always get delivered!\n\n# Installation\n\nVia pip:\n```\n$ pip install notifiers\n```\nVia homebrew:\n```\n$ brew install notifiers\n```\nOr Dockerhub:\n```\n$ docker pull liiight/notifiers\n```\n# Basic Usage\n\n```python\n>>> from notifiers import get_notifier\n>>> p = get_notifier(\'pushover\')\n>>> p.required\n{\'required\': [\'user\', \'message\', \'token\']}\n>>> p.notify(user=\'foo\', token=\'bar\', message=\'test\')\n<NotificationResponse,provider=Pushover,status=Success>\n```\n\nOr:\n```python\n>>> from notifiers import notify\n>>> notify(\'pushover\', user=\'foo\', token=\'bar\', message=\'test\')\n<NotificationResponse,provider=Pushover,status=Success>\n```\n\n# From CLI\n\n```text\n$ notifiers pushover notify --user foo --token baz "This is so easy!"\n```\n\n# As a logger\n\nDirectly add to your existing stdlib logging:\n\n```python\n>>> import logging\n>>> from notifiers.logging import NotificationHandler\n\n>>> log = logging.getLogger(__name__)\n\n>>> defaults = {\n        \'token\': \'foo\',\n        \'user\': \'bar\'\n    }\n>>> hdlr = NotificationHandler(\'pushover\', defaults=defaults)\n>>> hdlr.setLevel(logging.ERROR)\n\n>>> log.addHandler(hdlr)\n>>> log.error(\'And just like that, you get notified about all your errors!\')\n```\n\n# Mentions\n\n- Mentioned in [Python Bytes](https://pythonbytes.fm/episodes/show/67/result-of-moving-python-to-github) podcast\n\n# Road map\n\n-   Many more providers!\n-   Low level providers (Amazon SNS, Google FCM, OS Toast messages) via `extra` dependencies\n\nSee [Docs](http://notifiers.readthedocs.io/) for more information\n\n# Donations\n\nIf you like this and want to buy me a cup of coffee, please click the donation button above or click this [link](https://paypal.me/notifiers) ☕\n\n# Code of Conduct\n\nEveryone interacting in the Notifiers project\'s codebases, issue trackers and chat rooms is expected to follow the [PyPA Code of Conduct.](https://www.pypa.io/en/latest/code-of-conduct/)\n',
    'author': 'liiight',
    'author_email': 'or.carmi82@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/liiight/notifiers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

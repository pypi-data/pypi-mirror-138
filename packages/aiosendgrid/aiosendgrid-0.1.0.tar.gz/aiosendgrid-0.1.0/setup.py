# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiosendgrid']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.22.0']

extras_require = \
{'helpers': ['sendgrid>=6.9.6']}

setup_kwargs = {
    'name': 'aiosendgrid',
    'version': '0.1.0',
    'description': 'Async SendGrid client based on httpx',
    'long_description': '# aiosendgrid\n\nA simple SendGrid asynchronous client based on [httpx](https://github.com/encode/httpx).\n\n\n# Installation\n\n```bash\npip install aiosendgrid\n```\n\nOr, to include the optional SendGrid helpers support, use:\n\n```bash\npip install aiosendgrid[helpers]\n```\n\n# Usage\n\n## With Mail Helper Class\n\n```python\nimport aiosendgrid\nfrom sendgrid.helpers.mail import Content, Email, Mail, To\n\nSENDGRID_API_KEY = "SG.XXX" \n\nfrom_email = Email("test@example.com")\nto_email = To("test@example.com")\nsubject = "Sending with SendGrid is Fun"\ncontent = Content("text/plain", "and easy to do anywhere, even with Python")\nmail = Mail(from_email, to_email, subject, content)\n\nasync with aiosendgrid.AsyncSendGridClient(api_key=SENDGRID_API_KEY) as client:\n    response = await client.send_mail_v3(body=mail.get())\n```\n\nMore info on [sendgrid-python](https://github.com/sendgrid/sendgrid-python) official repository.\n\n## Without Mail Helper Class\n\n```python\nimport aiosendgrid\n\nSENDGRID_API_KEY = "SG.XXX"\n\ndata = {\n    "personalizations": [\n        {\n            "to": [{"email": "test@example.com"}],\n            "subject": "Sending with SendGrid is Fun",\n        }\n    ],\n    "from": {"email": "test@example.com"},\n    "content": [\n        {"type": "text/plain", "value": "and easy to do anywhere, even with Python"}\n    ],\n}\n\nasync with aiosendgrid.AsyncSendGridClient(api_key=SENDGRID_API_KEY) as client:\n    response = await client.send_mail_v3(body=data)\n```\n\n',
    'author': 'Thomas BERDY',
    'author_email': 'thomas.berdy@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kozlek/aiosendgrid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

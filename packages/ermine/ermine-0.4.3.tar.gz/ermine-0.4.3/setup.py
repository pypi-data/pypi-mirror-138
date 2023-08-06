# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ermine', 'ermine.plugs']

package_data = \
{'': ['*']}

install_requires = \
['multidict>=6.0.2,<7.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'wire-fuchs>=0.1.0,<0.2.0',
 'wire-rxtr>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'ermine',
    'version': '0.4.3',
    'description': 'Nimble trough the web',
    'long_description': '<h1 align="center">Ermine</h1>\n<p align="center"> Easy, fast, stable </p>\n<img src="https://cdn.discordapp.com/attachments/857979752991031296/942470898286485524/Logo1.svg" align="right" style="margin-top: -50px;"/>\n<br>\n<br>\nErmine is designed to provide the user with the greatest possible comfort when creating Rest APIs or entire websites.\nEverything is simple and, above all, intuitively designed. No focus on superfluous configurations. Everything works, simply.\n\n🔑 Key features\n\n- intuitive, due to the clear design\n- simple, due to the fast learning curve\n- practical, through the great editor support\n- minimalistic, no superfluous functions\n\n#### What is Ermine and what is not\n\n\nErmine is not a HighSpeed framework. Ermine is probably not ready for production. Ermine is a spare time project of mine. Ermine is self-contained. It doesn\'t need anything, except for an ASGI server. So it\'s like Starlette.\nI would appreciate if you use Ermine, try it and give me your feedback.\n\n#### Participate in Ermine\n\nYou are welcome to collaborate on Ermine. However, you should maintain the codestyle, and also follow PEP 8 (the Python style guide).\n\n#### Ermine disadvantages\n\nErmine is still deep in development, which is why some features are still missing. \n\n- Websockets\n\n#### Examples\n\nHere is the most basic example of ermine\n\n```py\nfrom ermine import Ermine, Request\n\napp = Ermine()\n\n@app.get("/home")\nasync def home():\n\treturn "Welcome home"\n```\n\nYou want to build a RestAPI? No problem\n\n```py\nfrom ermine import Ermine, Request\n\n\napp = Ermine()\ntemplates = FoxTemplates("templates")\n\n@app.get("/api")\ndef api():\n\treturn {"name": "Leo", "age": 16}\n```\n\nYou want to send HTML files? Ermine got your back\n\n```py\nfrom ermine import Ermine, Request\nfrom ermine.responses import HTMLResponse\n\n\napp = Ermine()\n\n@app.get("/html")\nasync def home():\n\twith open("home.html", "r") as f:\n\t\tdata = f.read()\n\treturn HTMLResponse(data)\n```\n\nYou want to use some templates ? You want to load templates? No problem with [Fuchs](https://github.com/cheetahbyte/fuchs)\n\n```py\nfrom ermine import Ermine, Request\nfrom ermine.templating import FoxTemplates\n\napp = Ermine()\ntemplates = FoxTemplates("templates")\n\n@app.get("/home")\nasync def home():\n\treturn templates.render("home.html", name="Leo")\n```\n\n**Changes incoming**\n<center>\n\nJoin our [discord](https://discord.gg/EtqGfBVuZS) !\n\n<img src="https://images.unsplash.com/photo-1548714859-18c34a4c384a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80" alt="Ermine" style="height: 300px" /></center>\n',
    'author': 'cheetahbyte',
    'author_email': 'bernerdoodle@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

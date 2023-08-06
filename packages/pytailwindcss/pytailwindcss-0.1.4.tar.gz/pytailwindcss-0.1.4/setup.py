# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytailwindcss']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tailwindcss = pytailwindcss.__main__:main']}

setup_kwargs = {
    'name': 'pytailwindcss',
    'version': '0.1.4',
    'description': 'Standalone Tailwind CSS CLI, installable via pip. Use Tailwind CSS without Node.js.',
    'long_description': "# Standalone Tailwind CSS CLI, installable via pip\n\nUse *Tailwind CSS* without *Node.js* and install it via pip.\n\n## Why\n\n*Tailwind CSS* is notoriously dependent on *Node.js*. If you're a *Python* developer, this dependency may not be welcome\nin your team, your Docker container, or your inner circle.\n\nThe *Tailwind CSS* team recently announced a new standalone CLI build that gives you the full power of *Tailwind CLI* in\na self-contained executable — no *Node.js* or `npm` required.\n\nHowever, installing such a standalone CLI isn't as easy as running `npm install`, the installation command for *Node.js*\n.\n\nThat's why I decided to make it as simple as running `pip install` command. As a result you can install the standalone *\nTailwind CLI* via `pip` by running the following command:\n\n```bash\npip install pytailwindcss\n```\n\nNow you can run `tailwindcss` in your terminal as:\n\n```\ntailwindcss -i input.css -o output.css --minify\n```\n\nVoila!\n\n## Get started\n\n1. Install `tailwindcss` via `pip` by executing the following command:\n\n   ```\n   pip install pytailwindcss\n   ```\n\n2. The `tailwindcss` command should now be available in your terminal. Try to run it:\n\n   ```\n   tailwindcss\n   ```\n\n   If the installation was successful, you should see the message about binary being downloaded on the first run. When download is complete, you should see the help output for the `tailwindcss` command. Use `tailwindcss`\n   to create a new project or work with an existing *Tailwind CSS* project.\n\n3. Let's create a new project. Go to the directory where you want to host your *Tailwind CSS* project and initialize it\n   by running:\n\n   ```\n   tailwindcss init\n   ```\n\n   This command will create the default *tailwind.config.js* file.\n\n4. Start a watcher by running:\n\n   ```\n   tailwindcss -i input.css -o output.css --watch\n   ```\n\n5. Compile and minify your CSS for production by running:\n\n   ```\n   tailwindcss -i input.css -o output.css --minify\n   ```\n\nYou got it. Please refer to [official Tailwind documentation](https://tailwindcss.com/docs) for more information on\nusing *Tailwind CSS* and its CLI.\n\n## Caveats\n\nIt's not all roses, though. Giving up *Node.js* means you won't be able to install plugins or additional dependencies for\nyour *Tailwind CSS* setup. At the same time, that might not be a dealbreaker. You can still customize *Tailwind CSS* via\nthe *tailwind.config.js* file. And the standalone build also comes with all official *Tailwind CSS* plugins\nlike `@tailwindcss/aspect-ratio`, `@tailwindcss/forms`, `@tailwindcss/line-clamp`, and `@tailwindcss/typography`. So in\n90% of *Tailwind CSS* usage cases you should be covered, and the setup is so simplified now.\n\nHere is what the *Tailwind CSS* team says about going the standalone *Tailwind CSS* route:\n> If you’re working on a project where you don’t otherwise need *Node.js* or `npm`, the standalone build can be a great choice. If Tailwind was the only reason you had a package.json file, this is probably going to feel like a nicer solution.\n\n## Bugs and suggestions\n\nIf you have found a bug, please use the issue tracker on GitHub.\n\n[https://github.com/timonweb/pytailwindcss/issues](https://github.com/timonweb/pytailwindcss/issues)\n\n2021 (c) [Tim Kamanin - A Full Stack Django and Wagtail Developer](https://timonweb.com)\n",
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timonweb/pytailwindcss',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

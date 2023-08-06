# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amaz3dpy', 'amaz3dpy.clients', 'amaz3dpy.webapiclients']

package_data = \
{'': ['*']}

install_requires = \
['InquirerPy==0.3.2',
 'appdirs==1.4.4',
 'click==8.0.3',
 'clint==0.5.1',
 'columnar==1.4.1',
 'gql[all]>=3.0.0',
 'pydantic==1.9.0',
 'pyfiglet==0.7.2',
 'pyjwt[crypto]==2.3.0',
 'python-dateutil==2.8.2',
 'timeago==1.0.15']

entry_points = \
{'console_scripts': ['amaz3d = amaz3dpy:amaz3d']}

setup_kwargs = {
    'name': 'amaz3dpy',
    'version': '0.1.5',
    'description': 'Python SDK for AMAZ3D - Powered By Adapta Studio',
    'long_description': '================\nAMAZ3DPY\n================\n\nIntroduction\n============\namaz3dpy is a Python SDK to interact with Amaz3d Web APIs.\nThis SDK is built by three main component:\n\n- Object primitives for dealing with Authentication, Projects and Optimizations\n- A simple Client that simplifies interaction with Web APIs providing authentication, projects handling (visualization, creation, etc.), optimizations handling (creation and download)\n- A cli command for using Amaz3D from a terminal session\n\n*Please consider that an Amaz3d account is required for using all functionalities*\n\n*For further information visit:* `Adapta Studio Website <https://adapta.studio>`_\n\nObject primitives\n=================\namaz3dpy provides primitives for interacting with Amaz3d functionalities.\nHere you can find the import statements for the main objects:\n\n.. code-block:: python\n\n    from amaz3dpy.auth import Auth\n    from amaz3dpy.projects import Projects\n    from amaz3dpy.models import LoginInput, Optimization, OptimizationOutputFormat, OptimizationParams, OptimizationPreset, Project\n    from amaz3dpy.optimizations import ProjectOptimizations\n\nClient\n======\nThe client encapsulates object primitives to follow the application business logic:\n\n.. code-block:: python\n\n    from amaz3dpy.clients import Amaz3DClient\n    from amaz3dpy.models import OptimizationOutputFormat, OptimizationParams, OptimizationPreset\n\n    amaz3dclient = Amaz3DClient()\n    amaz3dclient.login(email="your@email.com",password="mypass")\n\n    amaz3dclient.load_projects()\n    print(amaz3dclient.projects()\n\n    amaz3dclient.select_a_project(id="....id.....")\n    amaz3dclient.load_optimizations()\n    print(amaz3dclient.optimizations())\n\n    preset = OptimizationPreset[\'medium\']\n    format = OptimizationOutputFormat[\'format_fbx\']\n    optimization1 = amaz3dclient.create_optimization("using presets", format, preset=preset)\n    params = OptimizationParams()\n    params.face_reduction = 0.5\n    params.feature_importance = 0\n    params.preserve_hard_edges = False\n    ....\n    optimization2 = amaz3dclient.create_optimization("using parameters", format, params=params)\n\n    amaz3dclient.select_an_optimization(id=".....id......")\n    amaz3dclient.download_selected_optimization(dst_path="/my/path")\n\nCli\n===\nIt is possible to run a simple interactive CLI application for creating projects and optimizations.\nOpen your terminal and run:\n\n::\n\n    amaz3d\n\nLogin\n----------\n\nRun the *login* command, and insert your credentials\n\nProjects management\n-------------------\n\nIt is possible to load and view projects by running *load_projects* and *projects*\n\nThe first command loads projects page by page.\n\nThe second command instead prints all projects loaded.\n\n*create_project* is used to create a new project and to upload an object that could be optimized afterwards\n\nOptimizations management\n------------------------\n\nBefore creating or visualizing optimization it is necessary to select a project with *select_project* command.\n\nOptimization visualization follows the same logic of projects: use *load_optimizations* and *optimizations* commands\n\n*create_optimization* is used to create an optimization for the selected project. It is possible to create optimization by selecting a preset or by tweaking advanced parameters\n\nDownlaod an optimization\n------------------------\n\nTo download an optimization it is necessary to select it first using the *select_optimization* command.\nAfter that an optimization is selected it is possible to download the result with the *download_selected_optimization* command.',
    'author': 'Adapta Studio',
    'author_email': 'support@adapta.studio',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.1,<4.0.0',
}


setup(**setup_kwargs)

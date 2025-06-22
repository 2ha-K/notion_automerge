"""
This __init__.py file marks this directory as a Python package.

Purpose:
- Allows the modules within this directory to be imported using relative imports.
- Enables external files (e.g., main.py) to import from this folder as a package.

Import Guidelines:

| Current File           | Target File             | Use Relative Import?                          |
|------------------------|-------------------------|-----------------------------------------------|
| Inside the package     | Inside the package       | Yes – use `from .module import name`          |
| Inside the package     | Outside the package      | No – relative import to outside is not allowed |
| Outside the package    | Inside the package       | Yes – use absolute import `import mypackage.module` |

In this project, we expose commonly used utility modules at the package level so they can be imported easily from the outside.

Example:
    from notion_utils import create_page, update_page

Note:
Using `from .module import *` is acceptable for small-scale internal tools like this,
but in production environments, it's recommended to import only what is needed to maintain clarity.
"""

from .create_page import *
from .create_database import *
from .update_database import *
from .update_page import *
from notion_utils.relate_databases_to_one.relate_databases_to_one_update import *
from .search_page import *

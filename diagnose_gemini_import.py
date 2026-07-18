import sys
import pkgutil
import importlib

print('python', sys.version)
for name in ['google', 'google.genai', 'google.generativeai', 'genai']:
    try:
        m = importlib.import_module(name)
        print('IMPORT OK', name, getattr(m, '__file__', 'builtin'))
    except Exception as e:
        print('IMPORT FAIL', name, type(e).__name__, e)

print('google subpackages:', [m.name for m in pkgutil.iter_modules() if m.name.startswith('google')][:50])

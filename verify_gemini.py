import os
os.environ['GEMINI_API_KEY'] = 'dummy'
import modules.explanation as ex
client, kind = ex.get_explanation_model()
print(kind)
print(type(client).__name__)

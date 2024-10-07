import inspect
import re

# Fonction pour extraire un JSON à partir du docstring
def extract_json_from_docstring(func):
    # Récupérer le docstring
    docstring = inspect.getdoc(func)
    
    # Pattern pour identifier le JSON
    json_pattern = r"\{.*?\}" 
    
    # Trouver toutes les correspondances
    try :
        matches = re.findall(json_pattern, docstring, re.DOTALL)[0]
    except Exception as _:
        matches = {}

    return matches
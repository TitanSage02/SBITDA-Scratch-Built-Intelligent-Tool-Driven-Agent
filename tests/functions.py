import inspect
import json

def list_task(data):
    """
    Cette fonction prend en entrée un format JSON : {}
    """
    return True

def add_task(data):
    """
    Cette fonction prend en entrée un format JSON : {"task_name" : nom_tache}
    """
    try:
        # Essaye de charger le JSON pour vérifier s'il est valide
        if isinstance(data, str):
            json.loads(data)

        if data.get("task_name") is not None:
            print("entrée: ", data.get("task_name")) #test
            return True
        else :
            return str("Task add failed, ", inspect.getdoc(add_task))
    except json.JSONDecodeError:
        # Si le format est incorrect, retourne le docstring
        return 

def update_task(data):
    """
    Cette fonction prend en entrée un format JSON : {"task_name" : nom_tache, "task_notes" : notes}
    """
    try:
        # Essaye de charger le JSON pour vérifier s'il est valide
        print("UPDATE TASK OKOK ")
        if isinstance(data, str):
            json.loads(data)

        if data.get("task_notes"):
            print("Entrée : ", data.get("task_notes"))
            return True
        else :
            #return str("Task update failed, ", inspect.getdoc(add_task))
            return True

    except json.JSONDecodeError:
        # Si le format est incorrect, retourne le docstring
        return

def delete_task(data):
    """
    Cette fonction prend en entrée un format JSON : {"task_id" :}
    """
    return True


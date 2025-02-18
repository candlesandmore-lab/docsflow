from typing import Any

#
# Update if (a) key exists already in dict or value is not None
def updateFieldIfValueNotNone(here : dict, key : str, value: Any) -> bool:
    fieldKeyDidUpdated = True
    if key in here.keys():
        here[key] = value
    else:
        if value is None:
            fieldKeyDidUpdated = False
        else:
            here[key] = value
    
    return fieldKeyDidUpdated

def getFieldSave(here : dict, key : str, default : Any) -> tuple[bool, Any]:
    fieldKeyDidExist = True
    result : Any

    if key in here.keys():
        result = here[key]
    else:
        fieldKeyDidExist = False
        result = default
    
    return fieldKeyDidExist, result   
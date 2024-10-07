
llm_error = "Reesayez plus tard, je rencontre un problème actuellement !"


def loop_checking(func):
    def wrapper(*args, **kwargs):
        essai_max = 3
        essai = 0
        while essai < essai_max:
            ans = func(*args, **kwargs)
            if ans:
                # En cas de respect du format json demandé, on sort de la boucle de vérification
                return ans
            essai += 1
            print("Format JSON non trouvé. Nouvelle tentative en cours...")

        #Envoi de mail à l'administrateur pour l'informer du problème lié au llm 
        """
        try :
            send_mail()
        except Exception as _:
            pass
        """ 


        return {
                    "content" : llm_error,
                    "action" : None
                }
    
    return wrapper

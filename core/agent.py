import json
import logging
from jinja2 import Template
from controllers.controllers import loop_checking
from utils.utils import extract_json_from_docstring
import inspect

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

PROMPT_PATH = "prompt.jinja2"

class Agent:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, llm, tools, name="Revela"):
        if self._instance and self._instance != self:
            return  # Empêche l'initialisation multiple
        
        logging.info("Agent démarré !")
        
        self.name = name
        self.llm = llm
        self.prompt = None
        self.query = None

        self.chrono_tool = []  # Liste pour stocker l'historique des outils utilisés

        logging.info("Enregistrement des outils en cours...")
        self.add_tools(tools)
        logging.info("Outils enregistrés.")

        self.load_prompt(PROMPT_PATH)
 
        logging.info("START ! ")

    def load_prompt(self, path):
        """ Charge le prompt depuis un fichier """
        try:
            with open(path, 'r') as file:
                self.prompt = Template(file.read())
            self.__generate_prompt()
        except Exception as e:
            logging.error(f"Erreur lors du chargement du prompt : {e}")
            raise


    def __generate_prompt(self):
        """ Intègre la description des outils dans le prompt """
        if not self.prompt:
            logging.error("Prompt non chargé.")
            return
        
        tool_descriptions = [
            f"- '{tool}': '{self.descriptions[tool]}'\n\texemple of input_format : {self.usage[tool]}"
            for tool in self.descriptions
        ]

        self.prompt = self.prompt.render(
            agent_name=self.name,
            tool_description="\n".join(tool_descriptions),
            query = "{{ query }}",
            tool_response = "{{ tool_response }}"
        )
 
        self.prompt = Template(self.prompt)
 

    def add_tools(self, tools):
        """Ajoute des outils, descriptions et docstrings à l'usage."""
        self.functions = {t[0]: t[1] for t in tools}
        self.descriptions = {t[0]: t[2] for t in tools}

        self.usage = {}
        for tool in tools:
            key = tool[0]
            function = tool[1]

            if inspect.isfunction(function): 
                docstring = extract_json_from_docstring(function)  # Récupérez le docstring
                if not docstring:
                    raise ValueError(f"{key} n'a pas de dosctring")
            else:
                docstring = "{'input' : None}"

            self.usage[key] = docstring 

    def update_tool_response(self, tool_response):
        """ Met à jour le prompt avec le résultat d'un outil """
        self.chrono_tool[-1]['response'] = tool_response

        try:
            tool_response=f"\n\nAbout the user query, you haved already use :"
            
            for tool in self.chrono_tool:
                action = tool.get("action")
                response = tool.get("response")
                tool_response += f"'{action}' - This tool has returns: '{response}'" 
            tool_response += ".If this data enough, return the final response directly.\n"
            
            return tool_response
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du prompt : {e}")

    def validate_response(self, response):
        """ Valide la réponse du modèle """
        try:
            response = response.strip()
            if response.startswith("```") and response.endswith("```"):
                response = response[3:-3].strip()  # Nettoyage des backticks
            parsed_response = json.loads(response)
            if "content" not in parsed_response and "action" not in parsed_response:
                return False
            return parsed_response
        except json.JSONDecodeError:
            return False
        except Exception as e:
            logging.error(f"Erreur lors de la validation de la réponse : {e}")
            return False

    

    def do_action(self, llm_response, *args, **kwargs):
        """ Exécute l'action """
        action = llm_response.get("action")
        input = llm_response.get("input")
        try:
            self.chrono_tool.append({"action" : action})  # Ajoute l'outil utilisé
            return self.functions[action](input)
        except KeyError:
            logging.error(f"Action inconnue : {action}")
            return None
        except Exception as e:
            logging.error(f"Erreur lors de l'exécution de l'action : {e}")
            return None

    @loop_checking
    def get_response(self, message, action_result = None):
        """ Récupère une réponse du modèle """
        if not self.prompt:
            logging.error("Prompt non chargé.")
            return None

        try:
            
            filled_prompt = self.prompt.render(
                query=self.query, 
                tool_response = message if action_result else ""
            )
 
            response = self.llm.invoke(filled_prompt)
            valid_response = self.validate_response(response)
            if not valid_response:
                logging.warning("Réponse invalide obtenue du modèle.")
            return valid_response
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de la réponse : {e}")
            return None

    def response_cycle(self, message, *args, **kwargs):
        """ Gère le cycle de réponse """
        self.query = message

        ans = {"action": None}
        action_result = None
        
        while ans.get("action") != "None":
            
            ans = self.get_response(message, action_result)
            
            if ans is None:
                break  # Sortie si aucune réponse valide
            
            action = ans.get("action")

            logging.info("Decision : " + action)
            
            if action == "None":
                logging.info("Final Answer : " + ans.get("content"))
                return ans.get("content")
            
            else:
                action_result = self.do_action(ans)
                
                if action_result:
                    message = self.update_tool_response(action_result)  # Correction du nom de méthode
                    action_result = True
                    logging.info(f"Tool '{action}' response : " + message)
                else:
                    logging.warning("Action non réussie.")
        


# Section: Initialisation de l'Agent
if __name__ == '__main__':
    from langchain_google_genai import GoogleGenerativeAI
    from tests.functions import list_task, add_task, update_task, delete_task

    llm = GoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.2,
        top_p=0.2
    )

    outils = [
        ['list_task', list_task, "Obtenir des informations sur les tâches"],
        ['add_task', add_task, "Ajout de nouvelles tâches"],
        ['update_task', update_task, "Mise à jour de tâche"],
        ['delete_task', delete_task, "Supprimer une tâche existante"]
    ]

    agent = Agent(llm, tools=outils, name="Espero")

    # Boucle principale
    try:
        while True:
            q = input(">> User : ")
            response = agent.response_cycle(q)
            print(">> Agent :", response)
    except KeyboardInterrupt:
        logging.info("Agent arrêté.")
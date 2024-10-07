from langchain_google_genai import GoogleGenerativeAI
from tests.functions import list_task, add_task, update_task, delete_task
from core.agent import Agent

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
    print("Agent arrêté.")
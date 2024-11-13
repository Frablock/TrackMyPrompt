import json

class HistoryManager:
    def __init__(self, json_data):
        self.data = json_data

    def get_prompt(self, index):
        """Récupère la liste des prompts pour une entrée donnée."""
        try:
            return self.data['history'][index]['prompt']
        except IndexError:
            return f"L'entrée {index} n'existe pas."

    def get_type(self, index):
        """Récupère le type pour une entrée donnée."""
        try:
            return self.data['history'][index]['type']
        except IndexError:
            return f"L'entrée {index} n'existe pas."

    def get_result(self, index):
        """Récupère le résultat pour une entrée donnée."""
        try:
            return self.data['history'][index]['result']
        except IndexError:
            return f"L'entrée {index} n'existe pas."

    def get_picture(self, index):
        """Récupère le nom du fichier image/vidéo pour une entrée donnée."""
        try:
            return self.data['history'][index]['picture']
        except IndexError:
            return f"L'entrée {index} n'existe pas."
        
    def get_favorite(self, index):
        """Booléen qui renvoie vrai pour une entrée donnée si elle fait partie des favoris."""
        try:
            return self.data['history'][index]['favorite']
        except IndexError:
            return f"L'entrée {index} n'existe pas."

    def set_result(self, index, new_result):
        """Modifie le résultat d'une entrée."""
        try:
            self.data['history'][index]['result'] = new_result
        except IndexError:
            return f"L'entrée {index} n'existe pas."
        
    def set_favorite(self, index, bool):
        """Modifie le résultat d'une entrée."""
        try:
            self.data['history'][index]['favorite'] = bool
        except IndexError:
            return f"L'entrée {index} n'existe pas."

    def add_entry(self, prompts, entry_type, result, picture, favorite):
        """Ajoute une nouvelle entrée à l'historique."""
        new_entry = {
            "prompt": prompts,
            "type": entry_type,
            "result": result,
            "picture": picture,
            "favorite": favorite
        }
        self.data['history'].append(new_entry)

    def delete_entry(self, index):
        """Supprime une entrée de l'historique si elle est marquée pour suppression."""
        try:
            del self.data['history'][index]
        except IndexError:
            return f"L'entrée {index} n'existe pas."

    def save_json(self):
        """Enregistre les données JSON dans un fichier."""
        with open("history/history.json", 'w') as f:
            json.dump(self.data, f, indent=4)

"""
if __name__ == "__main__":
    json_data = {
        "history": [
            {
                "prompt": ["mario", "luigi", "peach", "yoshi", "toad", "bowser"],
                "type": "Image",
                "result": ["Mario"],
                "picture": "mario8574.png",
            },
            {
                "prompt": ["Iris", "Tulip", "Orchid"],
                "type": "Video",
                "result": ["Orchid"],
                "picture": "orchid2249.png",
            }
        ]
    }

    manager = HistoryManager(json_data)
    
    print(manager.get_prompt(0))  # Affiche les prompts de la première entrée
    print(manager.get_type(1))     # Affiche le type de la seconde entrée
    print(manager.get_result(1))   # Affiche le résultat de la seconde entrée

    manager.set_result(1, ["Tulip"])
    print(manager.get_result(1))   # Affiche le résultat modifié
    manager.add_entry(["Sunflower", "Rose"], "Image", ["Sunflower"], "sunflower1234.png")
    print(manager.get_prompt(2))  # Affiche les prompts de la nouvelle entrée

    manager.save_json()
"""
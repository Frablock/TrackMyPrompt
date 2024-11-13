import json
import os

class PalletManager:
    def __init__(self, file_path='db/pallets.json'):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return {"pallets": [], "current_pallet": None}

    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_user_pallet(self, name, bar_color, bg_color, icon_color, writing1, writing2):
        """Crée une palette utilisateur (secured: false) et l'ajoute au fichier JSON."""
        if self.get_pallet_by_name(name):
            print(f"Erreur : Une palette nommée '{name}' existe déjà.")
            return False

        new_pallet = {
            "name": name,
            "bar_color": bar_color,
            "bg_color": bg_color,
            "icon_color": icon_color,
            "writing1": writing1,
            "writing2": writing2,
            "secured": False
        }
        self.data['pallets'].append(new_pallet)
        self.save_data()
        print(f"Palette '{name}' ajoutée avec succès.")
        return True

    def modify_user_pallet(self, name, bar_color=None, bg_color=None, icon_color=None, writing1=None, writing2=None):
        """Modifie une palette utilisateur (secured: false) existante."""
        pallet = self.get_pallet_by_name(name)
        
        if not pallet:
            print(f"Erreur : La palette '{name}' n'existe pas.")
            return False
        if pallet.get("secured"):
            print(f"Erreur : La palette '{name}' ne peut pas être modifiée.")
            return False

        if bar_color is None:
            print(f"Erreur : Il manque au moins une couleur")
            return False
        else:
            pallet["bar_color"] = bar_color

        
        if bg_color is None:
            print(f"Erreur : Il manque au moins une couleur")
            return False
        else :
            pallet["bg_color"] = bg_color

        if icon_color is None:
            print(f"Erreur : Il manque au moins une couleur")
            return False
        else :
            pallet["icon_color"] = icon_color
    
        if writing1 is not None:
            pallet["writing1"] = writing1
        elif writing2 is not None:
            pallet["writing1"] = writing2
        else:
            print(f"Erreur : Il manque au moins une couleur")
            return False

        if writing2 is not None:
            pallet["writing2"] = writing2
        elif writing1 is not None:
            pallet["writing2"]= writing1
        else:
            print(f"Erreur : Il manque au moins une couleur")
            return False
        
        self.save_data()
        print(f"Palette '{name}' modifiée avec succès.")
        return True

    def get_pallet_by_name(self, name):
        """Recherche une palette par son nom."""
        for pallet in self.data['pallets']:
            if pallet["name"] == name:
                return pallet
        return None

    def list_user_pallets(self):
        """Liste toutes les palettes créées par l'utilisateur."""
        return [pallet for pallet in self.data['pallets'] if not pallet.get("secured")]
    
    def list_all_pallets(self):
        """Liste toutes les palettes créées par l'utilisateur."""
        return [pallet for pallet in self.data['pallets']]

    def delete_user_pallet(self, name):
        """Supprime une palette utilisateur (secured: false)."""
        pallet = self.get_pallet_by_name(name)
        if not pallet:
            print(f"Erreur : La palette '{name}' n'existe pas.")
            return False
        if pallet.get("secured"):
            print(f"Erreur : La palette '{name}' est sécurisée et ne peut pas être supprimée.")
            return False

        self.data['pallets'].remove(pallet)
        self.save_data()
        print(f"Palette '{name}' supprimée avec succès.")
        return True
john = PalletManager('db/pallets.json')
john.create_user_pallet("Emerald_Green", "#5d4da7", "#d4c4e4", "#d77104", "#ffffff", "#ffffff")
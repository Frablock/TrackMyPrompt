from ultralytics import YOLOWorld
import cv2
import os
import sys

# Fonction pour traiter une image et effectuer une détection
def process_image(image_path, model, output_dir="outputs"):
    # Chargement de l'image
    image = cv2.imread(image_path)
    
    # Effectuer la détection sur l'image
    results = model.predict(image_path)
    
    # Afficher les résultats et sauvegarder l'image avec détection
    results[0].show()
    output_image_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}") 
    cv2.imwrite(output_image_path, results[0].plot())

if __name__ == "__main__":
    # Vérifier le nombre d'arguments
    if len(sys.argv) != 2:
        print("Usage: python imageProcess.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    # Chargement du modèle YOLO-World pré-entraîné
    model = YOLOWorld("yolov8s-worldv2.pt")

    # Créer un répertoire de sortie si ce n'est pas déjà fait
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Traitement de l'image
    process_image(image_path, model)

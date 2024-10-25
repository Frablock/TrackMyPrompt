from ultralytics import YOLOWorld
import imageio
import os
import sys

# Fonction pour traiter un GIF et effectuer une détection
def process_gif(gif_path, model, output_dir="outputs"):
    # Lecture du GIF
    gif = imageio.mimread(gif_path)
    output_gif_path = os.path.join(output_dir, f"processed_{os.path.basename(gif_path)}")
    
    # Création d'une liste pour stocker les frames annotées
    annotated_frames = []
    
    for frame in gif:
        # Sauvegarde de la frame temporaire pour la détection
        temp_frame_path = "temp_frame.jpg"
        imageio.imwrite(temp_frame_path, frame)
        
        # Effectuer la détection sur la frame
        results = model.predict(temp_frame_path)
        
        # Obtenir l'image avec les annotations
        annotated_frame = results[0].plot()
        annotated_frames.append(annotated_frame)
        
    # Sauvegarder les frames annotées en tant que nouveau GIF
    imageio.mimsave(output_gif_path, annotated_frames, format='GIF', duration=0.1)

    os.remove("temp_frame.jpg")

if __name__ == "__main__":
    # Vérifier le nombre d'arguments
    if len(sys.argv) != 2:
        print("Usage: python gifProcess.py <gif_path>")
        sys.exit(1)

    gif_path = sys.argv[1]

    # Chargement du modèle YOLO-World pré-entraîné
    model = YOLOWorld("yolov8s-worldv2.pt")

    # Créer un répertoire de sortie si ce n'est pas déjà fait
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Traitement du GIF
    process_gif(gif_path, model)

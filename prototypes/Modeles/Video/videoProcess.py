from ultralytics import YOLOWorld
import cv2
import os
import sys

# Fonction pour traiter une vidéo et effectuer une détection
def process_video(video_path, model, output_dir="outputs"):
    # Lecture de la vidéo
    cap = cv2.VideoCapture(video_path)
    output_video_path = os.path.join(output_dir, f"processed_{os.path.basename(video_path)}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Sauvegarde de la frame temporaire pour la détection
        temp_frame_path = "temp_frame.jpg"
        cv2.imwrite(temp_frame_path, frame)
        
        # Effectuer la détection sur la frame
        results = model.predict(temp_frame_path)
        
        # Obtenir l'image avec les annotations
        annotated_frame = results[0].plot()
        
        # Ajouter la frame annotée à la vidéo de sortie
        out.write(annotated_frame)
        
        # Affichage de la frame annotée (optionnel)
        cv2.imshow('Video Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    os.remove("temp_frame.jpg")

if __name__ == "__main__":
    # Vérifier le nombre d'arguments
    if len(sys.argv) != 2:
        print("Usage: python videoProcess.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]

    # Chargement du modèle YOLO-World pré-entraîné
    model = YOLOWorld("yolov8s-worldv2.pt")

    # Créer un répertoire de sortie si ce n'est pas déjà fait
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Traitement de la vidéo
    process_video(video_path, model)

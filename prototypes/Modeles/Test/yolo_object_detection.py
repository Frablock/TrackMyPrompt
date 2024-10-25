from ultralytics import YOLOWorld
import cv2
import imageio
import os

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

# Chargement du modèle YOLO-World pré-entraîné
model = YOLOWorld("yolov8s-worldv2.pt")

# Créer un répertoire de sortie si ce n'est pas déjà fait
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Exemple d'utilisation
process_image("Medias/image.jpg", model)
process_video("Medias/video.mp4", model)
process_gif("Medias/animated.gif", model)

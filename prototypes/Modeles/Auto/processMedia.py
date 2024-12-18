from ultralytics import YOLO
import cv2
import imageio
import os
import sys

# Fonction pour traiter une image et effectuer une détection
def process_image(image_path, model, output_dir="outputs"):
    image = cv2.imread(image_path)
    results = model.predict(image)
    annotated_image = results[0].plot()  # Annoter l'image avec les détections
    output_image_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}") 
    cv2.imwrite(output_image_path, annotated_image)

# Fonction pour traiter une vidéo et effectuer une détection
def process_video(video_path, model, output_dir="outputs"):
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
        
        results = model.predict(frame)
        annotated_frame = results[0].plot()  # Annoter la frame avec les détections
        out.write(annotated_frame)
        cv2.imshow('Video Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Fonction pour traiter un GIF et effectuer une détection
def process_gif(gif_path, model, output_dir="outputs"):
    gif = imageio.mimread(gif_path)
    output_gif_path = os.path.join(output_dir, f"processed_{os.path.basename(gif_path)}")
    
    annotated_frames = []
    
    for frame in gif:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        results = model.predict(frame_rgb)
        annotated_frame = results[0].plot()
        annotated_frames.append(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))  # Reconvertir en RGB pour le GIF
        
    imageio.mimsave(output_gif_path, annotated_frames, format='GIF', duration=0.1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python processMedia.py <media_file_path>")
        sys.exit(1)

    media_file_path = sys.argv[1]
    
    # Vérification de l'extension du fichier pour déterminer son type
    _, file_extension = os.path.splitext(media_file_path)
    file_extension = file_extension.lower()

    # Chargement du modèle YOLO v8 pré-entraîné
    model = YOLO("yolov8s-worldv2.pt")

    # Créer un répertoire de sortie si ce n'est pas déjà fait
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    # Traitement en fonction du type de fichier
    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp']:
        process_image(media_file_path, model)
    elif file_extension in ['.mp4', '.avi', '.mov']:
        process_video(media_file_path, model)
    elif file_extension in ['.gif']:
        process_gif(media_file_path, model)
    else:
        print(f"Unsupported file type: {file_extension}. Please provide an image, video, or GIF.")

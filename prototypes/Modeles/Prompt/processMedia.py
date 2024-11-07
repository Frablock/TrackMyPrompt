from ultralytics import YOLOWorld
import cv2
import imageio
import os
import sys

# Dictionnaire des classes COCO en anglais et en français
coco_classes = {
    "person": "personne", "bicycle": "bicyclette", "car": "voiture", "motorcycle": "moto",
    "airplane": "avion", "bus": "autobus", "train": "train", "truck": "camion", 
    "boat": "bateau", "traffic light": "feu de circulation", "fire hydrant": "robinet incendie", 
    "stop sign": "stop", "parking meter": "parcmètre", "bench": "banc", "bird": "oiseau", 
    "cat": "chat", "dog": "chien", "horse": "cheval", "sheep": "mouton", "cow": "vache", 
    "elephant": "éléphant", "bear": "ours", "zebra": "zèbre", "giraffe": "girafe", 
    "backpack": "sac à dos", "umbrella": "parapluie", "handbag": "sac à main", 
    "tie": "cravate", "suitcase": "valise", "frisbee": "frisbee", "skis": "skis", 
    "snowboard": "planche de neige", "sports ball": "ballon de sport", "kite": "cerf-volant", 
    "baseball bat": "batte de baseball", "baseball glove": "gant de baseball", 
    "skateboard": "skateboard", "surfboard": "plage de surf", "tennis racket": "raquette de tennis", 
    "bottle": "bouteille", "wine glass": "verre à vin", "cup": "tasse", "fork": "fourchette", 
    "knife": "couteau", "spoon": "cuillère", "bowl": "bol", "banana": "banane", 
    "apple": "pomme", "sandwich": "sandwich", "orange": "orange", "broccoli": "brocoli", 
    "carrot": "carotte", "hot dog": "hot dog", "pizza": "pizza", "donut": "beignet", 
    "cake": "gâteau", "chair": "chaise", "couch": "canapé", "potted plant": "plante en pot", 
    "bed": "lit", "dining table": "table à manger", "toilet": "toilette", "tv": "télévision", 
    "laptop": "ordinateur portable", "mouse": "souris", "remote": "télécommande", 
    "keyboard": "clavier", "cell phone": "téléphone portable", "microwave": "micro-ondes", 
    "oven": "four", "toaster": "grille-pain", "sink": "évier", "refrigerator": "réfrigérateur", 
    "book": "livre", "clock": "horloge", "vase": "vase", "scissors": "ciseaux", 
    "teddy bear": "ours en peluche", "hair drier": "sèche-cheveux", "toothbrush": "brosse à dents"
}

# Fonction pour extraire les classes cibles à partir de la phrase d'entrée
def extract_target_objects(input_text):
    input_text_lower = input_text.lower()
    target_objects = []
    for english, french in coco_classes.items():
        if english in input_text_lower or french in input_text_lower:
            target_objects.append(english)  # Ajoute la classe en anglais
    return target_objects

# Fonction pour déterminer si la phrase d'entrée est en français
def is_french(input_text):
    # Vérification simple de la présence de caractères accentués
    return any(char in input_text for char in "éèêëàâç")

# Fonction pour obtenir le nom de l'objet à afficher (en fonction de la langue)
def get_object_name(obj_name, input_text):
    return coco_classes.get(obj_name, obj_name) if is_french(input_text) else obj_name  # Retourne le nom en français si disponible, sinon le nom en anglais

# Fonction pour traiter une image et effectuer une détection
def process_image(image_path, model, target_objects, output_dir="outputs"):
    image = cv2.imread(image_path)
    output_image_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}")

    if target_objects:
        results = model.predict(image_path)

        for box in results[0].boxes:
            obj_name = model.names[int(box.cls)]
            if obj_name in target_objects:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text_to_display = get_object_name(obj_name, target_phrase)
                cv2.putText(image, text_to_display, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_image_path, image)

# Fonction pour traiter une vidéo et effectuer une détection
def process_video(video_path, model, target_objects, output_dir="outputs"):
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

        if target_objects:
            results = model.predict(frame)

            for box in results[0].boxes:
                obj_name = model.names[int(box.cls)]
                if obj_name in target_objects:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    text_to_display = get_object_name(obj_name, target_phrase)
                    cv2.putText(frame, text_to_display, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)
        cv2.imshow('Filtered Video Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Fonction pour traiter un GIF et effectuer une détection
def process_gif(gif_path, model, target_objects, output_dir="outputs"):
    gif = imageio.mimread(gif_path)
    output_gif_path = os.path.join(output_dir, f"processed_{os.path.basename(gif_path)}")
    
    annotated_frames = []

    for frame in gif:
        frame_cv = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if target_objects:
            results = model.predict(frame_cv)

            for box in results[0].boxes:
                obj_name = model.names[int(box.cls)]
                if obj_name in target_objects:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    text_to_display = get_object_name(obj_name, target_phrase)
                    cv2.putText(frame_cv, text_to_display, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        annotated_frames.append(cv2.cvtColor(frame_cv, cv2.COLOR_BGR2RGB))

    imageio.mimsave(output_gif_path, annotated_frames, format='GIF', duration=0.1)

# Création du répertoire de sortie s'il n'existe pas
def ensure_output_directory_exists(output_dir="outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python processMedia.py <media_file_path> <target_phrase>")
        sys.exit(1)

    media_file_path = sys.argv[1]
    target_phrase = sys.argv[2]

    # Extraire les objets cibles de la phrase d'entrée
    target_objects = extract_target_objects(target_phrase)

    # Chargement du modèle YOLO World pré-entraîné
    model = YOLOWorld('yolov8n.pt')

    # Vérification de l'extension du fichier
    extension = os.path.splitext(media_file_path)[1].lower()
    
    # Assurer l'existence du répertoire de sortie
    ensure_output_directory_exists()

    try:
        if extension in ['.jpg', '.jpeg', '.png']:
            process_image(media_file_path, model, target_objects)
        elif extension in ['.mp4', '.avi']:
            process_video(media_file_path, model, target_objects)
        elif extension in ['.gif']:
            process_gif(media_file_path, model, target_objects)
        else:
            print(f"Format de fichier non pris en charge: {extension}")
            sys.exit(1)
    except Exception as e:
        print(f"Une erreur s'est produite lors du traitement: {e}")
        sys.exit(1)

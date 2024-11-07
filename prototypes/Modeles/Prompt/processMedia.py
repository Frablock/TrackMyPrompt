from ultralytics import YOLOWorld
import cv2
import imageio
import os
import sys

# Dictionnaire des classes COCO en anglais et en français
coco_classes = {
    "person": ("personne", "personnes"), "bicycle": ("bicyclette", "bicyclettes"), 
    "car": ("voiture", "voitures"), "motorcycle": ("moto", "motos"),
    "airplane": ("avion", "avions"), "bus": ("autobus", "autobus"), 
    "train": ("train", "trains"), "truck": ("camion", "camions"),
    "boat": ("bateau", "bateaux"), "traffic light": ("feu de circulation", "feux de circulation"), 
    "fire hydrant": ("robinet incendie", "robinets incendie"),
    "stop sign": ("stop", "stops"), "parking meter": ("parcmètre", "parcmètres"), 
    "bench": ("banc", "bancs"), "bird": ("oiseau", "oiseaux"),
    "cat": ("chat", "chats"), "dog": ("chien", "chiens"), 
    "horse": ("cheval", "chevaux"), "sheep": ("mouton", "moutons"), 
    "cow": ("vache", "vaches"),
    "elephant": ("éléphant", "éléphants"), "bear": ("ours", "ours"), 
    "zebra": ("zèbre", "zèbres"), "giraffe": ("girafe", "girafes"),
    "backpack": ("sac à dos", "sacs à dos"), "umbrella": ("parapluie", "parapluies"), 
    "handbag": ("sac à main", "sacs à main"),
    "tie": ("cravate", "cravates"), "suitcase": ("valise", "valises"), 
    "frisbee": ("frisbee", "frisbees"),
    "skis": ("skis", "skis"), "snowboard": ("planche de neige", "planches de neige"), 
    "sports ball": ("ballon de sport", "ballons de sport"),
    "kite": ("cerf-volant", "cerfs-volants"), "baseball bat": ("batte de baseball", "battes de baseball"),
    "baseball glove": ("gant de baseball", "gants de baseball"), 
    "skateboard": ("skateboard", "skateboards"),
    "surfboard": ("planche de surf", "planches de surf"), 
    "tennis racket": ("raquette de tennis", "raquettes de tennis"),
    "bottle": ("bouteille", "bouteilles"), "wine glass": ("verre à vin", "verres à vin"), 
    "cup": ("tasse", "tasses"),
    "fork": ("fourchette", "fourchettes"), "knife": ("couteau", "couteaux"), 
    "spoon": ("cuillère", "cuillères"),
    "bowl": ("bol", "bols"), "banana": ("banane", "bananes"), 
    "apple": ("pomme", "pommes"), "sandwich": ("sandwich", "sandwichs"),
    "orange": ("orange", "oranges"), "broccoli": ("brocoli", "brocolis"), 
    "carrot": ("carotte", "carottes"),
    "hot dog": ("hot dog", "hot dogs"), "pizza": ("pizza", "pizzas"), 
    "donut": ("beignet", "beignets"),
    "cake": ("gâteau", "gâteaux"), "chair": ("chaise", "chaises"), 
    "couch": ("canapé", "canapés"),
    "potted plant": ("plante en pot", "plantes en pot"), 
    "bed": ("lit", "lits"),
    "dining table": ("table à manger", "tables à manger"), 
    "toilet": ("toilette", "toilettes"),
    "tv": ("télévision", "télévisions"), 
    "laptop": ("ordinateur portable", "ordinateurs portables"),
    "mouse": ("souris", "souris"), "remote": ("télécommande", "télécommandes"), 
    "keyboard": ("clavier", "claviers"),
    "cell phone": ("téléphone portable", "téléphones portables"), 
    "microwave": ("micro-ondes", "micro-ondes"),
    "oven": ("four", "fours"), "toaster": ("grille-pain", "grille-pains"), 
    "sink": ("évier", "éviers"),
    "refrigerator": ("réfrigérateur", "réfrigérateurs"), 
    "book": ("livre", "livres"),
    "clock": ("horloge", "horloges"), "vase": ("vase", "vases"), 
    "scissors": ("ciseaux", "ciseaux"),
    "teddy bear": ("ours en peluche", "ours en peluche"), 
    "hair drier": ("sèche-cheveux", "sèche-cheveux"),
    "toothbrush": ("brosse à dents", "brosses à dents")
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

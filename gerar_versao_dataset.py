import os
import shutil
from termcolor import colored
from mtcnn import MTCNN
import cv2


def load_face_detection_model():
    return MTCNN()

def detect_and_crop_face(image_path, detector, output_path=None):
    image = cv2.imread(image_path)
    faces = detector.detect_faces(image)

    if faces:
        (x, y, w, h) = faces[0]['box']
        (x, y) = (max(0, x), max(0, y))
        (endX, endY) = (min(image.shape[1], x + w), min(image.shape[0], y + h))
        face_crop = image[y:endY, x:endX]
        
        if output_path:  # Salva a imagem recortada se o caminho for fornecido
            cv2.imwrite(output_path, face_crop)
        
        return face_crop
    return None


def create_directories(base_dir, subdir_name):
    subdir_path = os.path.join(base_dir, subdir_name)
    os.makedirs(os.path.join(subdir_path, "anchor"), exist_ok=True)
    os.makedirs(os.path.join(subdir_path, "positive"), exist_ok=True)
    os.makedirs(os.path.join(subdir_path, "negative"), exist_ok=True)
    return subdir_path

def process_images(path, destination, detector):
    lista = os.listdir(path)

    for index, item in enumerate(lista):
        imagens = os.listdir(os.path.join(path, item))
        
        # Ignora se não houver imagens suficientes
        if len(imagens) < 2:
            continue

        for img_index, img in enumerate(imagens):
            subdir_name = f"{item}_{img_index}"
            subdir_path = create_directories(destination, subdir_name)

            source_path = os.path.join(path, item, img)
            destino_anchor = os.path.join(subdir_path, "anchor", img)

            detect_and_crop_face(source_path, detector, destino_anchor)

            if img_index + 1 < len(imagens):
                source_positive = os.path.join(path, item, imagens[img_index + 1])
                destino_positive = os.path.join(subdir_path, "positive", imagens[img_index + 1])
                detect_and_crop_face(source_positive, detector, destino_positive)

            # Processa a imagem "negative" da próxima pasta ou da primeira
            next_item = lista[(index + 1) % len(lista)]
            primeira_imagem = os.listdir(os.path.join(path, next_item))[0]
            source_negative = os.path.join(path, next_item, primeira_imagem)
            destino_negative = os.path.join(subdir_path, "negative", primeira_imagem)
            detect_and_crop_face(source_negative, detector, destino_negative)

            print(colored(subdir_name, "yellow"))
            print(colored([img, imagens[img_index + 1] if img_index + 1 < len(imagens) else 'N/A'], "cyan"))


path = "C:\\Users\\amissadai.pinheiro\\Documents\\face_reconhecimento\\train"
destination = "C:\\Users\\amissadai.pinheiro\\Documents\\face_reconhecimento\\dataset_cropado"

# Limpa e recria o diretório de destino
if os.path.exists(destination):
    shutil.rmtree(destination)
os.makedirs(destination, exist_ok=True)


detector = load_face_detection_model()
process_images(path, destination, detector)

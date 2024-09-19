import os
import shutil
from termcolor import colored

path = "C:\\Users\\amissadai.pinheiro\\Documents\\face_reconhecimento\\train"
lista = os.listdir(path)

destination = "C:\\Users\\amissadai.pinheiro\\Documents\\face_reconhecimento\\dataset_amissadai"

try:
    shutil.rmtree(destination)
except:
    pass
try:
    os.mkdir(destination)
except:
    pass

for index, item in enumerate(lista):
    imagens = os.listdir(f"{path}\\{item}")
    
    # Ignora se não houver imagens
    if len(imagens) < 0:
        continue

    # Cria subdiretórios para cada imagem da mesma pessoa
    for img_index, img in enumerate(imagens):
        # Define o nome do subdiretório com base no índice da imagem
        subdir_name = f"{item}_{img_index}"
        subdir_path = os.path.join(destination, subdir_name)
        
        os.mkdir(subdir_path)
        os.mkdir(os.path.join(subdir_path, "anchor"))
        os.mkdir(os.path.join(subdir_path, "positive"))
        os.mkdir(os.path.join(subdir_path, "negative"))
        
        # Copia a imagem para as pastas correspondentes
        destino_anchor = os.path.join(subdir_path, "anchor", img)
        shutil.copyfile(f"{path}\\{item}\\{img}", destino_anchor)

        # Verifica se há uma imagem seguinte para a pasta "positive"
        if img_index + 1 < len(imagens):
            destino_positive = os.path.join(subdir_path, "positive", imagens[img_index + 1])
            shutil.copyfile(f"{path}\\{item}\\{imagens[img_index + 1]}", destino_positive)

        # Escolhe a imagem negativa da próxima pasta ou da primeira, se for a última
        if index + 1 < len(lista):
            primeira_imagem = os.listdir(f"{path}\\{lista[index + 1]}")
            destino_negative = os.path.join(subdir_path, "negative", primeira_imagem[0])
            shutil.copyfile(f"{path}\\{lista[index + 1]}\\{primeira_imagem[0]}", destino_negative)
        else:
            primeira_imagem = os.listdir(f"{path}\\{lista[0]}")
            destino_negative = os.path.join(subdir_path, "negative", primeira_imagem[0])
            shutil.copyfile(f"{path}\\{lista[0]}\\{primeira_imagem[0]}", destino_negative)

        print(colored(subdir_name, "yellow"))
        print(colored([img, imagens[img_index + 1] if img_index + 1 < len(imagens) else 'N/A'], "cyan"))

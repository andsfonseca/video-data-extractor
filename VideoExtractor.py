import numpy as np
from tqdm import tqdm
from cv2 import cv2
import os

class VideoExtractor:
    """Conjunto de Métodos para extração de dados em um vídeo
    """

    def __init__(self):
        return None

    @staticmethod
    def VideoToFrames(path, code=None, skipFrames=0, scalePercent=100, outputFolderPath=None):
        """Recebe um vídeo e retorna um conjunto de Imagens

        Parameters:
            path (String): Caminho do Vídeo
            code (Object): Saída de Cor dos Frames
            scalePercent (Integer): Porcentagem de Escala
            skipFrames (Integer): Ignora um determinado número de Frames
            outputFolderPath (String): Caminho que as imagens serão salvas (Deixar vazio para não salvar)

        Returns:
            Array: Frames Capturados do Video
        """

        frames = []

        cap = cv2.VideoCapture(path)

        counterFrames = 0
        skippedFrames = 0

        size = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        loop = tqdm(total=size//(skipFrames+1), position=0, leave=False)

        while(cap.isOpened()):
            _, frame = cap.read()

            if(frame is None):
                break

            if(skippedFrames == 0):
                skippedFrames = skipFrames
            else:
                skippedFrames -= 1
                continue

            counterFrames += 1

            loop.set_description("Extraindo Frames...")
            loop.update(1)

            if(not code is None):
                frame = cv2.cvtColor(frame, code)

            if(scalePercent != 100):
                
                width = int(frame.shape[1] * scalePercent / 100)
                height = int(frame.shape[0] * scalePercent / 100)
                dsize = (width, height)
                frame = cv2.resize(frame, dsize)

            frames.append(frame)

            if(not outputFolderPath is None):
                _, tail = os.path.split(path)
                filename = os.path.splitext(tail)

                cv2.imwrite(
                    outputFolderPath + filename[0] + "_" + str(counterFrames) + ".jpg", frame)

        loop.close()
        cap.release()

    @staticmethod
    def LoadFramesFromFolder(folderPath, code=None):
        """Lê um conjunto de frames em uma pasta

        Parameters:
            folderPath (String): Caminho dos Frames
            code (Object): Saída de Cor dos Frames

        Returns:
            Array: Frames da Pasta
        """
        frames = []
        for filename in os.listdir(folderPath):
            img = cv2.imread(os.path.join(folderPath,filename))
            if img is not None:
                if(not code is None):
                    img = cv2.cvtColor(img, code)

                frames.append(img)
        return frames
        
    # @staticmethod
    # def RemoveBackgroundFromFrames(frames, method="image"):
    #     if(method == "image"):
    #         pass
    #     return None
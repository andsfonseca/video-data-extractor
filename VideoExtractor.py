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
    def VideoToFrames(path, code=None, skipFrames=0, scalePercent=100, outputFolderPath=None, returnsImagesInsteadOfFilenames = False):
        """Recebe um vídeo e retorna um conjunto de Imagens

        Parameters:
            path (String): Caminho do Vídeo
            code (Object): Saída de Cor dos Frames
            scalePercent (Integer): Porcentagem de Escala
            skipFrames (Integer): Ignora um determinado número de Frames
            outputFolderPath (String): Caminho que as imagens serão salvas (Deixar vazio para não salvar). Caso definida, o nome do arquivo será retornada em vez da imagem
            returnsImagesInsteadOfFilenames (bool): Caso um caminho de saída esteja definido e está flag ativada, o código irá retornar frames em vez de nomes do arquivo 

        Returns:
            Array: Frames Capturados do Video ou Caminho dos Frames em uma pasta
        """

        frames = []

        cap = cv2.VideoCapture(path)

        counterFrames = 0
        skippedFrames = 0

        size = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        zFillCounter = len(str(size))

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

            if(not outputFolderPath is None):
                _, tail = os.path.split(path)
                filename = os.path.splitext(tail)
                
                fullFilename = outputFolderPath + filename[0] + "_" + str(counterFrames).zfill(zFillCounter) + ".jpg"
                cv2.imwrite(fullFilename, frame)
                
                if(returnsImagesInsteadOfFilenames):
                    frames.append(frame)
                else:
                    frames.append(fullFilename)
            else:
                frames.append(frame)

        loop.close()
        cap.release()

        return frames

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
        
    @staticmethod
    def SaveFramesToVideo(frames, outputPath, fourcc=cv2.VideoWriter_fourcc(*'XVID'), fps=20.0):
        """Lê um conjunto de frames em uma pasta

        Parameters:
            frames (Array): Array de Frames do Video
            outputPath (String): Caminho do Video
            fourcc (Object): Codec do Video
            fps (Float): Frames por Segundo

        """
        if (len(frames) == 0): return

        size = len(frames)

        width = frames[0].shape[1]
        height = frames[0].shape[0]
        dsize = (width, height)

        loop = tqdm(total=size, position=0, leave=False)
        out = cv2.VideoWriter(outputPath,fourcc, fps, dsize)

        for frame in frames:
            out.write(frame)
            loop.set_description("Salvando Frame...")
            loop.update(1)
        
        loop.close()
        out.release()

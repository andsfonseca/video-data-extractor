# Extração de dados usando videos

## O que é?

Esta bibliteca contém métodos rápidos que ajudam a manipular dados de videos. Boa parte dos métodos usados aqui já existem na literatura.

Os métodos repositórios foram implementados por mim.

## Notas
 - Foi usado a biblioteca **opencv-python** para leitura dos videos

## Uso

* Importação

```python

from VideoExtractor import VideoExtractor

```

* Leitura do Video 

```python

VideoExtractor.VideoToFrames(path=, code=, skipFrames=, scalePercent=, outputFolderPath=)

```

* Leitura de Frames em uma Pasta (Leitura de Imagens)

```python

frames = VideoExtractorLoadFramesFromFolder(folderPath=, code=)

```



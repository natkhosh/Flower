import torch
import torchvision as tv
from PIL import Image


class Detector:
    """ Базовый класс для детектора

    """
    def __init__(self, model_path="", classes=['Ficus', 'Unknown', 'Saintpaulia', 'Phalaenopsis']):
        """

        :param model_path: путь к сохраненной модели
        :param classes: классы растений из обученного датасета
        """
        self.model_path = model_path
        self.classes = classes
        self.model = torch.load(model_path, map_location=torch.device('cpu'))
        self.model.eval()

    @staticmethod
    def image_transform(image):
        """ Функиця преоразования картинки в тензор и нормализации

        :param image: входное изображение
        :return: возвращает нормализованный тензор
        """

        stats = ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        normalize = tv.transforms.Normalize(*stats, inplace=True)
        transforms = tv.transforms.Compose([
            tv.transforms.ToTensor(),
            normalize
        ])

        return transforms(image)

    def predict(self, image_path):
        """ Функция классификации растения

        :param image_path: путь к изображению растения
        :return: возвращает класс растения
        """

        with open(image_path, 'rb') as f:
            img = Image.open(f)
            img.convert('RGB')
        image = self.image_transform(img)
        xb = image.unsqueeze(0)

        # Получаем предсказание класса растения от модели
        yb = self.model(xb)

        # Выбираем наибольную вероятность
        _, preds = torch.max(yb, dim=1)
        value = torch.max(yb, dim=1)

        # Если коэффициент предсказания меньше 3, то считаем, что модель не угадала и даем класс "Unknown"
        if value[0].item() > 3:
            # Retrieve the class label
            return self.classes[preds[0].item()]
        else:
            return "Unknown"


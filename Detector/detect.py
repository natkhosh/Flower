import torch
import torchvision as tv


class Detector:
    """ Базовый класс для детектора

    """
    def __init__(self, model, classes=['Ficus', 'Unknown', 'Saintpaulia', 'Phalaenopsis']):
        self.model = model
        self.classes = classes
        model.load_state_dict(torch.load(self.model))
        model.eval()

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

    def predict(self, image):
        """ Функция классификации растения

        :param image: изображение растения
        :return: возвращает класс растения
        """

        image = self.image_transform(image)

        # Конфертируем картинку в тензор датасета
        # xb = to_device(img.unsqueeze(0), device)

        xb = image.unsqueeze(0)

        # Получаем предсказание класса растения от модели
        yb = self.model(xb)

        # Выбираем наибольную вероятность
        _, preds = torch.max(yb, dim=1)
        value = torch.max(yb, dim=1)

        # Если коэффициент предсказания меньше 3, то считаем, что мы не угадали и даем класс "Unknown"
        if value[0].item() > 3:
            # Retrieve the class label
            return self.classes[preds[0].item()]
        else:
            return "Unknown"


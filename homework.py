from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight_kg: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration_h
        return avg_speed

    def get_spent_calories(self) -> float:
        raise NotImplementedError('Калории не определены')
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration_h,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20

    def get_spent_calories(self) -> float:
        calories_run = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                        * self.get_mean_speed()
                        - self.CALORIES_MEAN_SPEED_SHIFT)
                        * self.weight_kg / self.M_IN_KM
                        * (self.duration_h * self.H_IN_M)
                        )
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WALKING_COEFFICIENT_1: float = 0.035
    CALORIES_WALKING_COEFFICIENT_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        calories_walk = ((self.CALORIES_WALKING_COEFFICIENT_1
                         * self.weight_kg
                         + (self.get_mean_speed() ** 2
                          // self.height_cm)
                         * self.CALORIES_WALKING_COEFFICIENT_2
                         * self.weight_kg)
                         * (self.duration_h * self.H_IN_M)
                         )
        return calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_SWIMMING_COEFFICIENT_1: float = 1.1
    CALORIES_SWIMMING_COEFFICIENT_2: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_spent_calories(self) -> float:
        calories_swim = ((self.get_mean_speed()
                         + self.CALORIES_SWIMMING_COEFFICIENT_1)
                         * self.CALORIES_SWIMMING_COEFFICIENT_2
                         * self.weight_kg
                         )
        return calories_swim

    def get_mean_speed(self) -> float:
        avg_speed_swim = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration_h
        )
        return avg_speed_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_training: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in type_training:
        raise KeyError(
            f'Нет такого типа тренировки,'
            f'вам доступны только {type_training.keys()}'
            )
    return type_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

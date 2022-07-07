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
    h_in_m: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration_h: float = duration
        self.weight: float = weight

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
                        * self.weight / self.M_IN_KM
                        * (self.duration_h * self.h_in_m)
                        )
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_w_1: float = 0.035
    cf_w_2: float = 0.029
    cf_w_3: float = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_walk = ((self.cf_w_1
                         * self.weight
                         + (self.get_mean_speed() ** self.cf_w_3
                          // self.height)
                         * self.cf_w_2
                         * self.weight)
                         * (self.duration_h * self.h_in_m)
                         )
        return calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    cf_swim_1: float = 1.1
    cf_swim_2: float = 2

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
                         + self.cf_swim_1)
                         * self.cf_swim_2
                         * self.weight
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
        raise KeyError('Нет такого типа тренировки')
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

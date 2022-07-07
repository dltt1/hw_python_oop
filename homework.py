class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; py'
                f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    LEN_STEP_SWIM: float = 1.38
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        distance_swim = self.action * self.LEN_STEP_SWIM / self.M_IN_KM
        return distance and distance_swim

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.__class__.get_distance(self),
                           self.__class__.get_mean_speed(self),
                           self.__class__.get_mean_speed(self),
                           self.__class__.get_spent_calories(self))
    pass


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self, action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories_run = ((self.coeff_calorie_1
                        * self.get_mean_speed()
                        - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                        * (self.duration * 60)
                        )
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_walk_1 = 0.035
    coeff_walk_2 = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float, height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_walk = ((self.coeff_walk_1
                         * self.weight
                         + (self.get_mean_speed() ** 2 // self.height)
                         * self.coeff_walk_2
                         * self.weight)
                         * (self.duration * 60)
                         )
        return calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_swim_1 = 1.1
    coeff_swim_2 = 2.2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        calories_swim = ((self.get_mean_speed()
                         + self.coeff_swim_1)
                         * self.coeff_swim_2
                         * self.weight
                         )
        return calories_swim

    def get_mean_speed(self) -> float:
        avg_speed_swim = (
            self.lenght_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return avg_speed_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())
    """Главная функция."""


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

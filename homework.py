
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
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

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
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )
    pass


class Running(Training):
    """Тренировка: бег."""
    cf_1 = 18
    cf_2 = 20

    def __init__(self, action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories_run = ((self.cf_1
                        * self.get_mean_speed()
                        - self.cf_2) * self.weight / self.M_IN_KM
                        * (self.duration * 60)
                        )
        return calories_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_w_1 = 0.035
    cf_w_2 = 0.029
    cf_w_3 = 2
    h_in_m = 60

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
                         * (self.duration * self.h_in_m)
                         )
        return calories_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    cf_swim_1 = 1.1
    cf_swim_2 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

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

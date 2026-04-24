from typing import List,Tuple
from dataclasses import dataclass
import bisect

@dataclass
class BusStop:
    name: str
    coordinates: Tuple[float, float]
    time_to_next: float
    
    def __str__(self):
        return f"{self.name} ({self.coordinates[0]}, {self.coordinates[1]})"


class BusRoute:
    
    def __init__(self):
        self.stops: List[BusStop] = []
    
    def add_stop(self, name, coordinates: Tuple[float, float], time_to_next):

        new_stop = BusStop(name, coordinates, time_to_next)
        self.stops.append(new_stop)
        print(f"Остановка '{name}' добавлена в маршрут")
    
    def calculate_total_time(self,n):
        
        if not self.stops:
            return 0.0
        
        total_time = sum(stop.time_to_next for stop in self.stops[:n])
        return total_time
    
    def get_bus_position_after_n_stops(self, n):

        if not self.stops:
            return "Маршрут пуст"
        else:
            time_to_stop = self.calculate_total_time(n)
        
        if n <= 0:
            return f"Автобус находится на начальной остановке: {self.stops[0].name}"
        
        if n >= len(self.stops):
            remaining = n - (len(self.stops) - 1)
            if remaining == 0:
                return f"Автобус прибыл на конечную остановку: {self.stops[-1].name}"
            else:
                return f"Автобус отправился обратно {remaining} остановок назад. Конечная: '{self.stops[-1].name}'"
        return f"Через {n} остановок автобус будет на остановке: {self.stops[n].name}, затратив на это {time_to_stop} мин."

    def get_bus_position_after_n_time(self,n):
        
        time_dict = dict()
        total_time = self.calculate_total_time(-1)
        
        if not self.stops:
            return "Маршрут пуст"
        else:
            for i in range(len(self.stops)):
                time_dict[self.calculate_total_time(i)] = self.stops[i].name

        time_keys_list = sorted(time_dict.keys())
        
        if n in time_dict:
            name_station = time_dict.get(n)
            return f"Через {n} мин. автобус будет на остановке {name_station}"

        else:

            pos = bisect.bisect_left(time_keys_list,n)

            if pos == 0:
                return f"Через {n} мин. автобус не начнёт движения, он находится на {self.stops[0].name}"

            elif pos == len(time_keys_list):
                time_waste = n - total_time
                return f"Через {n} мин. автобус приедет на конечную остановку {self.stops[-1].name} и простоит {time_waste} мин." 

            else:
                pred_station = time_keys_list[pos - 1]
                next_station = time_keys_list[pos]
                return f"Через {n} мин. автобус будет между остановками {time_dict[pred_station]} и {time_dict[next_station]}"
                
    def build_reverse_route(self):
        reverse_route = BusRoute()
        
        if not self.stops:
            return reverse_route
        
        reversed_stops = list(reversed(self.stops))
        
        for i, stop in enumerate(reversed_stops):
            if i < len(reversed_stops) - 1:
                original_stop_index = len(self.stops) - 1 - i
                time_to_next = self.stops[original_stop_index - 1].time_to_next if original_stop_index > 0 else 0
                reverse_route.add_stop(stop.name, stop.coordinates, time_to_next)
            else:
                reverse_route.add_stop(stop.name, stop.coordinates, 0)
        
        return reverse_route
    
    def display_route(self):
        if not self.stops:
            print("Маршрут пуст")
            return
        
        print("\nТЕКУЩИЙ МАРШРУТ:")
        print("\n|   Название остановки   |   Местонахождение   |   Время до следующей остановки   |")
        for i, stop in enumerate(self.stops):
            name_stop_time_to_next  = str(stop.time_to_next) + " мин."
            time_con = "Конечная"
            if i < len(self.stops) - 1:
                print(f"|{stop.name:^24}|   Ш:{stop.coordinates[0]}       Д:{stop.coordinates[1]}   |{name_stop_time_to_next:^34}|")
            else:
                print(f"|{stop.name:^24}|   Ш:{stop.coordinates[0]}       Д:{stop.coordinates[1]}   |{time_con:^34}|") 
                

def main():
    route = BusRoute()
    
    print("\nДОБАВЛЕНИЕ ОСТАНОВОК:")
    route.add_stop("Центральный рынок", (55, 37), 2)
    route.add_stop("Площадь Революции", (59, 37), 12)
    route.add_stop("Театральная площадь", (70, 40), 1)
    route.add_stop("Кремль", (70, 41), 6)
    route.add_stop("Вознесенская", (69, 38), 9)
    route.add_stop("Улица 1905 года",(68, 38), 7)
    route.add_stop("Сокольники", (67,38), 12)
    route.add_stop("Вокзальная", (67, 37), 0) #-конечная
    
    
    route.display_route()

    
    print("\nРАСЧЕТ ОБЩЕГО ВРЕМЕНИ ")
    total_time = route.calculate_total_time(-1)
    print(f"Общее время маршрута: {total_time} минут ({total_time/60:.1f} часов)")
    
    print("\nОПРЕДЕЛЕНИЕ ПОЛОЖЕНИЯ АВТОБУСА ")
    test_stops = [0, 2,3, 4, 5, 7]
    for n in test_stops:
        print(route.get_bus_position_after_n_stops(n))

    test_time = [0,1,2,14,17,21,50]
    for n in test_time:
        print(route.get_bus_position_after_n_time(n))
    
    print("\nПОСТРОЕНИЕ ОБРАТНОГО МАРШРУТА ")
    reverse_route = route.build_reverse_route()
    reverse_route.display_route()
    
    reverse_time = reverse_route.calculate_total_time(-1)
    print(f"\nОбщее время обратного маршрута: {reverse_time} минут ({reverse_time/60:.1f} часов)")

if __name__ == "__main__":
    main()

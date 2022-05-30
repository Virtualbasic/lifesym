import random
import time

print('R[d]-zabity królik \n' 'F[d]-zabity lis')
class AppSymulation:
    def __init__(self, size):
        self.size = size
        self._data = {}
        self.flag = True
        self.m = 1
        self.gras_position = []
        self.dirt_position = []
        self.rabb_position = []
        self.fox_position = []
#uzyskiwanie struktury
#sprawdzanie pozycji
    def get_struct(self, value):

        for _lsit in (self.gras_position, self.dirt_position):
            if _lsit:
                _lsit.clear()

        for i in range(3):
            for j in range(-1, 2):
                if i == 0:
                    pos = value - self.size + j
                    if self._data.get(pos):
                        if 'fox' in self._data.get(pos):
                            self.gras_position.append(0)
                        if 'grass' in self._data.get(pos):
                            self.gras_position.append(pos)
                        else:
                            self.dirt_position.append(pos)
                if i == 1:
                    if j == 0:
                        continue

                    pos = value + j
                    if self._data.get(pos):
                        if 'fox' in self._data.get(pos):
                            self.gras_position.append(0)
                        if 'grass' in self._data.get(pos):
                            self.gras_position.append(pos)
                        else:
                            self.dirt_position.append(pos)
                if i == 2:
                    pos = value + self.size + j
                    if self._data.get(pos):
                        if 'fox' in self._data.get(pos):
                            self.gras_position.append(0)
                        if 'grass' in self._data.get(pos):
                            self.gras_position.append(pos)
                        else:
                            self.dirt_position.append(pos)

    # poruszanie się  lisa  , jeśli lis nie znajdzie królika  wyczyszczenie go z z kratki i wstawie nie w jego miejsce F[d]
    # jeśli na kratce  lis nie zastanie królika   zostaje przeniesiony na kolejną losową kratke
    # jeśli zastanie królika zabija go i w miejce krtólika zostaje R[d]
    def move_fox(self, pos, day):
        if self.fox_position:
            if self.m <= 3:
                self.m += 1
            else:
                if 'rabbit' not in self.gras_position + self.dirt_position:
                    self._data[pos].clear()
                    self._data[pos].append('F[d]')
                    tag = 10 * '---'
                    print(f'{tag}\n{day}-go dnia lis umiera z głodu\n{tag}\n')
                    return

        while True:
            step = self.gras_position + self.dirt_position
            idx = random.randint(0, len(step) - 1)
            if 'rabbit' not in self._data[step[idx]] \
                    or 'R[d]' not in self._data[step[idx]]:
                self._data[pos].remove('fox')
                self._data[step[idx]].append('fox')
                break

    # metoda move rabbit  służy do przenoszenie królika  na najbliższą kratke z kratki na której aktualnie się znajduje
    # "logika"
    # kratki zajęte przez innego królika 'rabbit'
    # kratki zajęte przez martwe zwierzę 'R[d], F[d]
    # podst struktura danych [kratka z ziemią, kratka z trawą]
    # obiekty grass_position oraz dirt_position przechowóją indexy danych struktur
    # monitorowane jest przebywanie królika na kratkach bez pożywienia  wszystkie informacje przekładają się na długość życia królika
    def move_rabbit(self, pos, day):
        if self.gras_position:
            if 0 in self.gras_position:
                self._data[pos].clear()
                self._data[pos].append('R[d]')

                tag = 12 * '---'
                print(f'{tag}\n{day}-go dnia królik ginie poprzez kontakt z lisem\n{tag}\n')
                self.m = 1
                return

            while True:
                idx = random.randint(0, len(self.gras_position) - 1)
                if 'rabbit' not in self._data[self.gras_position[idx]] \
                        or 'R[d]' not in self._data[self.gras_position[idx]] \
                        or 'F[d]' not in self._data[self.gras_position[idx]]:
                    print(self._data[pos])

                    self._data[pos].clear()
                    self._data[pos].append('dirt')
                    self._data[self.gras_position[idx]].append('rabbit')
                    break

        else:
            if type(self._data[pos][0]) is not int:
                self._data[pos].insert(0, 0)
            else:
                self._data[pos][0] += 1
                if self._data[pos][0] > 2:
                    self._data[pos].clear()
                    self._data[pos].append('dirt')
                    self._data[pos].append('R[d]')
                    print(self._data[pos])
                    tag = 10 * '---'
                    print(f'{tag}\n{day}-dnia królik umiera z głodu\n{tag}\n')
                    return

            while True:
                idx = random.randint(0, len(self.dirt_position) - 1)
                if 'rabbit' not in self._data[self.dirt_position[idx]] \
                        or 'R[d]' not in self._data[self.dirt_position[idx]] \
                        or 'F[d]' not in self._data[self.dirt_position[idx]]:
                    self._data[pos].remove('rabbit')
                    self._data[self.dirt_position[idx]].append('rabbit')
                    break

    # przegląd siatki
    def view_grid(self, day):
        # kolory siatki
        def set_color(c):
            color = {'fox': '\033[93m',
                     'F[d]': '\033[93m',
                     'rabbit': '\033[m',
                     'R[d]': '\033[m',
                     'grass': '\033[32m',
                     'dirt': '\033[33m'}

            return color[c]

        if not self.check_values():
            return

        if self.rabb_position:
            self.rabb_position.clear()

        if self.fox_position:
            self.fox_position.clear()

        title = f'Size: {self.size}x{self.size} | Day: {day}\n'
        lines = '-' * (len(title) - 1)
        print('\033[0m', f'{title}{lines}')

        s = self.size
        for _x in range(0, s):
            for _y in range(_x * s + 1, _x * s + s + 1):
                print(set_color(self._data[_y][-1]), f'{self._data[_y][-1]:7}', end='')

                if 'rabbit' in self._data[_y]:
                    self.rabb_position.append(_y)
                if 'fox' in self._data[_y]:
                    self.fox_position.append(_y)
            print('')
        print('')

        if not self.rabb_position:
            tag = 15 * '---'
            print(f'{tag}\nSymulacja zakończona Populacja królików wymarła.\n{tag}\n')
            self.flag = False
            return

        for pos in self.rabb_position:
            self.get_struct(pos)
            self.move_rabbit(pos, day)

        if self.fox_position:
            self.get_struct(self.fox_position[0])
            self.move_fox(self.fox_position[0], day)

    # tworzenie  strukt danych + pozycjonowanie
    def create_data(self):
        s = self.size
        for _x in range(0, s):
            for _y in range(_x * s + 1, _x * s + s + 1):
                data_struct = random.sample(['grass'] * 5 + ['dirt'], k=1)
                self._data[_y] = data_struct

                if _y == s / s or _y == s * s:
                    self._data[_y] = data_struct + ['rabbit']
                if _y == s * s // 2:
                    self._data[_y] = data_struct + ['fox']

    def check_values(self):
        if type(self.size) is not int:
            print('Niepoprawny typ danych! Obiekt Oczekuje liczby...')
            return False
        return True

if __name__ == '__main__':
    # Tworzenie obiekt
    sym = AppSymulation(7)
    # Tworzenie domyślnej struktury danych (losowo)
    sym.create_data()
    # printowanie siatki
    for day in range(1, 100):
        if sym.flag:
            sym.view_grid(day)
            time.sleep(0.1)
import random
import sys
import time
from .constants import CASINO_MESSAGES
import typer

class Casino():
    """Великая развлекаловка для студентов"""
    def __init__(self, balance):
        self.balance = balance
        self.casino_price = {
            "❌": 0,
            "🍒": 10,
            "🥝": 20,
            "✈️": 45,
            "7️⃣": 120,
        }
        self.chances = {
            "7️⃣": 0.05,
            "✈️": 0.1,
            "🥝": 0.2,
            "🍒": 0.5,
            "❌": 1
        }
        self.count_multiplier = {
            2: 1.5,
            3: 5
        }
        self.cost = 50
        self.casino_symbols = ["🍒", "🥝", "✈️", "7️⃣", "❌"]
    @staticmethod
    def get_key(d: dict[str, float], value: float) -> str:
        """Получает ключ словаря по значению"""
        for k, v in d.items():
            if v == value:
                return k
        return ''
    def choice_slots(self) -> list:
        """Выбирает слоты по установленным шансам выпадения"""
        slots: list[str | int | float] = []
        for i in range(3):
            cur_chance = random.random()
            for chance in self.chances.values():
                if cur_chance <= chance:
                    slots.append(self.get_key(self.chances, chance))
                    break
        win_sum = self.summarize_win(slots)
        slots.append(win_sum)
        return slots
    def summarize_win(self, slots: list) -> float:
        """Подсчет суммы выиграша"""
        win_total = 0
        unique_slots = set(slots)
        for slot in unique_slots:
            slot_count = slots.count(slot)
            if slot_count > 1:
                win_total += self.casino_price[slot] * slot_count * self.count_multiplier[slot_count]
            else:
                win_total += self.casino_price[slot]
        return win_total

    def spin(self, duration):
        """Основная функция, осуществляющая прокрутку казино"""
        if self.balance - 50 >= 0:
            self.balance -= 50
            typer.echo(f"🎰 {random.choice(CASINO_MESSAGES)}")
            start_time = time.time()
            i = 1
            while time.time() - start_time < duration:
                slots = [random.choice(self.casino_symbols) for x in range(3)]
                sys.stdout.write(f"\r[{slots[0]} | {slots[1]} | {slots[2]}]")
                sys.stdout.flush()
                time.sleep(0.1 * i)
                i += 1
            final_slots = self.choice_slots()
            typer.echo(f"\r[{final_slots[0]} | {final_slots[1]} | {final_slots[2]}]")
            self.balance += final_slots[-1]
        else:
            typer.echo("😭 Баланс ледокоинов на нуле\nПромокод ledocol - 500 ледокоинов фрибета")
        return 0

from random import randint
import requests
from random import randint
class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1,1000)

        self.level = 1
        self.xp_now = 0
        self.xp_need = 100

        self.hp_max = 1
        self.hp_now = 1
        self.power = 1

        self.img = self.get_img()
        self.name = self.get_name()
        self.abilities = self.get_abilities()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon-form/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['front_default'])
        else:
            return "https://static.wikia.nocookie.net/pokemon/images/0/0d/025Pikachu.png/revision/latest/scale-to-width-down/1000?cb=20181020165701&path-prefix=ru"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"
    # Метод для получения способностей покемона через API
    def get_abilities(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data1 = response.json()
            abilities = {}
            for ability in data1['abilities']:
                url = ability["ability"]["url"]
                response = requests.get(url)
                if response.status_code == 200:
                    data2 = response.json()
                    for effect in data2["effect_entries"]:
                        if effect["language"]["name"] == "en":
                            abilities[ability["ability"]["name"]] = effect["effect"]
            return abilities
        else:
            url = f'https://pokeapi.co/api/v2/pokemon/25'
            response = requests.get(url)
            if response.status_code == 200:
                data1 = response.json()
                abilities = {}
                for ability in data1['abilities']:
                    url = ability["ability"]["url"]
                    response = requests.get(url)
                    if response.status_code == 200:
                        data2 = response.json()
                        for effect in data2["effect_entries"]:
                            if effect["language"]["name"] == "en":
                                abilities[ability["ability"]["name"]] = effect["effect"]
                return abilities

    # Метод класса для получения информации
    def info(self):
        return {"name": self.name,
                "hp_now": self.hp_now,
                "hp_max": self.hp_max,
                "power": self.power,
                "level": self.level,
                "xp_now": self.xp_now,
                "xp_need": self.xp_need,
                "abilities": self.abilities}

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    # Метод класса для повышение опыта покемона
    def uppend_xp(self, xp): #1 - новый уровень
        if self.xp_now + xp >= self.xp_need:
            self.xp_need += 50
            self.level += 1
            self.xp_now = 0
            self.hp_max += 20
            self.hp_now = self.hp_max
            self.power += 5
            return 1
        else:
            self.xp_now += xp
        

    # Метод класса для атаки другого покемона
    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp_now > self.power:
            enemy.hp_now -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}\nЗдоровье @{enemy.pokemon_trainer} теперь {enemy.hp_now}"
        else:
            enemy.hp_now = 0
            xp = randint(50,100)
            result = self.uppend_xp(xp)
            if result == 1:
                return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!\n@{self.pokemon_trainer} достигает необходимого кол-ва опыта и повышает свой уровень на 1!"
            else:
                return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!\n@{self.pokemon_trainer} получает {xp} опыта!"    


class Wizard(Pokemon):
    def __init__(self,pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp_max = randint(300,450)
        self.hp_now = self.hp_max
        self.power = randint(10,20)
        self.type = "Волшебник"

    def info(self):
        result = super().info()
        result["type"] = self.type
        return result
    
class Fighter(Pokemon):
    def __init__(self,pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.hp_max = randint(200,350)
        self.hp_now = self.hp_max
        self.power = randint(20,30)
        self.type = "Боец"

    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power} "
    
    def info(self):
        result = super().info()
        result["type"] = self.type
        return result
    
# if __name__ == '__main__':
#     wizard = Wizard("username1")
#     fighter = Fighter("username2")

#     print(wizard.info())
#     print()
#     print(fighter.info())
#     print()
#     print(fighter.attack(wizard))
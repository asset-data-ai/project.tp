class Player:
    def __init__(self, name, hp, dam):
        self.name = name
        self.hp = hp
        self.dam = dam

    def atak(self, other):
        other.hp-=self.dam
    def heal(self,other):
        other.hp += 20
while True:

p=Player('Azamat',1000,50)
p1=Player('Mansur',100,3)
p.atak(p1)
print(p1.hp)
p1.heal(p)
print(p.hp)


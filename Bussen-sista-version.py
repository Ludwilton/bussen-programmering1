# importerar nödvändiga moduler
import re
import random


# klass för passagerare
class Passenger:
    def __init__(self, age, gender):
        self.age = age # ålder
        self.gender = gender # kön
        self.ticket_bought = False  # variabel för att hålla koll på biljettstatus, Initialt är biljetten inte köpt
        self.calc_and_set_ticket()  # Beräkna och sätt biljettstatus
    
    def calc_and_set_ticket(self):
        # Beräkna biljettstatus baserat på ålder, används för poke funktionen
        if self.age < 12:
            self.ticket_bought = random.random() < 0.95  # 95% chans att ha biljett för ålder < 12
        elif 12 <= self.age <= 22:
            self.ticket_bought = random.random() < 0.5   # 50% chans för åldrar 12 - 22
        elif 22 < self.age <= 35:
            self.ticket_bought = random.random() < 0.75  # 75% chans för åldrar 23 - 35
        elif 35 < self.age <= 60:
            self.ticket_bought = random.random() < 0.9   # 90% chans för åldrar 36 - 60
        elif 60 < self.age <= 90:
            self.ticket_bought = random.random() < 0.98  # 98% chans för åldrar 60 - 90
        else:
            self.ticket_bought = random.random() < 0.5   # 50% chans för åldrar över 90

# klass som representerar bussen
class bus:
    def __init__(self):
        self.passengers = [None] * 25 # representerar 25 platser på bussen
        self.passenger_count = 0 # variabel för att hålla reda på hur många passagerare det är på för tillfället
        self.max_capacity = 25 # variabel för max capacitet i bussen

    
    def menu(self):  # visar menyn med alternativ för användaren
        print("\nVad vill du göra?")
        print("1. låt en passagerare gå på")
        print("2. visa vart alla passagerare sitter")
        print("3. Beräkna den totala åldern av alla passagerare")
        print("4. Beräkna den genomsnittliga åldern av alla passagerare")
        print("5. Visa passageraren med högst ålder")
        print("6. Visa passagerare inom en specifik åldersgrupp")
        print("7. Sortera passagerare efter ålder")
        print("8. Visa antalet manliga respektive kvinnliga passagerare")
        print("9. Gör en biljettkontroll!")
        print("10. Låt en passagerare gå av bussen")
        print("11. Rusningstrafik! Fyll bussen med slumpade passagerare") # främst finns denna funktion för debugging
        print("12. Avsluta programmet")

        
    def is_full(self): # kontrollerar om bussen är full. (gör detta till en funktion för att göra koden modulär)
        return self.passenger_count == self.max_capacity
        

    def populate_bus(self): # fyller bussen med en rimlig uppsättning av olika åldrar!
        if self.is_full(): # kontrollerar om bussen är full
            print("Bussen är redan full.")
            return
        
        # kollar antal passagerare som får plats
        total_passengers = self.max_capacity - self.passenger_count  
        
        under_12_count = int(total_passengers * 0.20) # tilldelar ett visst antal passagerare per åldersgrupp
        between_12_65_count = int(total_passengers * 0.70)
        over_65_count = total_passengers - under_12_count - between_12_65_count
        
        # genererar slumpmässigt olika åldersgrupper
        under_12_ages = [random.randint(0, 11) for _ in range(under_12_count)]
        between_12_65_ages = [random.randint(12, 65) for _ in range(between_12_65_count)]
        over_65_ages = [random.randint(66, 100) for _ in range(over_65_count)]      

        all_ages = under_12_ages + between_12_65_ages + over_65_ages           # kombinerar åldersgrupperna

        random.shuffle(all_ages)# blandar passagerare
        
        # slumpmässigt ger passagerarna kön
        genders = random.choices(["M", "F"], k=self.max_capacity)
        
        # variabel antalet passagerare som lagts till
        added_passengers = 0
        
        # lägger till passagerarna på bussen
        for age, gender in zip(all_ages, genders):
            self.add_passenger(age, gender, silent=True) #silent funktionen gör så att add_passenger() inte fyller terminalen med 25 meddelanden. istället används added_passengers
            added_passengers += 1
        
        # printar antalet tillagda passagerare
        print(f"{added_passengers} passagerare har hoppat på bussen.")


    def add_passenger(self, age, gender, silent=False): # lägger till en passagerare på bussen
        if self.is_full(): # kollar om det finns plats. # denna del ligger nu istället i inmatningen - låter ligga kvar för anteckningars skull.
            if not silent: # silent funktionen finns för att inte spamma terminalen när "populate_bus"
                print("Bussen är full. Det finns inga lediga platser.")
        else:
            new_passenger = Passenger(age, gender)
            self.passengers[self.passenger_count] = new_passenger
            self.passenger_count += 1
            if not silent:
                print(f"Passagerare tillagd på plats {self.passenger_count}.")


    def print_bus(self): # skriver ut information om passagerare, med plats, ålder, kön.
        print("+----------------------------+") # ram för att visualisera en buss

        for seat in range(1, 26):
            passenger_info = ""
            if seat <= self.passenger_count:
                passenger = self.passengers[seat - 1] 
                passenger_info = f"Ålder: {passenger.age}, Kön: {passenger.gender}" # variabel för att hålla information om varje passagerare
            print(f"| Säte {seat}: {passenger_info.ljust(19)}|") # skriver ut
        print("+----------------------------+") # resterande ram


    def calc_total_age(self): # kalkylerar totala åldern för alla passagerare sammanlagt
        total_age = sum(passenger.age for passenger in self.passengers[:self.passenger_count]) 
        print(f"Den totala åldern av alla passagerare är: {total_age}") 


    def calc_average_age(self): # kalkylerar genomsnittsåldern av alla passagerare
        if not self.passengers:
            print("Det finns inga passagerare i bussen.")
        else:
            total_age = sum(passenger.age for passenger in self.passengers[:self.passenger_count])
            average_age = total_age / self.passenger_count
            print(f"Genomsnittsåldern i bussen är: {average_age:.2f}") # skriver ut


    def max_age(self): # hittar passageraren med högst ålder på bussen med en for
        if not self.passengers: # kollar om bussen är tom först
            print("Det finns inga passagerare på bussen.")
            return
        
        max_age = self.passengers[0].age 
        max_age_index = 0
        
        for index, passenger in enumerate(self.passengers[1:]):
            if passenger is not None and passenger.age > max_age:
                max_age = passenger.age
                max_age_index = index + 1 # justerar index 
        print(f"Passageraren med högst ålder ({max_age}) sitter på plats {max_age_index+1}.") # skriver ut


    def find_age(self, age_range): # Sök efter passagerare inom ett angivet åldersintervall med formatet nummerlågt-nummerhögt.
        try:
            # Splitta intervallet i start- och slutålder   /att kunna skriva in t.ex 20-50 var klurigt att få till, använde mig av regex i input
            start_age, end_age = age_range.split("-")
            start_age = int(start_age)
            end_age = int(end_age)

            if start_age <= end_age:
                found_positions = [] # initierar

                # iterera genom listan av passagerare
                for index, passenger in enumerate(self.passengers):
                    if passenger is not None and start_age <= passenger.age <= end_age:
                        found_positions.append(index)

                if found_positions:
                    print(f"Passagerare inom åldersintervallet {start_age}-{end_age} hittas på platserna: {', '.join(str(position + 1) for position in found_positions)}")
                else:
                    print(f"Det finns inga passagerare inom åldersintervallet {start_age}-{end_age} på bussen.")
            else:
                print("Felaktigt intervall.")
        except ValueError:
            print("Felaktig inmatning. Ange ett giltigt åldersintervall från lågt till högt. t.ex 20-55")

    def sort_bus(self): # sorterar passagerare i stigande ålder med bubble sort, utan att lämna tomma säten mellan passagerare.

        # filtrerar ut none värden
        passengers = [passenger for passenger in self.passengers if passenger is not None]

        is_sorted = False # med syfte av optimering men inte implementerats ännu.

        while not is_sorted:
            is_sorted = True

            for i in range(len(passengers) - 1):
                # jämför nuvarande och nästa passagerares ålder
                if passengers[i].age > passengers[i + 1].age:
                    # byt ut passagerarna ifall nuvarande är äldre än nästa
                    passengers[i], passengers[i + 1] = passengers[i + 1], passengers[i]
                    is_sorted = False

 # fyller på lista med none värden så att add_passenger() fungerar korrekt. utan detta kraschade programmet när man försökte fylla bussen efter sortering.
        if len(passengers) < self.max_capacity:
            noneList = [None] * (self.max_capacity - len(passengers))
            passengers.extend(noneList)

        # updaterar listan
        self.passengers = passengers
        self.print_bus() # printar bussen här också för att visa sorteringen.
        print("Efter mycket stök och tumult på bussen har den sorterats i åldersordning.")


    def print_gender(self): # räknar och skriver ut antalet av varje kön
        male_count = 0 # initierar variabler
        female_count = 0

        for passenger in self.passengers:
            if passenger is not None: # om platsen inte är tom ..
                if passenger.gender == "M": # om passagerarens kön är "M" för male så
                    male_count += 1 # inkrementerar variabel med 1
                elif passenger.gender == "F":
                    female_count += 1
        print(f"Antal manliga passagerare: {male_count}") # skriver ut
        print(f"Antal kvinnliga passagerare: {female_count}")


    def poke(self, passenger_index): # biljettkontroll
        passenger_index -= 1  # justerar index
        if passenger_index < 0 or passenger_index >= self.passenger_count: # kollar så att det sitter person på vald plats
            print("Det sitter ingen på den platsen!")
        else:
            passenger = self.passengers[passenger_index]
            if passenger is not None: # kollar om passagerare finns
                if passenger.ticket_bought: # kollar om biljett finns
                    print(f"Passagerare på plats {passenger_index + 1} har en biljett.")
                else: # om inte 
                    print(f"Passagerare på plats {passenger_index + 1} har ingen biljett. Personen tas bort från bussen.")
                    self.remove_passenger(passenger_index + 1)  # justerar index och kallar på remove_passenger
            else: # TODO tekniskt sett är denna del överflödig nu eftersom input delen hanterar fel nu istället? (låter vara kvar tills vidare då det inte påverkar funktionalitet)
                print("Felaktigt index. Ange ett värde mellan 1 och {}.".format(self.passenger_count))


    def remove_passenger(self, passenger_index): # funktion för att slänga av passagerare, kallas av poke funktionen.
        passenger_index -= 1  # Justera index igen..
        if passenger_index < 0 or passenger_index >= self.passenger_count:
            print("Det sitter ingen på den platsen!.")
        else:
            removed_passenger = self.passengers[passenger_index]
            passenger_removed = False  # bool för att hålla reda på om någon har blivit avslängd

            if removed_passenger.age < 18: # printar olika strängar beroende på vilken ålder personen har
                print(f"En tonårsrevolterande passagerare, {removed_passenger.age} år gammal, blev avslängd bussen!") 
                print("Hen skrek något om att bara åka en hållplats för 36kr är absurt! De flesta på bussen verkar hålla med.")
                passenger_removed = True
            elif removed_passenger.age < 25:
                print(f"En ung och eventyrlig {removed_passenger.age}-åring, har slängts av bussen för att följa sina drömmar om att resa jorden runt! (till fots alltså)")
                passenger_removed = True
            elif removed_passenger.age > 80:
                print(f"Bussen har stannat för att släppa av en {removed_passenger.age}-åring med tillhörande rullator som nu får jobba övertid!")
                passenger_removed = True
            else:
                print(f"Passagerare {removed_passenger.age} år gammal har sparkats av under färd. De andra passagerarna är förskräckta och ser ut att köpa biljetter. Föraren Bosse har ringt ambulans.")
                passenger_removed = True

            # Om en passagerare har blivit avslängd köper de andra passagerarna biljetter
            if passenger_removed:
                for passenger in self.passengers:
                    if passenger is not None:
                        passenger.ticket_bought = True

            all_tickets_bought = all(passenger.ticket_bought for passenger in self.passengers if passenger is not None)
            if all_tickets_bought:
                print("Alla passagerare har nu en biljett!")

            # Justera platser så att det inte finns tomrum mellan passagerare
            for i in range(passenger_index, self.passenger_count - 1):
                self.passengers[i] = self.passengers[i + 1]
            self.passengers[self.passenger_count - 1] = None
            self.passenger_count -= 1


    def getting_off(self, passenger_index): # tar bort specifierad passagare från bussen(listan)
        passenger_index -= 1  
        if passenger_index < 0 or passenger_index >= self.passenger_count:
            print("Det sitter ingen på den platsen!.")
        else:
            removed_passenger = self.passengers[passenger_index] # tar bort person,printar,justerar listan, och uppdaterar även passenger count
            print(f"Passagerare {removed_passenger.age} år gammal har stigit av bussen.")
            for i in range(passenger_index, self.passenger_count - 1):
                self.passengers[i] = self.passengers[i + 1]
            self.passengers[self.passenger_count - 1] = None
            self.passenger_count -= 1


    def exit_program(self): #avslutar programmet
        print("Programmet avslutas.")
        exit()
    
        
    def run(self): # kör menyn och kallar till alla funktioner efter vad som valts, varje del av menyn hanterar felinmatning beroende på vilket val man väljer.
        menureturn = "Tryck på Enter för att återgå till menyn..." # variabel för att reducera röra i loopen -  används med f sträng "input(f"{menureturn})"

        print("Välkommen till Buss-simulatorn!")
        while True: # startar loopen
            self.menu() # skriver ut menyn 
            choice = input("Ange ditt val: ").strip().lower() # ber om inmatning som tilldelas till "choice"

            if choice == '12':
                self.exit_program()
                break  # avslutar programmet efter exit valts

            elif choice == '1':
                if self.is_full():
                    print("Bussen är redan full. Ingen passagerare kan läggas till.")
                    input(f"{menureturn}")
                else:
                    while True:
                        try:
                            age = int(input("Ange passagerarens ålder: "))
                            if age < 0 or age > 122: # 0-122 kändes som ett rimligt intervall
                                raise ValueError("Ålder måste vara ett positivt heltal.")
                            break
                        except ValueError:
                            print("Felaktig inmatning.  Ange ett positivt heltal för ålder.")

                    gender = input("Ange passagerarens kön (M/F): ").strip().upper() # rengör och konverterar till Caps i syfte av nästa rad
                    while gender not in ["M", "F"]:
                        gender = input("Felaktigt kön. Ange M eller F: ").strip().upper()

                    self.add_passenger(age, gender)
                    input(f"{menureturn}")

            elif choice == '2':
                self.print_bus()
                input(f"{menureturn}")

            elif choice == '3':
                self.calc_total_age()
                input(f"{menureturn}")

            elif choice == '4':
                self.calc_average_age()
                input(f"{menureturn}")

            elif choice == '5':
                self.max_age()
                input(f"{menureturn}")


            elif choice == '6':
                while True:
                    try:
                        age_range = input("Ange åldersintervall t.ex. '20-55': ")
                        pattern = r'^(\d+)-(\d+)$'  # Regex pattern för formatet 'num-num' (t.ex 20-55)
                        
                        if re.match(pattern, age_range):
                            start_age, end_age = map(int, age_range.split('-'))
                            if 0 <= start_age <= 122 and 0 <= end_age <= 122:
                                self.find_age(age_range)
                                break
                        raise ValueError
                    except ValueError:
                        print("Felaktig inmatning. Ange ett giltigt åldersintervall i formatet 'lägsta-högsta' mellan 0 och 122.")
                input(f"{menureturn}")


            elif choice == '7':
                self.sort_bus()
                input(f"{menureturn}")

            elif choice == '8':
                self.print_gender()
                input(f"{menureturn}")
            
            elif choice == '9':
                while True:
                    try:
                        self.print_bus()
                        passenger_index = int(input("biljettkontroll! Ange en passagerare: "))
                        if passenger_index < 1 or passenger_index > 25:
                            raise ValueError("Index måste vara mellan 1 och 25.")
                        break
                    except ValueError: 
                        print("Felaktig inmatning. Ange ett värde mellan 1 och 25.")

                self.poke(passenger_index)
                input(f"{menureturn}")


            elif choice == '10':
                self.print_bus() # skriver ut bussen innan inmatning för att göra upplevelsen bättre
                while True:
                    try:
                        passenger_index = int(input("Ange vilken plats passageraren sitter på: "))
                        if passenger_index < 1 or passenger_index > 25:
                            raise ValueError
                        break  # Bryter loop om inmatningen är ogiltig
                    except ValueError:
                        print("Felaktig inmatning. Ange ett värde mellan 1 och 25.")

                self.getting_off(passenger_index)
                input(f"{menureturn}")

                            
            elif choice == '11':
                self.populate_bus()
                input(f"{menureturn}")

            else:
                print("Ogiltigt val. Välj ett nummer mellan 1 och 12.")



class Program: # representerar simulatorn
    def __init__(self):  # kallas efter när en ny ionstans skapas
        self.minbus = bus() # skapar ett nytt buss objekt och sparar det som en attribut
        self.run_program() # ansvarar för att köra simulatorn

    def run_program(self): # loopar oändligt
        while True:

            self.minbus.run()  # Kör bussen


if __name__ == "__main__":
    # skapa en instans (kopia) av klassen Program 
    my_program = Program()














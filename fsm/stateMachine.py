plant_total = 0
rows = 5
cols = 16
germination_map = []
for i in range(rows):
    germination_map.append(["Status: "]*cols)


class State(object):

    def __init__(self):
        print("Processing current state: "), str(self)

    def on_event(self, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class Start(State):
    def on_event(self, event):
        if event == ("systems_initilized"):
            print("All systems initilized!")
            return Move()
        return self


class Move():
    def on_event(self, event):
        if plant_total == 64:  # i am not sure why this is throwing an error
            return End()
        # insert code to make robot move a certain amount IF it is at the beginning of a row
        # IF robot is at the end of a row, have it turn the corner to the next row
        # ELSE move robot 4 inches forward
        if event == ("plant_detected"):
            plant_total += 1  # i am not sure why this is throwing an error
            return Sensing()
        return self


class Sensing():
    # inset code to make robot identify germination status of plant
    def on_event(self, event):
        for i in range(rows):
            germinated_counter = 0
            for j in range(cols):
                if event == ("non_germination"):
                    germination_map[i][j].append("non_germination")
                    return Actuation()
                elif event == ("stressed"):
                    germinated_counter += 1
                    germination_map[i][j].append("single stressed seedling")
                    return Move()
                elif event == ("healthy"):
                    germinated_counter += 1
                    germination_map[i][j].append("single healthy seedling")
                    return Move()
            print("Row " + i + " Population Density: " + germinated_counter)
        return self


class Actuation():
    def on_event(self, event):
        if event == ("actuation"):
            # insert code that performs acutation on non-germination plants
            return Move()
        return self


class End():
    def on_event(self, event):
        # insert code to turn motors off
        for i in range(rows):
            for j in range(cols):
                print(germination_map[i][j])
        return self

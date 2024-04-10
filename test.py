class sheep:
    def __init__(self):
        self.carried = True

sheep = [sheep() for i in range(3)]

print([sheepbit.carried for sheepbit in sheep])
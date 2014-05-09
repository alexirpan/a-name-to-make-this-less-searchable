class Mod(object):
    P = 2
    inverses = []

    @staticmethod
    def egcd(a, b):
        """Find EGCD(a, b).
        """
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = Mod.egcd(b % a, a)
            return (g, x - (b / a) * y, y)

    @staticmethod
    def calculate_inverses():
        Mod.inverses = [None] * Mod.P
        for x in range(1, Mod.P):
            g, inv, y = Mod.egcd(x, Mod.P)
            Mod.inverses[x] = Mod.mod(inv)

    @staticmethod
    def mod(x):
        """Return x mod P (in the range 0...P-1).
        """
        if x < 0:
            x = -(-x % Mod.P)
        return (x + Mod.P) % Mod.P

    @staticmethod
    def mod_div(x, y):
        """Return x / y mod P.
        """
        x, y = Mod.mod(x), Mod.mod(y)
        return (x * Mod.inverses[y]) % Mod.P

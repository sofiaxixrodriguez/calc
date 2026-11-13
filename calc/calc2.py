class Calculadora:
    def __init__(self):
        self.__resultado = 0.0
        self._target = "="
        
    @property # getter
    def resultado(self):
        return self.__resultado
    
    @resultado.setter
    def resultado(self, valor):
        self.__resultado = valor
    
    def initial_msg(self):
        print("Modos disponibles:\n\tBASE -> base\n\tCIENTÍFICA -> cien\n\tPROGRAMACIÓN -> prog\n")

    def calc(self, op_input, num):
        match op_input:
            case "+":
                self.resultado += num
            case "-":
                self.resultado -= num
            case "x":
                self.resultado *= num
            case "/":
                if num == 0:
                    print("Error: División por cero.")
                else:
                    self.resultado /= num
            case _:
                print("Operación no permitida.")
        return self.resultado


class CalculadoraBase(Calculadora):
    def __init__(self):
        super().__init__()

    def start_msg(self):
        print("Modo: BASE\nOperaciones permitidas:\n\tSUMA -> +\n\tRESTA -> -\n\tMULTIPLICACIÓN -> x\n\tDIVISION -> /\n")

    def calc(self, op_input, num):
        match op_input:
            case "+" | "-" | "x" | "/":
                return super().calc(op_input, num)
            case _:
                print("Operación no permitida en modo BASE.")
        return self.resultado


class CalculadoraCientifica(Calculadora):
    def __init__(self):
        super().__init__()

    def start_msg(self):
        print("Modo: CIENTÍFICA\nOperaciones permitidas:\n\tPOTENCIA -> p\n\tFACTORIAL -> f\n\tRAÍZ CUADRADA -> r\n\tECUACIÓN 2do GRADO -> s\n")

    def fact(self, num):
        if num < 0:
            print("Error: El factorial no está definido para números negativos.")
            return None
        res = 1
        num_int = int(num)
        while num_int >= 1:
            res *= num_int
            num_int -= 1
        return float(res)

    def pot(self, num, elv):
        res = 1
        elv_int = int(elv)
        while elv_int > 0:
            res *= num
            elv_int -= 1
        return float(res)

    def sq_root(self, sq):  # babylonian method
        if sq < 0:
            return None
        if sq == 0:
            return 0.0
        root = 1.0
        while True:
            t_root = round(((root + (sq / root)) / 2), 3)
            if abs(root - t_root) < 0.0001:
                return t_root
            root = t_root

    # utils ec_seg_grado
    def _inc_b(self, a, c):
        x = self.sq_root(-c / a)
        print("Ecuación incompleta, falta b.\n")
        if x is None:
            print("No tiene soluciones reales.")
            return None      
        x = round(x, 3)
        print(f"Resultados: x1 = {-x}, x2 = {x}")
        return -x, x

    def _inc_c(self, a, b):
        x1 = 0.0
        x2 = round(-b / a, 3)
        print("Ecuación incompleta, falta c.")
        print(f"Resultados: x1 = {x1}, x2 = {x2}")
        return x1, x2

    def _inc_a(self, b, c):
        if b == 0:
            print("No es una ecuación válida.")
            return None
        x1 = round(-c / b, 3)
        print("No es una ecuación de segundo grado (lineal).")
        print(f"Resultado: x1 = {x1}")
        return x1, None

    def ec_seg_grado(self, a, b, c):
        if a == 0:
            return self._inc_a(b, c)
        if b == 0:
            return self._inc_b(a, c)
        if c == 0:
            return self._inc_c(a, b)
        
        disc = (b * b) - (4 * a * c)
        if disc < 0:
            print("La ecuación no tiene soluciones reales, discriminante negativo.")
            return None
        
        x1 = round((-b + self.sq_root(disc)) / (2 * a), 3)
        x2 = round((-b - self.sq_root(disc)) / (2 * a), 3)
        print(f"Resultados: x1 = {x1}, x2 = {x2}")
        return x1, x2


    def keep_result(self, res):
        if res is None:
            return self.resultado
        
        saved = input(f"Resultado obtenido: {res}. ¿Quieres conservarlo? S (sí) / N (descartar)\n").lower()
        if saved == "s":
            op_input = input("¿Qué quieres hacer con este resultado? +, -, x, /\n")
            return super().calc(op_input, res)
        else:
            print("Resultado descartado.")
            return self.resultado

    def calc(self, op_input, num):
        match op_input:
            case "p":
                base = float(input("Introduce la base de la potencia: \n"))
                elv = float(input("Introduce el exponente (entero positivo): \n"))
                res = self.pot(base, elv)
                return self.keep_result(res)
                
            case "f":
                val = float(input("Introduce el número para calcular su factorial: \n"))
                res = self.fact(val)
                return self.keep_result(res)
                
            case "r":
                val = float(input("Introduce el número para calcular su raíz cuadrada: \n"))
                res = self.sq_root(val)
                if res is None:
                    print("Error: No se puede calcular la raíz de un número negativo.")
                    return self.resultado
                return self.keep_result(res)
                
            case "s":
                print("Para ax^2 + bx + c = 0")
                a = float(input("Introduce el término a: \n"))
                b = float(input("Introduce el término b: \n"))
                c = float(input("Introduce el término c: \n"))
                r_ec = self.ec_seg_grado(a, b, c)
                
                if r_ec is None:
                    return self.resultado
                
                saved = input("¿Quieres conservar algún resultado? x1, x2, N (descartar)\n").lower()
                if saved in ["x1", "x2"]:
                    op_input_acum = input("¿Qué quieres hacer con este resultado? +, -, x, /\n")
                    num_elegido = r_ec[0] if saved == "x1" else r_ec[1]
                    return super().calc(op_input_acum, num_elegido)
                else:
                    print("Resultado descartado.")
                    return self.resultado
            case _:
                print("Operación no permitida en modo CIENTÍFICA.")
                return self.resultado

class CalculadoraProgramacion(Calculadora):
    def __init__(self):
        super().__init__()

    def start_msg(self):
        print("Modo: PROGRAMACIÓN\nOperaciones permitidas:\n\tCONVERSIÓN HEXADECIMAL -> hex\n")

    def dec_hex(self, n):
        if n < 0:
            print("Error: Solo se permiten números enteros positivos.")
            return None
        hex_str = "0123456789ABCDEF"
        hexadecimal = ""
        n_int = int(n)
        if n_int == 0:
            return "0"
        while n_int > 0:
            residuo = n_int % 16
            hexadecimal = hex_str[residuo] + hexadecimal
            n_int = n_int // 16
        return hexadecimal

    def calc(self, op_input, num):
        if op_input == "hex":
            val = float(input("Introduce el número entero positivo a convertir a hexadecimal: "))
            resultado_hex = self.dec_hex(val)
            if resultado_hex is not None:
                print(f"El número {int(val)} en hexadecimal es: {resultado_hex}")
                print("(Operación informativa: El valor actual no se modifica)")
            return self.resultado
        else:
            print("Operación n permitida en modo PROGRAMACIÓN.")
            return self.resultado

class InterfazCalculadora:
    def __init__(self):
        self.modos = {
            "base": CalculadoraBase(),
            "cien": CalculadoraCientifica(),
            "prog": CalculadoraProgramacion()
        }

        self.current_mode = "base"
        self.calc_mode = self.modos[self.current_mode]

    def change_modo(self, nuevo_modo):
        resultado_actual = self.calc_mode.resultado
        self.current_mode = nuevo_modo
        self.calc_mode = self.modos[nuevo_modo]
        self.calc_mode.resultado = resultado_actual
        
        self.calc_mode.start_msg()

    def starter_num(self):
        while True:
            num_input = input("Introduce un número:\n").strip().lower()
            
            if num_input == self.calc_mode._target:
                print(f"Resultado final: {self.calc_mode.resultado}")
                exit()        
            
            if num_input in self.modos:
                self.change_modo(num_input)
                continue
                
            try:
                return float(num_input)
            except ValueError:
                print("No es un número válido.")
                return 0.0

    def run(self):
        self.calc_mode.initial_msg()
        print(f"Escribe '{self.calc_mode._target}' para salir u obtener el resultado final.\n")
        self.calc_mode.start_msg()
        
        self.calc_mode.resultado = self.starter_num()

        while True:
            print(f"\n[Resultado actual: {self.calc_mode.resultado}]")

            op_input = input("Introduce una operación:\n").strip().lower()
            if self.calc_mode._target == op_input:
                print(f"Resultado final: {self.calc_mode.resultado}")
                break

            if op_input in self.modos:
                self.change_modo(op_input)
                continue

            if op_input in ["p", "f", "r", "s", "hex"]:
                self.calc_mode.calc(op_input, 0)
                continue

            num_input = input("Introduce un número:\n").strip().lower()
            if self.calc_mode._target == num_input:
                print(f"Resultado final: {self.calc_mode.resultado}")
                break
            if num_input in self.modos:
                self.change_modo(num_input)
                continue

            try:
                num = float(num_input)
            except ValueError:
                print("No es un número válido.")
                continue

            self.calc_mode.calc(op_input, num)

def main():
    app = InterfazCalculadora()
    app.run()

if __name__ == "__main__":
    main()
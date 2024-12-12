from typing import List
import math

class AsymptoticAnalyzer:
    def __init__(self):
        # Define common growth rates from slowest to fastest
        self.growth_rates = [
            ("1", lambda n: 1),
            ("log(log(n))", lambda n: math.log(math.log(n))),
            ("log(n)", lambda n: math.log(n)),
            ("(log(n))^2", lambda n: math.log(n)**2),
            ("sqrt(log(n))", lambda n: math.sqrt(math.log(n))),
            ("sqrt(n)", lambda n: math.sqrt(n)),
            ("n^(1/3)", lambda n: n**(1/3)),
            ("n", lambda n: n),
            ("n*log(log(n))", lambda n: n * math.log(math.log(n))),
            ("n*log(n)", lambda n: n * math.log(n)),
            ("n*log(n)^2", lambda n: n * math.log(n)**2),
            ("n^(1.5)", lambda n: n**1.5),
            ("n^2", lambda n: n**2),
            ("n^2*log(n)", lambda n: n**2 * math.log(n)),
            ("n^3", lambda n: n**3),
            ("2^(sqrt(n))", lambda n: 2**math.sqrt(n)),
            ("2^n", lambda n: 2**n),
            ("3^n", lambda n: 3**n),
            ("n^n", lambda n: n**n),
            ("n!", lambda n: math.factorial(n) if n <= 20 else float('inf'))
        ]
    
    def parse_expression(self, expression: str) -> callable:
        """Convert string expression to lambda function"""
        expression = expression.lower().replace(' ', '')
        
        expressions = {
            "1": lambda n: 1,
            "loglogn": lambda n: math.log(math.log(n)),
            "logn": lambda n: math.log(n),
            "(logn)^2": lambda n: math.log(n)**2,
            "sqrt(logn)": lambda n: math.sqrt(math.log(n)),
            "sqrtn": lambda n: math.sqrt(n),
            "n^(1/3)": lambda n: n**(1/3),
            "n": lambda n: n,
            "nloglogn": lambda n: n * math.log(math.log(n)),
            "nlogn": lambda n: n * math.log(n),
            "nlogn^2": lambda n: n * math.log(n)**2,
            "n^1.5": lambda n: n**1.5,
            "n^2": lambda n: n**2,
            "n^2logn": lambda n: n**2 * math.log(n),
            "n^3": lambda n: n**3,
            "2^sqrtn": lambda n: 2**math.sqrt(n),
            "2^n": lambda n: 2**n,
            "3^n": lambda n: 3**n,
            "n^n": lambda n: n**n,
            "n!": lambda n: math.factorial(n) if n <= 20 else float('inf')
        }
        
        if expression in expressions:
            return expressions[expression]
        raise ValueError(f"Unsupported expression: {expression}")
    
    def is_little_o(self, f: callable, g: callable, n_values: List[int] = None) -> bool:
        """Check if f(n) is little o of g(n) by testing limit"""
        if n_values is None:
            n_values = [10, 100, 1000, 10000]
        
        ratios = []
        for n in n_values:
            try:
                f_n = f(n)
                g_n = g(n)
                if g_n == 0:
                    continue
                ratio = f_n / g_n
                ratios.append(ratio)
            except (OverflowError, ValueError):
                continue
        
        if not ratios:
            return False
        
        return all(ratios[i] > ratios[i+1] for i in range(len(ratios)-1))
    
    def find_little_o_functions(self, big_o_expr: str) -> List[str]:
        """Find all common functions that are little o of the given Big O function"""
        try:
            g = self.parse_expression(big_o_expr)
            little_o_functions = []
            
            for name, f in self.growth_rates:
                if self.is_little_o(f, g):
                    little_o_functions.append(name)
            
            return little_o_functions
        except ValueError as e:
            return [f"Error: {str(e)}"]

def main():
    analyzer = AsymptoticAnalyzer()
    
    print("\nAvailable expressions:")
    print("Basic: 1, logn, sqrtn, n, n^2, n^3")
    print("Logarithmic variations: loglogn, (logn)^2, sqrt(logn)")
    print("Linear variations: nlogn, nloglogn, nlogn^2")
    print("Polynomial variations: n^(1/3), n^1.5, n^2logn")
    print("Exponential and beyond: 2^sqrtn, 2^n, 3^n, n^n, n!")
    
    big_o = input("\nEnter the Big O expression (e.g., 'n^2'): ")
    
    results = analyzer.find_little_o_functions(big_o)
    
    print(f"\nFunctions that are little o of {big_o}:\n")
    for func in results:
        print(f"- {func}")
    
    print(f"\nKey relationship: For all functions f(n) listed above:")
    print(f"lim(n→∞) f(n)/{big_o} = 0")
    print("This means they grow strictly slower than your input function.\n")
    print("Big O (O) represents an upper bound that can be tight.")
    print("Little o (o) represents a strictly smaller growth rate")

if __name__ == "__main__":
    main()
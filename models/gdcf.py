import numpy as np

class DCF:
    def __init__(self):
        # Default parameters
        self._current_fcf = 0.0  # Current Free Cash Flow
        self._growth_rates = []  # List of growth rates for each projection period
        self._terminal_growth_rate = 0.02 # Perpetual growth rate after projection period
        self._wacc = 0.10 # Weighted Average Cost of Capital (discount rate)
        self._cash_and_equivalents = 0.0 # Cash and equivalents
        self._total_debt = 0.0 # Total debt
        self._shares_outstanding = 1.0 # Number of shares outstanding

    # --- Setter Methods ---
    def set_current_fcf(self, fcf: float):
        if not isinstance(fcf, (int, float)) or fcf < 0:
            raise ValueError("Current FCF must be a non-negative number.")
        self._current_fcf = fcf
        return self # Allow method chaining

    def set_growth_rates(self, rates: list):
        if not isinstance(rates, list) or not all(isinstance(r, (int, float)) for r in rates):
            raise ValueError("Growth rates must be a list of numbers.")
        self._growth_rates = rates
        return self

    def set_terminal_growth_rate(self, rate: float):
        if not isinstance(rate, (int, float)):
            raise ValueError("Terminal growth rate must be a number.")
        self._terminal_growth_rate = rate
        return self

    def set_wacc(self, wacc: float):
        if not isinstance(wacc, (int, float)) or not (0 < wacc < 1):
            raise ValueError("WACC must be a number between 0 and 1 (exclusive).")
        self._wacc = wacc
        return self

    def set_cash_and_equivalents(self, cash: float):
        if not isinstance(cash, (int, float)) or cash < 0:
            raise ValueError("Cash and equivalents must be a non-negative number.")
        self._cash_and_equivalents = cash
        return self

    def set_total_debt(self, debt: float):
        if not isinstance(debt, (int, float)) or debt < 0:
            raise ValueError("Total debt must be a non-negative number.")
        self._total_debt = debt
        return self

    def set_shares_outstanding(self, shares: float):
        if not isinstance(shares, (int, float)) or shares <= 0:
            raise ValueError("Shares outstanding must be a positive number.")
        self._shares_outstanding = shares
        return self

    # --- Getter Methods (Optional, but good practice for access) ---
    def get_current_fcf(self):
        return self._current_fcf

    def get_growth_rates(self):
        return self._growth_rates

    def get_terminal_growth_rate(self):
        return self._terminal_growth_rate

    def get_wacc(self):
        return self._wacc

    def get_cash_and_equivalents(self):
        return self._cash_and_equivalents

    def get_total_debt(self):
        return self._total_debt

    def get_shares_outstanding(self):
        return self._shares_outstanding

    # --- Calculation Method ---
    def calc(self):
        """
        Calculates the intrinsic value per share using the DCF model.
        """
        if self._wacc <= self._terminal_growth_rate:
            raise ValueError("WACC must be greater than the terminal growth rate for a stable terminal value calculation.")
        if not self._growth_rates:
            raise ValueError("Growth rates list cannot be empty. Please set growth rates for projection period.")
        if self._current_fcf <= 0:
            print("Warning: Current FCF is zero or negative. DCF might not be appropriate or projections need careful review.")

        # 1. Project Free Cash Flows (FCF) for the explicit forecast period
        projected_fcfs = []
        last_fcf = self._current_fcf
        for i, growth_rate in enumerate(self._growth_rates):
            next_fcf = last_fcf * (1 + growth_rate)
            projected_fcfs.append(next_fcf)
            last_fcf = next_fcf

        # 2. Discount Projected FCFs to Present Value
        present_value_of_fcfs = 0
        for i, fcf in enumerate(projected_fcfs):
            discount_factor = (1 + self._wacc)**(i + 1)
            present_value_of_fcfs += fcf / discount_factor

        # 3. Calculate Terminal Value (TV)
        # Using the Gordon Growth Model: TV = FCF_n * (1 + g) / (WACC - g)
        # FCF_n is the FCF of the last projected year.
        # FCF_n * (1 + g) is the FCF for the first year beyond the explicit forecast.
        last_projected_fcf = projected_fcfs[-1]
        terminal_value = (last_projected_fcf * (1 + self._terminal_growth_rate)) / \
                         (self._wacc - self._terminal_growth_rate)

        # 4. Discount Terminal Value to Present Value
        # The discount period is the number of years in the explicit forecast period.
        discount_factor_tv = (1 + self._wacc)**len(self._growth_rates)
        present_value_of_terminal_value = terminal_value / discount_factor_tv

        # 5. Calculate Enterprise Value (EV)
        enterprise_value = present_value_of_fcfs + present_value_of_terminal_value

        # 6. Calculate Equity Value
        equity_value = enterprise_value + self._cash_and_equivalents - self._total_debt

        # 7. Calculate Intrinsic Value Per Share
        if self._shares_outstanding <= 0:
            return 0 # Avoid division by zero
        intrinsic_value_per_share = equity_value / self._shares_outstanding

        return {
            "projected_fcfs": projected_fcfs,
            "present_value_of_fcfs": present_value_of_fcfs,
            "terminal_value": terminal_value,
            "present_value_of_terminal_value": present_value_of_terminal_value,
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "intrinsic_value_per_share": intrinsic_value_per_share
        }

# --- Example Usage ---
if __name__ == "__main__":
    try:
        dcf_model = DCF()

        # Set parameters using method chaining
        valuation_results = dcf_model \
            .set_current_fcf(100) \
            .set_growth_rates([0.15, 0.10, 0.08, 0.05, 0.03]) \
            .set_terminal_growth_rate(0.02) \
            .set_wacc(0.09) \
            .set_cash_and_equivalents(50) \
            .set_total_debt(20) \
            .set_shares_outstanding(100) \
            .calc()

        print("--- DCF Valuation Results ---")
        print(f"Projected FCFs (Year 1-5): {[round(f, 2) for f in valuation_results['projected_fcfs']]}")
        print(f"Present Value of FCFs: ${valuation_results['present_value_of_fcfs']:.2f}")
        print(f"Terminal Value (End of Year 5): ${valuation_results['terminal_value']:.2f}")
        print(f"Present Value of Terminal Value: ${valuation_results['present_value_of_terminal_value']:.2f}")
        print(f"Enterprise Value: ${valuation_results['enterprise_value']:.2f}")
        print(f"Equity Value: ${valuation_results['equity_value']:.2f}")
        print(f"Intrinsic Value Per Share: ${valuation_results['intrinsic_value_per_share']:.2f}")

        print("\n--- Another Example (adjusting parameters) ---")
        dcf_model_2 = DCF()
        valuation_results_2 = dcf_model_2 \
            .set_current_fcf(50) \
            .set_growth_rates([0.20, 0.15, 0.12]) \
            .set_terminal_growth_rate(0.025) \
            .set_wacc(0.11) \
            .set_cash_and_equivalents(30) \
            .set_total_debt(10) \
            .set_shares_outstanding(50) \
            .calc()

        print(f"Intrinsic Value Per Share (Example 2): ${valuation_results_2['intrinsic_value_per_share']:.2f}")

    except ValueError as e:
        print(f"Error: {e}")
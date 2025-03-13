import pytest
from decimal import Decimal
from app.calculation import Calculation
from app.calculations import Calculations
from app.plugins.add_command import AddCommand
from app.plugins.subtract_command import SubtractCommand

@pytest.fixture
def reset_calculations():
    """
    Clears calculation history before running each test.
    """
    Calculations.clear_history()

def test_add_calculation(reset_calculations):
    add_command = AddCommand()
    calc = Calculation(Decimal(2), Decimal(3), add_command)
    calc.operate()
    Calculations.add_calculation(calc)

    history = Calculations.get_all_calculations()
    assert len(history) == 1
    assert history.iloc[0]['result'] == Decimal(5)

def test_clear_history(reset_calculations):
    command = AddCommand()
    calc = Calculation(Decimal(10), Decimal(5), command)
    calc.operate()
    Calculations.add_calculation(calc)

    Calculations.clear_history()
    history = Calculations.get_all_calculations()
    assert history.empty

def test_filter_by_operation(reset_calculations):
    add_command = AddCommand()
    subtract_command = SubtractCommand()

    calc_add = Calculation(Decimal(7), Decimal(2), add_command)
    calc_add.operate()
    Calculations.add_calculation(calc_add)

    calc_subtract = Calculation(Decimal(9), Decimal(4), subtract_command)
    calc_subtract.operate()
    Calculations.add_calculation(calc_subtract)

    filtered = Calculations.filter_by_operation("add")
    assert len(filtered) == 1
    assert filtered.iloc[0]['operation'] == "add"

def test_save_and_load_history(reset_calculations, tmp_path):
    add_command = AddCommand()
    calc = Calculation(Decimal(3), Decimal(7), add_command)
    calc.operate()
    Calculations.add_calculation(calc)

    save_file = tmp_path / "calc_history.csv"
    Calculations.save_history(str(save_file))

    Calculations.clear_history()
    assert Calculations.get_all_calculations().empty

    Calculations.load_history(str(save_file))
    loaded = Calculations.get_all_calculations()
    assert len(loaded) == 1
    assert loaded.iloc[0]['result'] == Decimal(10)

def test_delete_history(reset_calculations):
    add_command = AddCommand()
    calc = Calculation(Decimal(1), Decimal(2), add_command)
    calc.operate()
    Calculations.add_calculation(calc)

    Calculations.delete_history(0)
    assert Calculations.get_all_calculations().empty

def test_delete_invalid_index(reset_calculations, capsys):
    add_command = AddCommand()
    calc = Calculation(Decimal(1), Decimal(2), add_command)
    calc.operate()
    Calculations.add_calculation(calc)

    Calculations.delete_history(10)
    captured = capsys.readouterr()
    assert "Invalid index: 10. No record deleted." in captured.out

def test_empty_history_on_start(reset_calculations):
    history = Calculations.get_all_calculations()
    assert history.empty

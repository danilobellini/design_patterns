#!/usr/bin/env py.test
# @author: Danilo J. S. Bellini
import os, envoy, pytest, re, sys
from tempfile import mktemp
from operator import itemgetter


### Fixtures ###

@pytest.yield_fixture
def run_in_dir():
  os.chdir("strategy")
  try:
    yield envoy.run
  finally:
    os.chdir(os.path.pardir)

@pytest.yield_fixture
def gcc(run_in_dir):
  tmp = mktemp()
  try:
    def gcc_call(fname):
      resp = run_in_dir("gcc -o {} {}".format(tmp, fname))
      resp.fname = tmp
      return resp
    yield gcc_call
  finally:
    os.remove(tmp)


### Expected data ###

expected_first = [
  "22 + 3 = {}".format(22 + 3),
  "22 - 3 = {}".format(22 - 3),
  "22 * 3 = {}".format(22 * 3),
]

expected_c = [
  "2 + 3 = {}".format(2 + 3),
  "7 + 5 = {}".format(7 + 5),
  "2 - 3 = {}".format(2 - 3),
  "7 - 5 = {}".format(7 - 5),
  "2 * 3 = {}".format(2 * 3),
  "7 * 5 = {}".format(7 * 5),
]

expected_multiton = [
  "2,  +2 -> {}".format(2 + 2),
  "-1, +2 -> {}".format(-1 + 2),
  "7,  +2 -> {}".format(7 + 2),
  "2,  5- -> {}".format(5 - 2),
  "-1, 5- -> {}".format(5 - -1),
  "7,  5- -> {}".format(5 - 7),
  "2,  -3 -> {}".format(2 - 3),
  "-1, -3 -> {}".format(-1 - 3),
  "7,  -3 -> {}".format(7 - 3),
  "2,  4* -> {}".format(4 * 2),
  "-1, 4* -> {}".format(4 * -1),
  "7,  4* -> {}".format(4 * 7),
  "2,  +2 -> {}".format(2 + 2),
  "-1, +2 -> {}".format(-1 + 2),
  "7,  +2 -> {}".format(7 + 2),
]

expected_missing = [
  "2 + 3 = {}".format(2 + 3),
  "7 + 5 = {}".format(7 + 5),
  "2  + 3 = {}".format(2 + 3),
  "7  + 5 = {}".format(7 + 5),
  "2  -   3 = {}".format(2 - 3),
  "7  -   5 = {}".format(7 - 5),
  "2 ", "* ", " 3 = {}".format(2 * 3),
  "7 ", "* ", " 5 = {}".format(7 * 5),
]


### Tests ###

@pytest.mark.parametrize(("fname", "expected"), [
  ("strategy_0.py", expected_first),
  ("strategy_1.py", expected_first),
  ("strategy_2.py", expected_first),
  ("strategy_3.py", expected_c),
  ("subclasshook.py", ["True", "True"]),
  ("multiton.py", expected_multiton),
])
def test_python_deterministic_implementations(fname, expected, run_in_dir):
  resp = run_in_dir("python3 " + fname)
  assert resp.std_err == ""
  assert resp.status_code == 0
  assert expected == resp.std_out.splitlines()

def test_c_implementation(gcc):
  resp = envoy.run(gcc("strategy.c").fname)
  assert resp.std_err == ""
  assert resp.status_code == 0
  assert expected_c == resp.std_out.splitlines()

def test_strategy_4_which_has_non_deterministic_order(run_in_dir):
  resp = run_in_dir("python3 strategy_4.py")
  assert resp.std_err == ""
  assert resp.status_code == 0
  result = resp.std_out.splitlines()
  to_set_of_pairs = lambda seq: set(zip(seq[::2], seq[1::2]))
  assert to_set_of_pairs(result) == to_set_of_pairs(expected_c)

def test_strategy_sort(run_in_dir):
  resp = run_in_dir("python3 strategy_sort.py")
  assert resp.std_err == ""
  assert resp.status_code == 0

  # Representation for each strategy
  strategies_fmt = {
    "slow": "('slow', 'bad'): <function {} at 0x...>",
    "merge": "('merge',): <function {} at 0x...>",
    "bubble": "('bubble',): <function {} at 0x...>",
  }
  if sys.version_info.minor > 2: # Name in __code__.co_name
    strategies = {k: v.format("sort") for k, v in strategies_fmt.items()}
  else: # Function representation uses __name__
    strategies = {k: v.format(k) for k, v in strategies_fmt.items()}

  # Starting values
  result = iter(resp.std_out.splitlines())
  assert next(result) == "slow"
  assert next(result) == ""
  assert next(result) == "True"
  assert next(result) == ""

  # The strategies shown should match a valid representation
  names_shown = re.sub(r"(?<=0x)[0-9a-f]+", "...", next(result))
  names_order = sorted((names_shown.index(n), n) for n in strategies.keys())
  names = map(itemgetter(1), names_order)
  names_expected = "{%s}" % ", ".join(strategies[name] for name in names)
  assert names_shown == names_expected

  # Tests each strategy call
  list30 = list(range(30))
  for unused in range(3):
    assert next(result) == ""
    numbers_str = next(result)
    numbers = list(map(int, re.findall("\d+", numbers_str)))
    assert sorted(numbers) == list30
    assert numbers_str == str(numbers)
    assert numbers_str != str(list30)
    assert next(result) == str(list30)

  # There should be nothing left behind
  with pytest.raises(StopIteration):
    next(result)

def test_python_missing_with_error(run_in_dir):
  resp = run_in_dir("python3 missing.py")
  err_data = resp.std_err.splitlines()
  assert err_data[0].startswith("Traceback")
  assert err_data[-1] == "KeyError: 'Not Found'"
  assert resp.status_code != 0
  assert expected_missing == resp.std_out.splitlines()

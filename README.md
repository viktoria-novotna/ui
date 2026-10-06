# Inteligentný agent pre zavlažovanie poľa

Simulácia poľa 5×5 zón, na ktorom agent každý deň sezóny (90 dní) rozhoduje, ktoré zóny zaliať.

## Spustenie

Potrebný je Python 3.8+ a (len pre graf) knižnica matplotlib. Na textové GUI sa
používa vstavaný modul `curses` (na Windowse môže vyžadovať `pip install windows-curses`).

```bash
pip install -r requirements.txt

python main.py                  # celý experiment: konfigurácie z konfiguracie.json x 2 agenti x 20 SEEDov
python main.py --behy 5         # rýchlejšie, menej opakovaní
python main.py --demo hard      # jeden beh inteligentného agenta deň po dni (text)
python main.py --gui hard       # to isté ako --demo, ale ako textové GUI v termináli
python main.py --gui hard --seed 7
python main.py --gui hard --agent baseline   # spustí základného agenta (predvolený je smart)
```

V GUI: medzerník/→ = ďalší deň, `a` = automatický beh, `s` = zastaviť, `q` = koniec.
`--agent baseline` alebo `--agent smart` volí, ktorý agent beží (predvolený je `smart`).
Počas behu sa mriežka farbí podľa vlhkosti. Na konci sezóny sa prekreslí podľa
finálneho zdravia zón (`@` = zdravá, `o` = trpela, `x` = takmer uschla, `X` = uschla)
a vypíše počet zón, ktoré prežili a ktoré uschli.

## Testy

```bash
python -m unittest discover tests -v
```

## Výsledky

Výsledky sa ukladajú do priečinka `results/`:

| Súbor | Obsah |
| --- | --- |
| `behy.csv` | výsledky každého jedného behu experimentu vrátane počtu krokov, dňa vyčerpania nádrže a času výpočtu |
| `priebeh.csv` | priebeh každého behu deň po dni (120 behov po 90 dní) |
| `suhrn.csv` | priemer a smerodajná odchýlka pre každú dvojicu (konfigurácia, agent) |
| `graf_skore.png` | stĺpcový graf porovnania agentov (skóre) |
| `log.txt` | záznam každého behu experimentu |
| `priebeh_demo.csv` | priebeh behu spusteného cez `--demo` |
| `gui_vysledky.csv`, `gui_priebeh.csv` | výsledok a priebeh každého behu spusteného cez `--gui` (pridávajú sa) |

## Štruktúra projektu

```
zavlazovanie_projekt/
├── main.py                  # vstupný bod (CLI)
├── requirements.txt
├── README.md                # tento súbor
├── konfiguracie.json        # konfigurácie prostredia: default, easy, medium, hard
├── zavlazovanie/               # zdrojový balík
│   ├── config.py             # dataclass Config + načítanie z JSON
│   ├── interface.py          # Percept, Action, AgentInfo — rozhranie agent <-> svet
│   ├── environment.py        # 1. prostredie (skutočný stav) a generátor počasia
│   ├── sensors.py            # 2. senzory (zašumený vnem)
│   ├── actuators.py          # 4. aktuátory (vykonanie akcií)
│   ├── performance.py        # 5. miera úspešnosti
│   ├── agents/                # 3. agenti
│   │   ├── baseline_agent.py  # základný agent
│   │   └── smart_agent.py     # vlastný inteligentný agent (vrátane jeho pamäte Belief)
│   ├── simulation.py          # spája päť častí do jednej slučky
│   ├── experiments.py         # spúšťanie a vyhodnotenie experimentov, log, CSV, graf
│   └── tui.py                 # textové GUI v termináli
├── tests/                     # unit testy (python -m unittest discover tests)
└── results/                   # generované výstupy (CSV, log, graf)
```

## Pridanie novej konfigurácie prostredia

Do súboru `konfiguracie.json` pridaj nový záznam s poliami, ktoré sa líšia od `"default"`
(napr. `"moja": {"nadrz": 500.0, "pocet_senzorov": 3}`). Objaví sa automaticky
v `python main.py`, `--demo` aj `--gui` (bez úpravy kódu).

## Použité knižnice a zdroje

- Štandardná knižnica Pythonu (`random`, `math`, `dataclasses`, `statistics`, `csv`, `logging`, `argparse`, `os`, `abc`, `curses`).
- `matplotlib` (jediná externá knižnica, používa sa len na grafy, viď `requirements.txt`).
- Rozhodovací algoritmus agentov je našou vlastnou implementáciou, nepoužili sme žiadny hotový agentný framework.
- Russell, S., Norvig, P.: Artificial Intelligence: A Modern Approach.
- Prednášky a zadanie k predmetu Umelá inteligencia.
- Pri návrhu a implementácii sme využili AI asistenta Claude (Anthropic).

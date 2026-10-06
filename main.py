"""
Vstupný bod programu: spúšťa experiment, demo alebo textové GUI. Samotná logika je
v balíku zavlazovanie/, úrovne náročnosti sú v súbore konfiguracie.json.

Použitie:
    python main.py                               # celý experiment (20 behov na úroveň)
    python main.py --behy 5                      # rýchlejšie, menej behov
    python main.py --demo hard                   # jeden beh po dňoch vypísaný ako text
    python main.py --gui hard                    # ten istý beh v textovom GUI
    python main.py --gui hard --seed 7           # iný SEED
    python main.py --gui hard --agent baseline   # základný agent namiesto inteligentného
"""

import argparse

from zavlazovanie.config import nacitaj_config, zoznam_konfiguracii
from zavlazovanie.agents.baseline_agent import BaselineAgent
from zavlazovanie.agents.smart_agent import SmartAgent
from zavlazovanie.experiments import (PRVY_SEED, demo, spusti_experiment, zaznamenaj_gui_beh,
                                    zaznamenaj_gui_priebeh)

AGENTI_CLI = {"baseline": BaselineAgent, "smart": SmartAgent}


if __name__ == "__main__":
    konfiguracie = zoznam_konfiguracii()

    parser = argparse.ArgumentParser(description="Experimenty s agentmi na zavlažovanie poľa")
    parser.add_argument("--behy", type=int, default=None,
                        help="počet behov (SEEDov) na konfiguráciu")
    parser.add_argument("--demo", choices=konfiguracie,
                        help="vypíše jeden beh inteligentného agenta deň po dni")
    parser.add_argument("--gui", choices=konfiguracie,
                        help="spustí ten istý beh ako textové GUI v termináli (curses)")
    parser.add_argument("--agent", choices=list(AGENTI_CLI), default="smart",
                        help="ktorého agenta spustiť s --gui (predvolene 'smart')")
    parser.add_argument("--seed", type=int, default=PRVY_SEED, help="SEED pre --demo/--gui")
    args = parser.parse_args()

    if args.gui:
        from zavlazovanie import tui
        config = nacitaj_config(args.gui).s(seed=args.seed)
        trieda_agenta = AGENTI_CLI[args.agent]
        vysledok = tui.spusti(args.gui, config, trieda_agenta)
        if vysledok is not None:
            v, priebeh = vysledok
            print(f"Agent: {args.agent}")
            print(f"Úroda {v['uroda']:.0f}, voda {v['voda']:.0f} l, dni sucha {v['dni_sucha']}, "
                  f"dni prelievania {v['dni_prelievania']}, dni sparenia {v['dni_sparenia']}, "
                  f"skóre {v['skore']:.0f}")
            cesta = zaznamenaj_gui_beh(args.gui, args.seed, v, args.agent)
            print(f"Surové výsledky behu uložené do: {cesta}")
            cesta_priebehu = zaznamenaj_gui_priebeh(args.gui, args.seed, priebeh, args.agent)
            print(f"Priebeh behu (deň po dni) uložený do: {cesta_priebehu}")
    elif args.demo:
        demo(args.demo, args.seed)
    else:
        from zavlazovanie.experiments import POCET_BEHOV
        spusti_experiment(args.behy if args.behy is not None else POCET_BEHOV)

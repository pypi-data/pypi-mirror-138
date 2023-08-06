import argparse

def compute(dev: int, sprint_size: int, support: int, day_off: int, focus_factor: float):
    return (((dev - support) * sprint_size) - day_off) * focus_factor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--devs", type=int, help="Number of devs")
    parser.add_argument("--sprint-size", type=int, default=15, help="Sprint size in weeks")
    parser.add_argument("--support", type=int, default=2, help="People who make support")
    parser.add_argument("--day-off", type=int, help="Hollydays")
    parser.add_argument("--focus-factor", type=float, default=1, help="Focus factor")
    args = parser.parse_args()
    r = compute(args.devs, args.sprint_size, args.support, args.day_off, args.focus_factor)
    print(r)

if __name__ == '__main__':
    main()

import sys

def main():
    channels = set()
    with open("samples/Hawaii5-0.sco", "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                try:
                    ch = int(parts[2])
                    channels.add(ch)
                except:
                    pass
    print(f"Channels: {sorted(list(channels))}")

if __name__ == "__main__":
    main()

from .demo import run_demo

def main():
    ranking,metrics=run_demo()
    print(ranking.to_string(index=False))
    print("\nBacktest fixture metrics:",metrics)

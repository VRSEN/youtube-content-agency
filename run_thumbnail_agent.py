from dotenv import load_dotenv
from agency_swarm import Agency

from thumbnail_generator_agent import thumbnail_generator_agent


def main() -> None:
    load_dotenv()
    Agency(thumbnail_generator_agent, name="ThumbnailOnly").terminal_demo()


if __name__ == "__main__":
    main()

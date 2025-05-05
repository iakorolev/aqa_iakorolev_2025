from pathlib import Path
from parser import ModelParser
from generators import ConfigGenerator, MetaGenerator

def main():
    input_file = Path("C:/Users/User/Downloads/Стажировка AQA Python 2025. телеком/Стажировка AQA Python 2025/input/test_input.xml")
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)

    # Парсинг модели
    parser = ModelParser(input_file)
    model = parser.parse()
    print(model)

    # Генерация config.xml
    config_generator = ConfigGenerator(model)
    config_generator.generate(output_dir / "config.xml")

    # Генерация meta.json
    meta_generator = MetaGenerator(model)
    meta_generator.generate(output_dir / "meta.json")

    print("Генерация завершена. Файлы сохранены в папке 'out'.")

if __name__ == "__main__":
    main()

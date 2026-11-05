import typing
from data_processor import (
    DataProcessor, NumericProcessor, TextProcessor, LogProcessor
)


class DataStream:
    def __init__(self) -> None:
        self._processors: typing.List[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        if proc not in self._processors:
            self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for elem in stream:
            handled: bool = False
            for processor in self._processors:
                if processor.validate(elem):
                    processor.ingest(elem)
                    handled = True
                    break

            if not handled:
                print(
                    "DataStream error"
                    f" - Can't process element in stream: {elem}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return

        display_name: str = ""
        for proc in self._processors:
            if isinstance(proc, NumericProcessor):
                display_name = "Numeric Processor"
            elif isinstance(proc, TextProcessor):
                display_name = "Text Processor"
            elif isinstance(proc, LogProcessor):
                display_name = "Log Processor"
            else:
                display_name = proc.__class__.__name__

            total: int = proc._counter
            remain: int = len(proc._storage)
            print(
                f"{display_name}: total {total} items processed, "
                f"remaining {remain} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")

    pipeline = DataStream()
    pipeline.print_processors_stats()
    print("\nRegistering Numeric Processor\n")

    num: NumericProcessor = NumericProcessor()
    pipeline.register_processor(num)

    content: typing.List[typing.Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': (
                    'Telnet access! '
                    'Use ssh instead'
                )
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected'
            }
        ],
        42,
        ['Hi', 'five']
    ]
    print(f"Send first batch of data on stream: {content}")
    pipeline.process_stream(content)
    pipeline.print_processors_stats()

    print("\nRegistering other data processors")
    text: TextProcessor = TextProcessor()
    log: LogProcessor = LogProcessor()
    pipeline.register_processor(text)
    pipeline.register_processor(log)
    print("Send the same batch again")
    pipeline.process_stream(content)
    pipeline.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        num.output()
    for _ in range(2):
        text.output()
    for _ in range(1):
        log.output()
    pipeline.print_processors_stats()


if __name__ == "__main__":
    main()

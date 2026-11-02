import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self._storage: typing.List[typing.Tuple[int, str]] = []
        self._counter: int = 0
        self.proc_counter: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> typing.Tuple[int, str] | None:
        if not self._storage:
            return None
        return self._storage.pop(0)


class NumericProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            for item in data:
                if not isinstance(
                    item, (int, float)
                ) or isinstance(item, bool):
                    return False
            return True
        return False

    def ingest(
        self, data: typing.Union[
            int, float, typing.List[typing.Union[int, float]]
        ]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self._storage.append((self._counter, str(item)))
                self._counter += 1
                self.proc_counter += 1
        else:
            self._storage.append((self._counter, str(data)))
            self._counter += 1
            self.proc_counter += 1


class TextProcessor(DataProcessor):
    def validate(self, data: typing.Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, str):
                    return False
            return True
        return False

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self._storage.append((self._counter, item))
                self._counter += 1
                self.proc_counter += 1
        else:
            self._storage.append((self._counter, data))
            self._counter += 1
            self.proc_counter += 1


class LogProcessor(DataProcessor):
    def _is_valid_dict(self, item: typing.Any) -> bool:
        if not isinstance(item, dict):
            return False
        for key, value in item.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
        return True

    def validate(self, data: typing.Any) -> bool:
        if self._is_valid_dict(data):
            return True
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                if not self._is_valid_dict(item):
                    return False
            return True
        return False

    def ingest(self, data: typing.Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def format_log(log: dict[str, str]) -> str:
            level = log.get('log_level', '')
            msg = log.get('log_message', '')
            if level and msg:
                return f"{level}: {msg}"
            return ": ".join(log.values())

        if isinstance(data, list):
            for item in data:
                self._storage.append((self._counter, format_log(item)))
                self._counter += 1
                self.proc_counter += 1
        else:
            self._storage.append((self._counter, format_log(data)))
            self._counter += 1
            self.proc_counter += 1


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
                print(f"DataStream error - Can't process element in stream: {elem}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return

        for proc in self._processors:
            name = proc.__class__.__name__.replace("Processor", "Processor")
            if name == "NumericProcessor":
                display_name: str = "Numeric Processor"
            elif name == "TextProcessor":
                display_name = "Text Processor"
            elif name == "LogProcessor":
                display_name = "Log Processor"
            else:
                display_name = name    

            total: int = proc.proc_counter
            remain: int = len(proc._storage)
            print(f"{display_name}: total {total} items processed, remaining {remain} on processor")


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
            {'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, 
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
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

    print("\nConsume some elements from the data processors: Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num.output()
    for _ in range(2):
        text.output()
    for _ in range(1):
        log.output()
    pipeline.print_processors_stats()


if __name__ == "__main__":
    main()

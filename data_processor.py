import abc
import typing


class DataProcessor(abc.ABC):
    def __init__(self) -> None:
        self._storage: typing.List[typing.Tuple[int, str]] = []
        self._counter: int = 0

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
        else:
            self._storage.append((self._counter, str(data)))
            self._counter += 1


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
        else:
            self._storage.append((self._counter, data))
            self._counter += 1


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
        else:
            self._storage.append((self._counter, format_log(data)))
            self._counter += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("Testing Numeric Processor...")
    num = NumericProcessor()
    print(f" Trying to validate input '42': {num.validate(42)}")
    print(f" Trying to validate input 'Hello': {num.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo") # type: ignore
    except ValueError as err:
        print(f" Got exception: {err}")

    print("Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num.output()
        print(f"Numeric value {rank}: {val}")
    print(f"In storage: {num._storage}")

    print("\nTesting Text Processor ...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(['Hello', 'Nexus', 'World'])
    print("Extracting 1 value...")
    for _ in range(1):
        rank, val = text.output()
        print(f"Text value {rank}: {val}")
    print(f"In storage: {num._storage}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    log_data: typing.Any[str, str] = [
        {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
        {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
    ]
    print(f"Processing data: {log_data}")
    log.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log.output()
        print(f"Log entry {rank}: {val}")
    print(f"In storage: {log._storage}")


if __name__ == "__main__":
    main()

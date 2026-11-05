import abc
import typing
from data_processor import DataProcessor, NumericProcessor, TextProcessor, LogProcessor


class ExportPlugin(typing.Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass

class CSVExportPlugin:
    def process_output(self, data: typing.List[typing.Tuple[int, str]]) -> None:
        if not data:
            return
        for item_id, val in data:
            val = val.strip()
            if "," in val or '"' in val:
                val = '"' + val.replace('"', '""') + '"'
            print("CSV Output:")
            print(val)


class JSONExportPlugin:
    def process_output(self, data: typing.List[typing.Tuple[int, str]]) -> None:
        print("JSON Output:")
        if not data:
            print("[]")
            return

        lines = []
        for item_id, val in data:
            safe_val = val.replace('"', '\\"')
            lines.append(f'  {{\n    "id": {item_id},\n    "value": "{safe_val}"\n  }}')
        
        json_output = "[\n" + ",\n".join(lines) + "\n]"
        print(json_output)


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        extracted_data: list[tuple[int, str]] = []

        for processor in self._processors:
            for _ in range(nb):
                if processor._storage:
                    item = processor.output()
                    extracted_data.append(item)
                else:
                    break
        plugin.process_output(extracted_data)

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
    print("\nInitialize Data Stream...\n")
    pipeline = DataStream()
    
    pipeline.print_processors_stats()
    print("\nRegistering Numeric Processor\n")
    
    num_p = NumericProcessor()
    text_p = TextProcessor()
    log_p = LogProcessor()

    pipeline.register_processor(num_p)
    pipeline.register_processor(text_p)
    pipeline.register_processor(log_p)

    content: typing.List[typing.Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'},
            {'log_level': 'INFO', 'log_message': 'User wil isconnected'}
        ], 
        42,
        ['Hi', 'five']
    ]

    print(f"Send first batch of data on stream: {content}\n")
    pipeline.process_stream(content)
    pipeline.print_processors_stats()
    print("\nSend 3 processed data from each processor to a CSV plugin:")

    csv = CSVExportPlugin()
    json = JSONExportPlugin()

    pipeline.output_pipeline(3, csv)
    pipeline.print_processors_stats()


if __name__ == "__main__":
    main()
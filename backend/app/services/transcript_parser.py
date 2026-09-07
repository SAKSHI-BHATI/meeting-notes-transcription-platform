from abc import ABC, abstractmethod
import json, re
from app.schemas.meeting import SegmentCreate


class TranscriptParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> list[SegmentCreate]: ...


class TxtParser(TranscriptParser):
    def parse(self, content: str) -> list[SegmentCreate]:
        segments = []
        for index, line in enumerate(line.strip() for line in content.splitlines() if line.strip()):
            match = re.match(r"(?:\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*)?([^:]{1,80}):\s*(.+)", line)
            speaker, text = (match.group(2), match.group(3)) if match else ("Unknown", line)
            seconds = self._seconds(match.group(1)) if match and match.group(1) else index * 20
            segments.append(SegmentCreate(speaker_name=speaker.strip(), start_time_ms=seconds * 1000, end_time_ms=(seconds + 18) * 1000, content=text.strip()))
        return segments
    @staticmethod
    def _seconds(value: str) -> int:
        parts = [int(x) for x in value.split(":")]
        return parts[-1] + parts[-2] * 60 + (parts[-3] * 3600 if len(parts) == 3 else 0)


class VttParser(TxtParser):
    def parse(self, content: str) -> list[SegmentCreate]:
        blocks = re.split(r"\n\s*\n", content.replace("\r", "")); result = []
        for block in blocks:
            lines = [line for line in block.splitlines() if line and line != "WEBVTT"]
            timing = next((line for line in lines if "-->" in line), None)
            if not timing: continue
            start = self._seconds(timing.split("-->")[0].strip().split(".")[0]); text = " ".join(line for line in lines if line != timing)
            result.extend(TxtParser().parse(f"[{start // 60:02d}:{start % 60:02d}] {text}"))
        return result


class JsonParser(TranscriptParser):
    def parse(self, content: str) -> list[SegmentCreate]:
        data = json.loads(content)
        items = data.get("segments", []) if isinstance(data, dict) else data if isinstance(data, list) else []
        return [SegmentCreate(speaker_name=str(item.get("speaker", "Unknown")), start_time_ms=int(item.get("start_time_ms", 0)), end_time_ms=int(item.get("end_time_ms", item.get("start_time_ms", 0) + 10000)), content=str(item.get("content", item.get("text", "")))) for item in items]


def parser_for(filename: str) -> TranscriptParser:
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else "txt"
    return {"vtt": VttParser(), "json": JsonParser(), "txt": TxtParser()}.get(suffix, TxtParser())

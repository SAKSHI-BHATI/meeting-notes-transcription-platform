from app.services.transcript_parser import JsonParser, TxtParser, VttParser

def test_txt_parser_normalizes_timestamps_and_speakers():
    items = TxtParser().parse("[01:05] Maya: We should ship Thursday.")
    assert items[0].speaker_name == "Maya"
    assert items[0].start_time_ms == 65_000

def test_vtt_parser_reads_cues():
    items = VttParser().parse("WEBVTT\n\n00:00:03.000 --> 00:00:08.000\nNoah: Hello")
    assert len(items) == 1
    assert items[0].start_time_ms == 3_000


def test_json_parser_accepts_segment_array():
    items = JsonParser().parse('[{"speaker":"Maya","start_time_ms":2000,"end_time_ms":4000,"content":"Ready"}]')
    assert items[0].speaker_name == "Maya"
    assert items[0].start_time_ms == 2_000

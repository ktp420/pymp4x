import pytest

from uuid import UUID

from pymp4.parser import *
from pymp4.util import BoxUtil

data=[
    ('dinf', b'\x00\x00\x00$dinf\x00\x00\x00\x1cdref\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x0curl \x00\x00\x00\x01',
        Container(offset=0, type=b'dinf', children=ListContainer([
            Container(offset=8, type=b'dref', version=0, flags=0, data_entries=ListContainer([
                Container(type=b'url ', version=0, flags=Container(self_contained=True), location=None)
            ]),
            end=36),
        ]),
        end=36)
    ),
    ('stsd mp4a', b'\x00\x00\x00gstsd\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00Wmp4a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x10\x00\x00\x00\x00V"\x00\x00\x00\x00\x003esds\x00\x00\x00\x00\x03\x80\x80\x80"\x00\x00\x00\x04\x80\x80\x80\x14@\x15\x00\x18\x00\x00\x00\x00\x00\x00\x00\xfa\x00\x05\x80\x80\x80\x02\x13\x90\x06\x80\x80\x80\x01\x02',
        Container(offset=0, type=b'stsd', version=0, flags=0, entries=ListContainer([
            Container(format=b'mp4a', data_reference_index=1, version=0, revision=0, vendor=0, channels=2, bits_per_sample=16, compression_id=0, packet_size=0, sampling_rate=22050, children=ListContainer([ 
                Container(offset=52, type=b'esds', data=b'\x00\x00\x00\x00\x03\x80\x80\x80"\x00\x00\x00\x04\x80\x80\x80\x14@\x15\x00\x18\x00\x00\x00\x00\x00\x00\x00\xfa\x00\x05\x80\x80\x80\x02\x13\x90\x06\x80\x80\x80\x01\x02', end=103),
            ])),
        ]),
        end=103)
    ),
    ('stsd avc1', b"\x00\x00\x00\x92stsd\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x82avc1\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x80\x01h\x00H\x00\x00\x00H\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\xff\xff\x00\x00\x00,avcC\x01B\xe0\x1e\xff\x01\x00\x15'B\xe0\x1e\xa9\x18\x14\x05\xff.\x00\xd4\x18\x04\x1a\xdb\n\xd7\xbd\xf0\x10\x01\x00\x04(\xde\t\xc8",
        Container(offset=0, type=b'stsd', version=0, flags=0, entries=ListContainer([
            Container(format=b'avc1', data_reference_index=1, version=0, revision=0, vendor=u'', temporal_quality=0, spatial_quality=0, width=640, height=360, horizontal_resolution=72, vertical_resolution=72, data_size=0, frame_count=1, compressor_name=u'', depth=24, color_table_id=-1,
                avc_data=Container(type=b'avcC',
                    version=1, profile=66, compatibility=224, level=30, flags=Container(nal_unit_length_field=3),
                    sps=ListContainer([unhexlify('2742e01ea9181405ff2e00d418041adb0ad7bdf010')]),
                    pps=ListContainer([unhexlify('28de09c8')])
                ),
            sample_info=ListContainer()),
        ]),
        end=146)
    ),
    ('stsd rtp', b'\x00\x00\x004stsd\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00$rtp \x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x01\x00\x00\x05\xaa\x00\x00\x00\x0ctims\x00\x01_\x90',
        Container(offset=0, type=b'stsd', version=0, flags=0, entries=ListContainer([ 
            Container(format=b'rtp ', data_reference_index=1, data=b'\x00\x01\x00\x01\x00\x00\x05\xaa\x00\x00\x00\x0ctims\x00\x01_\x90')
            ]),
        end=52)
    ),
    ('stts empty', b'\x00\x00\x00\x10stts\x00\x00\x00\x00\x00\x00\x00\x00',
        Container(offset=0, type=b'stts', version=0, flags=0, entries=ListContainer(), end=16)
    ),
    ('stts 1 entry', b'\x00\x00\x00\x18stts\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x05\x0f\x00\x00\x04\x00',
        Container(offset=0, type=b'stts', version=0, flags=0, entries=ListContainer([ 
            Container(sample_count=1295, sample_delta=1024)
        ]),
        end=24)
    ),
    ('stts multiple entries', b'\x00\x00\x00 stts\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x05\x9f\x00\x00\x00\x19\x00\x00\x00\x01\x00\x00\x00R',
        Container(offset=0, type=b'stts', version=0, flags=0, entries=ListContainer([
            Container(sample_count=1439, sample_delta=25),
            Container(sample_count=1, sample_delta=82)
        ]),
        end=32)
    ),
    ('stsd enca', b"\x00\x00\x00\xf6stsd\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x9benca\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x10\x00\x00\x00\x00\xacD\x00\x00\x00\x00\x00'esds\x00\x00\x00\x00\x03\x19\x00\x01\x00\x04\x11@\x15\x00\x00\x00\x00\x01\xf4\t\x00\x01\xf4\t\x05\x02\x12\x10\x06\x01\x02\x00\x00\x00Psinf\x00\x00\x00\x0cfrmamp4a\x00\x00\x00\x14schm\x00\x00\x00\x00cenc\x00\x01\x00\x00\x00\x00\x00(schi\x00\x00\x00 tenc\x00\x00\x00\x00\x00\x00\x01\x08:t\xf0\x97{j\x16`_6\xa3=\x10\xf4j\xff\x00\x00\x00Kmp4a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x10\x00\x00\x00\x00\xacD\x00\x00\x00\x00\x00'esds\x00\x00\x00\x00\x03\x19\x00\x01\x00\x04\x11@\x15\x00\x00\x00\x00\x01\xf4\t\x00\x01\xf4\t\x05\x02\x12\x10\x06\x01\x02",
        Container(offset=0, type=b'stsd', version=0 , flags=0, entries=ListContainer([
            Container(format=b'enca', data_reference_index=1, version=0, revision=0, vendor=0, channels=2, bits_per_sample=16, compression_id=0, packet_size=0, sampling_rate=44100, children=ListContainer([
                Container(offset=52, type=b'esds' , data=b'\x00\x00\x00\x00\x03\x19\x00\x01\x00\x04\x11@\x15\x00\x00\x00\x00\x01\xf4\t\x00\x01\xf4\t\x05\x02\x12\x10\x06\x01\x02',
                    end=91),
                Container(offset=91, type=b'sinf', children=ListContainer([
                        Container(offset=99, type=b'frma', original_format=b'mp4a',
                            end=111),
                        Container(offset=111, type=b'schm', version=0, flags=0, scheme_type=b'cenc', scheme_version=65536, schema_uri=None,
                            end=131),
                        Container(offset=131, type=b'schi', children=ListContainer([
                            Container(offset=139, type=b'tenc', version=0, flags=0, default_byte_blocks=0, is_encrypted=1, iv_size=8, key_ID=UUID('3a74f097-7b6a-1660-5f36-a33d10f46aff'), constant_iv=None,
                                    end=171),
                            ]),
                            end=171),
                        ]),
                end=171),
                ])),
            Container(format=b'mp4a', data_reference_index=1, version=0, revision=0, vendor=0, channels=2, bits_per_sample=16, compression_id=0, packet_size=0, sampling_rate=44100,
                children=ListContainer([
                    Container(offset=207, type=b'esds', data=b'\x00\x00\x00\x00\x03\x19\x00\x01\x00\x04\x11@\x15\x00\x00\x00\x00\x01\xf4\t\x00\x01\xf4\t\x05\x02\x12\x10\x06\x01\x02',
                        end=246),
                ])
            ),
            ]),
        end=246)
    ),
    ('senc', b'\x00\x00\x00 senc\x00\x00\x00\x00\x00\x00\x00\x02\xeaY[\x86\xb1\x96\x12\x05\xeaY[\x86\xb1\x96\x12\x06',
        Container(offset=0, type=b'senc', version=0, flags=Container(has_subsample_encryption_info=False),
            sample_encryption_info=ListContainer([
                Container(iv=b'\xeaY[\x86\xb1\x96\x12\x05', subsample_encryption_info=None),
                Container(iv=b'\xeaY[\x86\xb1\x96\x12\x06', subsample_encryption_info=None),
            ]),
        end=32)
    ),
    ('traf with assert help', b'\x00\x00\x00ltraf\x00\x00\x00\x1ctfhd\x00\x02\x00*\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x10tfdt\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1ctrun\x00\x00\x02\x01\x00\x00\x00\x02\x00\x00\x07H\x00\x00\x01s\x00\x00\x01t\x00\x00\x00\x1csbgp\x00\x00\x00\x00roll\x00\x00\x00\x01\x00\x00\x01\xb1\x00\x00\x00\x01',
        Container(offset=0, type=b'traf', children=ListContainer([
            Container(offset=8, type=b'tfhd', version=0,
                flags=Container(
                    default_base_is_moof=True,
                    duration_is_empty=False,
                    default_sample_flags_present=True,
                    default_sample_size_present=False,
                    default_sample_duration_present=True,
                    sample_description_index_present=True,
                    base_data_offset_present=False
                ),
                track_ID=1,
                base_data_offset=None,
                sample_description_index=2,
                default_sample_duration=1024,
                default_sample_size=None,
                default_sample_flags=None,
                end=36),
            Container(offset=36, type=b'tfdt', version=0, flags=0, baseMediaDecodeTime=0,
                end=52),
            Container(offset=52, type=b'trun', version=0,
                flags=Container(
                    sample_composition_time_offsets_present=False,
                    sample_flags_present=False,
                    sample_size_present=True,
                    sample_duration_present=False,
                    first_sample_flags_present=False,
                    data_offset_present=True
                ),
                sample_count=2,
                data_offset=1864,
                first_sample_flags=None,
                sample_info=ListContainer([
                    Container(sample_duration=None, sample_size=371, sample_flags=None, sample_composition_time_offsets=None),
                    Container(sample_duration=None, sample_size=372, sample_flags=None, sample_composition_time_offsets=None),
                ]),
                end=80),
            Container(offset=80, type=b'sbgp', data=b'\x00\x00\x00\x00roll\x00\x00\x00\x01\x00\x00\x01\xb1\x00\x00\x00\x01',
                end=108),
            ]),
        end=108)
    ),
    ("pasp", b'\x00\x00\x00\x10\x70\x61\x73\x70\x00\x00\x01\x94\x00\x00\x01\x95',
        Container(offset=0, type=b'pasp', hSpacing=404, vSpacing=405, end=16)
    ),
    ("edts", b'\x00\x00\x00\x24\x65\x64\x74\x73\x00\x00\x00\x1c\x65\x6c\x73\x74\x00\x00\x00\x00\x00\x00\x00\x01\x00\x4f\x1b\x6b\x00\x00\x00\x00\x00\x01\x00\x00',
        Container(offset=0, type=b'edts', children=ListContainer([
            Container(offset=8, type=b'elst', version=0, flags=0, entries=ListContainer([
                Container(track_duration=5184363, media_time=0, media_rate_integer=1, media_rate_fraction=0)
                ]),
                end=36)
            ]),
            end=36
        )
    ),
]


@pytest.mark.parametrize("box_type, to_parse, box", data)
def test_parsing_box(box_type, to_parse, box):
    parsed_box = Box.parse(to_parse)
    if box_type == 'traf with assert help':
        # Reomve the default_sample_flags since can't compare it
        tfhd = next(BoxUtil.find(parsed_box, b'tfhd'), None)
        if tfhd:
            tfhd.default_sample_flags=None
    assert parsed_box == box

@pytest.mark.parametrize("box_type, to_parse, box", data)
def test_building_box(box_type, to_parse, box):
    builded = Box.build(box)
    assert builded == to_parse

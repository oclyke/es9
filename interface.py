import mido
from enum import Enum

import logging
logger = logging.getLogger(__name__)

import proto.es9_pb2 as es9_py_pb2

EXPERT_SLEEPERS_MANUFACTURER_ID = bytes((0x00, 0x21, 0x27))
ES9_SYSEX_HEADER = bytes(EXPERT_SLEEPERS_MANUFACTURER_ID) + bytes((0x19,))

class MessageType(Enum):
    # Messages received by the ES-9 from the host
    APPLY_CONFIGURATION_DUMP = 0x09
    REQUEST_VERSION_STRING = 0x22
    REQUEST_CONFIGURATION_DUMP = 0x23
    REQUEST_SAVE = 0x24
    REQUEST_RESTORE = 0x25
    REQUEST_RESET = 0x26
    REQUEST_MIX = 0x2A
    REQUEST_USAGE = 0x2B
    REQUEST_SAMPLE_RATE = 0x2C
    SET_HPF = 0x31 # set high-pass filters
    SET_OPTIONS = 0x32
    SET_LINKS = 0x33
    SET_VIRTUAL_MIX = 0x34
    SET_MIDI_CHANNELS = 0x35
    SET_DC_OFFSET = 0x36
    SET_FILTER = 0x39
    SET_SMOOTHING = 0x3A
    SET_INPUTS = 0x40 # base, OR DSP block number 0-3
    SET_OUTPUTS = 0x50 # base, OR DSP block number 0-3
    SET_MIX = 0x60 # base, OR mix ID 0-15

    # Messages sent by the ES-9 to the host
    REPORT_CONFIGURATION_DUMP = 0x08
    REPORT_MIX = 0x11
    REPORT_USAGE = 0x12
    REPORT_SAMPLE_RATE = 0x14
    REPORT_MESSAGE = 0x32 # general message, version string and operation success status


MAP_ES9_INPUT_ROUTE_ID_BY_CHANNEL = {
    # Input channels
    es9_py_pb2.Channel.CHANNEL_INPUT_1: 0x78,
    es9_py_pb2.Channel.CHANNEL_INPUT_2: 0x79,
    es9_py_pb2.Channel.CHANNEL_INPUT_3: 0x76,
    es9_py_pb2.Channel.CHANNEL_INPUT_4: 0x75,
    es9_py_pb2.Channel.CHANNEL_INPUT_5: 0x74,
    es9_py_pb2.Channel.CHANNEL_INPUT_6: 0x7B,
    es9_py_pb2.Channel.CHANNEL_INPUT_7: 0x7A,
    es9_py_pb2.Channel.CHANNEL_INPUT_8: 0x77,
    es9_py_pb2.Channel.CHANNEL_INPUT_9: 0x73,
    es9_py_pb2.Channel.CHANNEL_INPUT_10: 0x72,
    es9_py_pb2.Channel.CHANNEL_INPUT_11: 0x7D,
    es9_py_pb2.Channel.CHANNEL_INPUT_12: 0x7C,
    es9_py_pb2.Channel.CHANNEL_INPUT_13: 0x7E,
    es9_py_pb2.Channel.CHANNEL_INPUT_14: 0x7F,

    # Internal busses
    es9_py_pb2.Channel.CHANNEL_BUS_1: 0x60,
    es9_py_pb2.Channel.CHANNEL_BUS_2: 0x61,
    es9_py_pb2.Channel.CHANNEL_BUS_3: 0x62,
    es9_py_pb2.Channel.CHANNEL_BUS_4: 0x63,
    es9_py_pb2.Channel.CHANNEL_BUS_5: 0x64,
    es9_py_pb2.Channel.CHANNEL_BUS_6: 0x65,
    es9_py_pb2.Channel.CHANNEL_BUS_7: 0x66,
    es9_py_pb2.Channel.CHANNEL_BUS_8: 0x67,
    es9_py_pb2.Channel.CHANNEL_BUS_9: 0x68,
    es9_py_pb2.Channel.CHANNEL_BUS_10: 0x69,
    es9_py_pb2.Channel.CHANNEL_BUS_11: 0x6A,
    es9_py_pb2.Channel.CHANNEL_BUS_12: 0x6B,
    es9_py_pb2.Channel.CHANNEL_BUS_13: 0x6C,
    es9_py_pb2.Channel.CHANNEL_BUS_14: 0x6D,
    es9_py_pb2.Channel.CHANNEL_BUS_15: 0x6E,
    es9_py_pb2.Channel.CHANNEL_BUS_16: 0x6F,

    # USB channels
    es9_py_pb2.Channel.CHANNEL_USB_1: 0x00,
    es9_py_pb2.Channel.CHANNEL_USB_2: 0x01,
    es9_py_pb2.Channel.CHANNEL_USB_3: 0x02,
    es9_py_pb2.Channel.CHANNEL_USB_4: 0x03,
    es9_py_pb2.Channel.CHANNEL_USB_5: 0x04,
    es9_py_pb2.Channel.CHANNEL_USB_6: 0x05,
    es9_py_pb2.Channel.CHANNEL_USB_7: 0x06,
    es9_py_pb2.Channel.CHANNEL_USB_8: 0x07,
    es9_py_pb2.Channel.CHANNEL_USB_9: 0x10,
    es9_py_pb2.Channel.CHANNEL_USB_10: 0x11,
    es9_py_pb2.Channel.CHANNEL_USB_11: 0x12,
    es9_py_pb2.Channel.CHANNEL_USB_12: 0x13,
    es9_py_pb2.Channel.CHANNEL_USB_13: 0x14,
    es9_py_pb2.Channel.CHANNEL_USB_14: 0x15,
    es9_py_pb2.Channel.CHANNEL_USB_15: 0x16,
    es9_py_pb2.Channel.CHANNEL_USB_16: 0x17,

    # Mix outputs
    # (applies the same between either Mixer 1 or Mixer 2)
    es9_py_pb2.Channel.CHANNEL_MIX_1: 0x20,
    es9_py_pb2.Channel.CHANNEL_MIX_2: 0x21,
    es9_py_pb2.Channel.CHANNEL_MIX_3: 0x22,
    es9_py_pb2.Channel.CHANNEL_MIX_4: 0x23,
    es9_py_pb2.Channel.CHANNEL_MIX_5: 0x24,
    es9_py_pb2.Channel.CHANNEL_MIX_6: 0x25,
    es9_py_pb2.Channel.CHANNEL_MIX_7: 0x26,
    es9_py_pb2.Channel.CHANNEL_MIX_8: 0x27,
    es9_py_pb2.Channel.CHANNEL_MIX_11: 0x32,
    es9_py_pb2.Channel.CHANNEL_MIX_12: 0x33,
    es9_py_pb2.Channel.CHANNEL_MIX_13: 0x34,
    es9_py_pb2.Channel.CHANNEL_MIX_14: 0x35,
    es9_py_pb2.Channel.CHANNEL_MIX_15: 0x36,
    es9_py_pb2.Channel.CHANNEL_MIX_16: 0x37,

    # SPDIF Input
    es9_py_pb2.Channel.CHANNEL_SPDIF_L: 0x30,
    es9_py_pb2.Channel.CHANNEL_SPDIF_R: 0x31,
}
MAP_ES9_CHANNEL_BY_INPUT_ROUTE_ID = {v: k for k, v in MAP_ES9_INPUT_ROUTE_ID_BY_CHANNEL.items()}
assert len(MAP_ES9_CHANNEL_BY_INPUT_ROUTE_ID) == len(MAP_ES9_INPUT_ROUTE_ID_BY_CHANNEL), "Input route ID mapping is not one-to-one"


MAP_ES9_OUTPUT_ROUTE_ID_BY_CHANNEL = {
    es9_py_pb2.Channel.CHANNEL_MAIN_OUT_L: 0x06,
    es9_py_pb2.Channel.CHANNEL_MAIN_OUT_R: 0x07,
    es9_py_pb2.Channel.CHANNEL_PHONES_L: 0x0C,
    es9_py_pb2.Channel.CHANNEL_PHONES_R: 0x0D,
    es9_py_pb2.Channel.CHANNEL_ES5_L: 0x0E,
    es9_py_pb2.Channel.CHANNEL_ES5_R: 0x0F,

    es9_py_pb2.Channel.CHANNEL_OUTPUT_1: 0x08,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_2: 0x09,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_3: 0x04,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_4: 0x05,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_5: 0x02,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_6: 0x03,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_7: 0x0B,
    es9_py_pb2.Channel.CHANNEL_OUTPUT_8: 0x0A,

    es9_py_pb2.Channel.CHANNEL_BUS_1: 0x10,
    es9_py_pb2.Channel.CHANNEL_BUS_2: 0x11,
    es9_py_pb2.Channel.CHANNEL_BUS_3: 0x12,
    es9_py_pb2.Channel.CHANNEL_BUS_4: 0x13,
    es9_py_pb2.Channel.CHANNEL_BUS_5: 0x14,
    es9_py_pb2.Channel.CHANNEL_BUS_6: 0x15,
    es9_py_pb2.Channel.CHANNEL_BUS_7: 0x16,
    es9_py_pb2.Channel.CHANNEL_BUS_8: 0x17,
    es9_py_pb2.Channel.CHANNEL_BUS_9: 0x18,
    es9_py_pb2.Channel.CHANNEL_BUS_10: 0x19,
    es9_py_pb2.Channel.CHANNEL_BUS_11: 0x1A,
    es9_py_pb2.Channel.CHANNEL_BUS_12: 0x1B,
    es9_py_pb2.Channel.CHANNEL_BUS_13: 0x1C,
    es9_py_pb2.Channel.CHANNEL_BUS_14: 0x1D,
    es9_py_pb2.Channel.CHANNEL_BUS_15: 0x1E,
    es9_py_pb2.Channel.CHANNEL_BUS_16: 0x1F,
}
MAP_ES9_CHANNEL_BY_OUTPUT_ROUTE_ID = {v: k for k, v in MAP_ES9_OUTPUT_ROUTE_ID_BY_CHANNEL.items()}
assert len(MAP_ES9_CHANNEL_BY_OUTPUT_ROUTE_ID) == len(MAP_ES9_OUTPUT_ROUTE_ID_BY_CHANNEL), "Output route ID mapping is not one-to-one"

def es9_filter_enabled_from_storage_value(value: int) -> bool:
    return bool(value & 0x01)

def es9_filter_type_from_storage_value(value: int) -> es9_py_pb2.FilterType:
    match value >> 1:
        case 0:
            return es9_py_pb2.FilterType.LOW_PASS_1ST_ORDER
        case 1:
            return es9_py_pb2.FilterType.HIGH_PASS_1ST_ORDER
        case 2:
            return es9_py_pb2.FilterType.LOW_PASS_2ND_ORDER
        case 3:
            return es9_py_pb2.FilterType.HIGH_PASS_2ND_ORDER
        case 4:
            return es9_py_pb2.FilterType.LOW_SHELF
        case 5:
            return es9_py_pb2.FilterType.HIGH_SHELF
        case 6:
            return es9_py_pb2.FilterType.PEAK
        case 7:
            return es9_py_pb2.FilterType.INVERT_PHASE
        case _:
            raise ValueError(f"Invalid filter type storage value: {value}")

def es9_equalizer_filter_frequency_to_float(v: int) -> float:
    import math
    min_val = 10.0
    mult = math.log(22000.0 / min_val) / 32767.0
    return min_val * math.exp(mult * v)

def es9_equalizer_filter_q_to_float(v: int) -> float:
    import math
    min_val = 0.1
    mult = math.log(18.0 / min_val) / 32767.0
    return min_val * math.exp(mult * v)

def es9_try_recover_channel_from_output_route_id(route_id: int) -> es9_py_pb2.Channel:
    try:
        return MAP_ES9_CHANNEL_BY_OUTPUT_ROUTE_ID[route_id]
    except KeyError:
        logger.warning(f"Unexpected ES-9 output route ID: {route_id:02X}")
        logger.error(f"Failed to recover ES-9 channel from output route ID: {route_id:02X}")
        return es9_py_pb2.Channel.CHANNEL_UNSPECIFIED

def es9_try_recover_channel_from_input_route_id(route_id: int) -> es9_py_pb2.Channel:
    try:
        return MAP_ES9_CHANNEL_BY_INPUT_ROUTE_ID[route_id]
    except KeyError:
        logger.warning(f"Unexpected ES-9 input route ID: {route_id:02X}")
        logger.error(f"Failed to recover ES-9 channel from input route ID: {route_id:02X}")
        return es9_py_pb2.Channel.CHANNEL_UNSPECIFIED

def es9_channel_is_input(channel: es9_py_pb2.Channel) -> bool:
    return channel in {
        es9_py_pb2.Channel.CHANNEL_INPUT_1, es9_py_pb2.Channel.CHANNEL_INPUT_2, es9_py_pb2.Channel.CHANNEL_INPUT_3, es9_py_pb2.Channel.CHANNEL_INPUT_4,
        es9_py_pb2.Channel.CHANNEL_INPUT_5, es9_py_pb2.Channel.CHANNEL_INPUT_6, es9_py_pb2.Channel.CHANNEL_INPUT_7, es9_py_pb2.Channel.CHANNEL_INPUT_8,
        es9_py_pb2.Channel.CHANNEL_INPUT_9, es9_py_pb2.Channel.CHANNEL_INPUT_10, es9_py_pb2.Channel.CHANNEL_INPUT_11, es9_py_pb2.Channel.CHANNEL_INPUT_12,
        es9_py_pb2.Channel.CHANNEL_INPUT_13, es9_py_pb2.Channel.CHANNEL_INPUT_14,
    }

def es9_channel_is_output(channel: es9_py_pb2.Channel) -> bool:
    return channel in {
        es9_py_pb2.Channel.CHANNEL_OUTPUT_1, es9_py_pb2.Channel.CHANNEL_OUTPUT_2, es9_py_pb2.Channel.CHANNEL_OUTPUT_3, es9_py_pb2.Channel.CHANNEL_OUTPUT_4,
        es9_py_pb2.Channel.CHANNEL_OUTPUT_5, es9_py_pb2.Channel.CHANNEL_OUTPUT_6, es9_py_pb2.Channel.CHANNEL_OUTPUT_7, es9_py_pb2.Channel.CHANNEL_OUTPUT_8,
    }

def es9_channel_to_input_route_id(channel: es9_py_pb2.Channel) -> int:
    assert channel in MAP_ES9_INPUT_ROUTE_ID_BY_CHANNEL, "Channel must be valid to be routed to an input"
    return MAP_ES9_INPUT_ROUTE_ID_BY_CHANNEL[channel]

def es9_channel_to_output_route_id(channel: es9_py_pb2.Channel) -> int:
    assert channel in MAP_ES9_OUTPUT_ROUTE_ID_BY_CHANNEL, "Channel must be valid to be routed to an output"
    return MAP_ES9_OUTPUT_ROUTE_ID_BY_CHANNEL[channel]

def es9_channel_is_mixer_output_routable(channel: es9_py_pb2.Channel) -> bool:
    try:
        es9_channel_to_output_route_id(channel)
        return True
    except AssertionError:
        return False

def es9_channel_is_mixer_input_routable(channel: es9_py_pb2.Channel) -> bool:
    try:
        es9_channel_to_input_route_id(channel)
        return True
    except AssertionError:
        return False

def es9_parse_message_report(payload: bytes) -> str:
    assert len(payload) >= 1, "Invalid payload length for message report"
    return payload[0: ].decode('ascii')

def es9_parse_version_string(payload: bytes) -> str:
    assert len(payload) == 6, "Invalid payload length for version string"
    return payload.decode('ascii')

def es9_parse_usage(payload: bytes) -> es9_py_pb2.Usage:
    assert len(payload) == 8, "Invalid payload length for usage report"
    u0 = payload[0] << 7 | payload[1]
    u1 = payload[2] << 7 | payload[3]
    u2 = payload[4] << 7 | payload[5]
    u3 = payload[6] << 7 | payload[7]
    return es9_py_pb2.Usage(
        usage_dsp0 = u0 / 4096.0,
        usage_dsp1 = u1 / 4096.0,
        usage_dsp2 = u2 / 4096.0,
        usage_dsp3 = u3 / 4096.0,
    )

def es9_parse_sample_rate_hz(payload: bytes) -> int:
    assert len(payload) == 3, "Invalid payload length for sample rate report"
    sample_rate = (payload[0] << 14) | (payload[1] << 7) | payload[2]
    return sample_rate * 4

def es9_parse_configuration_dump(payload: bytes) -> es9_py_pb2.Configuration:
    """
    Parse an ES-9 configuration dump SysEx payload into a Configuration protobuf message.
    """
    # Pack words back together from MIDI 7-bit bytes
    data = [
        (seg[0] << 14) | (seg[1] << 7) | seg[2]
        for seg in zip(payload[2::3], payload[3::3], payload[4::3])
    ]

    config = es9_py_pb2.Configuration()
    config.version = data[0]

    hpf = data[1]
    config.high_pass_filter_configuration.channel_pair_1_2_enabled = bool(hpf & 0x01)
    config.high_pass_filter_configuration.channel_pair_3_4_enabled = bool(hpf & 0x02)
    config.high_pass_filter_configuration.channel_pair_5_6_enabled = bool(hpf & 0x04)
    config.high_pass_filter_configuration.channel_pair_7_8_enabled = bool(hpf & 0x08)
    config.high_pass_filter_configuration.channel_pair_9_10_enabled = bool(hpf & 0x10)
    config.high_pass_filter_configuration.channel_pair_11_12_enabled = bool(hpf & 0x20)
    config.high_pass_filter_configuration.channel_pair_13_14_enabled = bool(hpf & 0x40)

    # Route in
    def route_in_value(dsp: int, ch: int) -> int:
        offset = 2 # version, hpf
        assert 0 <= dsp <= 3, "DSP block in of range"
        assert 0 <= ch <= 7, "Channel in of range"
        return data[offset + dsp*8 + ch]
    
    config.usb_routing_configuration.input1_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 0))
    config.usb_routing_configuration.input2_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 1))
    config.usb_routing_configuration.input3_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 2))
    config.usb_routing_configuration.input4_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 3))
    config.usb_routing_configuration.input5_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 4))
    config.usb_routing_configuration.input6_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 5))
    config.usb_routing_configuration.input7_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 6))
    config.usb_routing_configuration.input8_channel = es9_try_recover_channel_from_input_route_id(route_in_value(0, 7))
    config.usb_routing_configuration.input9_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 0))
    config.usb_routing_configuration.input10_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 1))
    config.usb_routing_configuration.input11_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 2))
    config.usb_routing_configuration.input12_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 3))
    config.usb_routing_configuration.input13_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 4))
    config.usb_routing_configuration.input14_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 5))
    config.usb_routing_configuration.input15_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 6))
    config.usb_routing_configuration.input16_channel = es9_try_recover_channel_from_input_route_id(route_in_value(1, 7))

    config.mixer1_routing_configuration.input1_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 0))
    config.mixer1_routing_configuration.input2_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 1))
    config.mixer1_routing_configuration.input3_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 2))
    config.mixer1_routing_configuration.input4_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 3))
    config.mixer1_routing_configuration.input5_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 4))
    config.mixer1_routing_configuration.input6_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 5))
    config.mixer1_routing_configuration.input7_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 6))
    config.mixer1_routing_configuration.input8_channel = es9_try_recover_channel_from_input_route_id(route_in_value(2, 7))

    config.mixer2_routing_configuration.input1_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 0))
    config.mixer2_routing_configuration.input2_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 1))
    config.mixer2_routing_configuration.input3_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 2))
    config.mixer2_routing_configuration.input4_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 3))
    config.mixer2_routing_configuration.input5_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 4))
    config.mixer2_routing_configuration.input6_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 5))
    config.mixer2_routing_configuration.input7_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 6))
    config.mixer2_routing_configuration.input8_channel = es9_try_recover_channel_from_input_route_id(route_in_value(3, 7))

    # Route out
    def route_out_value(dsp: int, ch: int) -> int:
        offset = 2 + 32 # version, hpf, route in (32 entries)
        assert 0 <= dsp <= 3, "DSP block out of range"
        assert 0 <= ch <= 7, "Channel out of range"
        return data[offset + dsp*8 + ch]

    config.usb_routing_configuration.output1_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 0))
    config.usb_routing_configuration.output2_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 1))
    config.usb_routing_configuration.output3_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 2))
    config.usb_routing_configuration.output4_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 3))
    config.usb_routing_configuration.output5_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 4))
    config.usb_routing_configuration.output6_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 5))
    config.usb_routing_configuration.output7_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 6))
    config.usb_routing_configuration.output8_channel = es9_try_recover_channel_from_output_route_id(route_out_value(0, 7))
    config.usb_routing_configuration.output9_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 0))
    config.usb_routing_configuration.output10_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 1))
    config.usb_routing_configuration.output11_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 2))
    config.usb_routing_configuration.output12_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 3))
    config.usb_routing_configuration.output13_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 4))
    config.usb_routing_configuration.output14_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 5))
    config.usb_routing_configuration.output15_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 6))
    config.usb_routing_configuration.output16_channel = es9_try_recover_channel_from_output_route_id(route_out_value(1, 7))

    config.mixer1_routing_configuration.output1_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 0))
    config.mixer1_routing_configuration.output2_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 1))
    config.mixer1_routing_configuration.output3_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 2))
    config.mixer1_routing_configuration.output4_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 3))
    config.mixer1_routing_configuration.output5_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 4))
    config.mixer1_routing_configuration.output6_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 5))
    config.mixer1_routing_configuration.output7_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 6))
    config.mixer1_routing_configuration.output8_channel = es9_try_recover_channel_from_output_route_id(route_out_value(2, 7))

    config.mixer2_routing_configuration.output1_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 0))
    config.mixer2_routing_configuration.output2_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 1))
    config.mixer2_routing_configuration.output3_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 2))
    config.mixer2_routing_configuration.output4_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 3))
    config.mixer2_routing_configuration.output5_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 4))
    config.mixer2_routing_configuration.output6_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 5))
    config.mixer2_routing_configuration.output7_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 6))
    config.mixer2_routing_configuration.output8_channel = es9_try_recover_channel_from_output_route_id(route_out_value(3, 7))

    # Mix
    def extract_mix_value_from_config_dump(mix_id: int, ch: int) -> int:
        offset = 2 + 32 + 32 # version, hpf, route in (32), route out (32)s
        assert 0 <= mix_id <= 15, "Mix ID out of range"
        assert 0 <= ch <= 7, "Channel out of range"
        return data[offset + mix_id*8 + ch]

    config.mixer1_crosspoint_configuration.output1_configuration.input1_level = extract_mix_value_from_config_dump(0, 0)
    config.mixer1_crosspoint_configuration.output1_configuration.input2_level = extract_mix_value_from_config_dump(0, 1)
    config.mixer1_crosspoint_configuration.output1_configuration.input3_level = extract_mix_value_from_config_dump(0, 2)
    config.mixer1_crosspoint_configuration.output1_configuration.input4_level = extract_mix_value_from_config_dump(0, 3)
    config.mixer1_crosspoint_configuration.output1_configuration.input5_level = extract_mix_value_from_config_dump(0, 4)
    config.mixer1_crosspoint_configuration.output1_configuration.input6_level = extract_mix_value_from_config_dump(0, 5)
    config.mixer1_crosspoint_configuration.output1_configuration.input7_level = extract_mix_value_from_config_dump(0, 6)
    config.mixer1_crosspoint_configuration.output1_configuration.input8_level = extract_mix_value_from_config_dump(0, 7)

    config.mixer1_crosspoint_configuration.output2_configuration.input1_level = extract_mix_value_from_config_dump(1, 0)
    config.mixer1_crosspoint_configuration.output2_configuration.input2_level = extract_mix_value_from_config_dump(1, 1)
    config.mixer1_crosspoint_configuration.output2_configuration.input3_level = extract_mix_value_from_config_dump(1, 2)
    config.mixer1_crosspoint_configuration.output2_configuration.input4_level = extract_mix_value_from_config_dump(1, 3)
    config.mixer1_crosspoint_configuration.output2_configuration.input5_level = extract_mix_value_from_config_dump(1, 4)
    config.mixer1_crosspoint_configuration.output2_configuration.input6_level = extract_mix_value_from_config_dump(1, 5)
    config.mixer1_crosspoint_configuration.output2_configuration.input7_level = extract_mix_value_from_config_dump(1, 6)
    config.mixer1_crosspoint_configuration.output2_configuration.input8_level = extract_mix_value_from_config_dump(1, 7)

    config.mixer1_crosspoint_configuration.output3_configuration.input1_level = extract_mix_value_from_config_dump(2, 0)
    config.mixer1_crosspoint_configuration.output3_configuration.input2_level = extract_mix_value_from_config_dump(2, 1)
    config.mixer1_crosspoint_configuration.output3_configuration.input3_level = extract_mix_value_from_config_dump(2, 2)
    config.mixer1_crosspoint_configuration.output3_configuration.input4_level = extract_mix_value_from_config_dump(2, 3)
    config.mixer1_crosspoint_configuration.output3_configuration.input5_level = extract_mix_value_from_config_dump(2, 4)
    config.mixer1_crosspoint_configuration.output3_configuration.input6_level = extract_mix_value_from_config_dump(2, 5)
    config.mixer1_crosspoint_configuration.output3_configuration.input7_level = extract_mix_value_from_config_dump(2, 6)
    config.mixer1_crosspoint_configuration.output3_configuration.input8_level = extract_mix_value_from_config_dump(2, 7)

    config.mixer1_crosspoint_configuration.output4_configuration.input1_level = extract_mix_value_from_config_dump(3, 0)
    config.mixer1_crosspoint_configuration.output4_configuration.input2_level = extract_mix_value_from_config_dump(3, 1)
    config.mixer1_crosspoint_configuration.output4_configuration.input3_level = extract_mix_value_from_config_dump(3, 2)
    config.mixer1_crosspoint_configuration.output4_configuration.input4_level = extract_mix_value_from_config_dump(3, 3)
    config.mixer1_crosspoint_configuration.output4_configuration.input5_level = extract_mix_value_from_config_dump(3, 4)
    config.mixer1_crosspoint_configuration.output4_configuration.input6_level = extract_mix_value_from_config_dump(3, 5)
    config.mixer1_crosspoint_configuration.output4_configuration.input7_level = extract_mix_value_from_config_dump(3, 6)
    config.mixer1_crosspoint_configuration.output4_configuration.input8_level = extract_mix_value_from_config_dump(3, 7)

    config.mixer1_crosspoint_configuration.output5_configuration.input1_level = extract_mix_value_from_config_dump(4, 0)
    config.mixer1_crosspoint_configuration.output5_configuration.input2_level = extract_mix_value_from_config_dump(4, 1)
    config.mixer1_crosspoint_configuration.output5_configuration.input3_level = extract_mix_value_from_config_dump(4, 2)
    config.mixer1_crosspoint_configuration.output5_configuration.input4_level = extract_mix_value_from_config_dump(4, 3)
    config.mixer1_crosspoint_configuration.output5_configuration.input5_level = extract_mix_value_from_config_dump(4, 4)
    config.mixer1_crosspoint_configuration.output5_configuration.input6_level = extract_mix_value_from_config_dump(4, 5)
    config.mixer1_crosspoint_configuration.output5_configuration.input7_level = extract_mix_value_from_config_dump(4, 6)
    config.mixer1_crosspoint_configuration.output5_configuration.input8_level = extract_mix_value_from_config_dump(4, 7)

    config.mixer1_crosspoint_configuration.output6_configuration.input1_level = extract_mix_value_from_config_dump(5, 0)
    config.mixer1_crosspoint_configuration.output6_configuration.input2_level = extract_mix_value_from_config_dump(5, 1)
    config.mixer1_crosspoint_configuration.output6_configuration.input3_level = extract_mix_value_from_config_dump(5, 2)
    config.mixer1_crosspoint_configuration.output6_configuration.input4_level = extract_mix_value_from_config_dump(5, 3)
    config.mixer1_crosspoint_configuration.output6_configuration.input5_level = extract_mix_value_from_config_dump(5, 4)
    config.mixer1_crosspoint_configuration.output6_configuration.input6_level = extract_mix_value_from_config_dump(5, 5)
    config.mixer1_crosspoint_configuration.output6_configuration.input7_level = extract_mix_value_from_config_dump(5, 6)
    config.mixer1_crosspoint_configuration.output6_configuration.input8_level = extract_mix_value_from_config_dump(5, 7)

    config.mixer1_crosspoint_configuration.output7_configuration.input1_level = extract_mix_value_from_config_dump(6, 0)
    config.mixer1_crosspoint_configuration.output7_configuration.input2_level = extract_mix_value_from_config_dump(6, 1)
    config.mixer1_crosspoint_configuration.output7_configuration.input3_level = extract_mix_value_from_config_dump(6, 2)
    config.mixer1_crosspoint_configuration.output7_configuration.input4_level = extract_mix_value_from_config_dump(6, 3)
    config.mixer1_crosspoint_configuration.output7_configuration.input5_level = extract_mix_value_from_config_dump(6, 4)
    config.mixer1_crosspoint_configuration.output7_configuration.input6_level = extract_mix_value_from_config_dump(6, 5)
    config.mixer1_crosspoint_configuration.output7_configuration.input7_level = extract_mix_value_from_config_dump(6, 6)
    config.mixer1_crosspoint_configuration.output7_configuration.input8_level = extract_mix_value_from_config_dump(6, 7)

    config.mixer1_crosspoint_configuration.output8_configuration.input1_level = extract_mix_value_from_config_dump(7, 0)
    config.mixer1_crosspoint_configuration.output8_configuration.input2_level = extract_mix_value_from_config_dump(7, 1)
    config.mixer1_crosspoint_configuration.output8_configuration.input3_level = extract_mix_value_from_config_dump(7, 2)
    config.mixer1_crosspoint_configuration.output8_configuration.input4_level = extract_mix_value_from_config_dump(7, 3)
    config.mixer1_crosspoint_configuration.output8_configuration.input5_level = extract_mix_value_from_config_dump(7, 4)
    config.mixer1_crosspoint_configuration.output8_configuration.input6_level = extract_mix_value_from_config_dump(7, 5)
    config.mixer1_crosspoint_configuration.output8_configuration.input7_level = extract_mix_value_from_config_dump(7, 6)
    config.mixer1_crosspoint_configuration.output8_configuration.input8_level = extract_mix_value_from_config_dump(7, 7)

    config.mixer2_crosspoint_configuration.output1_configuration.input1_level = extract_mix_value_from_config_dump(8, 0)
    config.mixer2_crosspoint_configuration.output1_configuration.input2_level = extract_mix_value_from_config_dump(8, 1)
    config.mixer2_crosspoint_configuration.output1_configuration.input3_level = extract_mix_value_from_config_dump(8, 2)
    config.mixer2_crosspoint_configuration.output1_configuration.input4_level = extract_mix_value_from_config_dump(8, 3)
    config.mixer2_crosspoint_configuration.output1_configuration.input5_level = extract_mix_value_from_config_dump(8, 4)
    config.mixer2_crosspoint_configuration.output1_configuration.input6_level = extract_mix_value_from_config_dump(8, 5)
    config.mixer2_crosspoint_configuration.output1_configuration.input7_level = extract_mix_value_from_config_dump(8, 6)
    config.mixer2_crosspoint_configuration.output1_configuration.input8_level = extract_mix_value_from_config_dump(8, 7)

    config.mixer2_crosspoint_configuration.output2_configuration.input1_level = extract_mix_value_from_config_dump(9, 0)
    config.mixer2_crosspoint_configuration.output2_configuration.input2_level = extract_mix_value_from_config_dump(9, 1)
    config.mixer2_crosspoint_configuration.output2_configuration.input3_level = extract_mix_value_from_config_dump(9, 2)
    config.mixer2_crosspoint_configuration.output2_configuration.input4_level = extract_mix_value_from_config_dump(9, 3)
    config.mixer2_crosspoint_configuration.output2_configuration.input5_level = extract_mix_value_from_config_dump(9, 4)
    config.mixer2_crosspoint_configuration.output2_configuration.input6_level = extract_mix_value_from_config_dump(9, 5)
    config.mixer2_crosspoint_configuration.output2_configuration.input7_level = extract_mix_value_from_config_dump(9, 6)
    config.mixer2_crosspoint_configuration.output2_configuration.input8_level = extract_mix_value_from_config_dump(9, 7)

    config.mixer2_crosspoint_configuration.output3_configuration.input1_level = extract_mix_value_from_config_dump(10, 0)
    config.mixer2_crosspoint_configuration.output3_configuration.input2_level = extract_mix_value_from_config_dump(10, 1)
    config.mixer2_crosspoint_configuration.output3_configuration.input3_level = extract_mix_value_from_config_dump(10, 2)
    config.mixer2_crosspoint_configuration.output3_configuration.input4_level = extract_mix_value_from_config_dump(10, 3)
    config.mixer2_crosspoint_configuration.output3_configuration.input5_level = extract_mix_value_from_config_dump(10, 4)
    config.mixer2_crosspoint_configuration.output3_configuration.input6_level = extract_mix_value_from_config_dump(10, 5)
    config.mixer2_crosspoint_configuration.output3_configuration.input7_level = extract_mix_value_from_config_dump(10, 6)
    config.mixer2_crosspoint_configuration.output3_configuration.input8_level = extract_mix_value_from_config_dump(10, 7)

    config.mixer2_crosspoint_configuration.output4_configuration.input1_level = extract_mix_value_from_config_dump(11, 0)
    config.mixer2_crosspoint_configuration.output4_configuration.input2_level = extract_mix_value_from_config_dump(11, 1)
    config.mixer2_crosspoint_configuration.output4_configuration.input3_level = extract_mix_value_from_config_dump(11, 2)
    config.mixer2_crosspoint_configuration.output4_configuration.input4_level = extract_mix_value_from_config_dump(11, 3)
    config.mixer2_crosspoint_configuration.output4_configuration.input5_level = extract_mix_value_from_config_dump(11, 4)
    config.mixer2_crosspoint_configuration.output4_configuration.input6_level = extract_mix_value_from_config_dump(11, 5)
    config.mixer2_crosspoint_configuration.output4_configuration.input7_level = extract_mix_value_from_config_dump(11, 6)
    config.mixer2_crosspoint_configuration.output4_configuration.input8_level = extract_mix_value_from_config_dump(11, 7)

    config.mixer2_crosspoint_configuration.output5_configuration.input1_level = extract_mix_value_from_config_dump(12, 0)
    config.mixer2_crosspoint_configuration.output5_configuration.input2_level = extract_mix_value_from_config_dump(12, 1)
    config.mixer2_crosspoint_configuration.output5_configuration.input3_level = extract_mix_value_from_config_dump(12, 2)
    config.mixer2_crosspoint_configuration.output5_configuration.input4_level = extract_mix_value_from_config_dump(12, 3)
    config.mixer2_crosspoint_configuration.output5_configuration.input5_level = extract_mix_value_from_config_dump(12, 4)
    config.mixer2_crosspoint_configuration.output5_configuration.input6_level = extract_mix_value_from_config_dump(12, 5)
    config.mixer2_crosspoint_configuration.output5_configuration.input7_level = extract_mix_value_from_config_dump(12, 6)
    config.mixer2_crosspoint_configuration.output5_configuration.input8_level = extract_mix_value_from_config_dump(12, 7)

    config.mixer2_crosspoint_configuration.output6_configuration.input1_level = extract_mix_value_from_config_dump(13, 0)
    config.mixer2_crosspoint_configuration.output6_configuration.input2_level = extract_mix_value_from_config_dump(13, 1)
    config.mixer2_crosspoint_configuration.output6_configuration.input3_level = extract_mix_value_from_config_dump(13, 2)
    config.mixer2_crosspoint_configuration.output6_configuration.input4_level = extract_mix_value_from_config_dump(13, 3)
    config.mixer2_crosspoint_configuration.output6_configuration.input5_level = extract_mix_value_from_config_dump(13, 4)
    config.mixer2_crosspoint_configuration.output6_configuration.input6_level = extract_mix_value_from_config_dump(13, 5)
    config.mixer2_crosspoint_configuration.output6_configuration.input7_level = extract_mix_value_from_config_dump(13, 6)
    config.mixer2_crosspoint_configuration.output6_configuration.input8_level = extract_mix_value_from_config_dump(13, 7)

    config.mixer2_crosspoint_configuration.output7_configuration.input1_level = extract_mix_value_from_config_dump(14, 0)
    config.mixer2_crosspoint_configuration.output7_configuration.input2_level = extract_mix_value_from_config_dump(14, 1)
    config.mixer2_crosspoint_configuration.output7_configuration.input3_level = extract_mix_value_from_config_dump(14, 2)
    config.mixer2_crosspoint_configuration.output7_configuration.input4_level = extract_mix_value_from_config_dump(14, 3)
    config.mixer2_crosspoint_configuration.output7_configuration.input5_level = extract_mix_value_from_config_dump(14, 4)
    config.mixer2_crosspoint_configuration.output7_configuration.input6_level = extract_mix_value_from_config_dump(14, 5)
    config.mixer2_crosspoint_configuration.output7_configuration.input7_level = extract_mix_value_from_config_dump(14, 6)
    config.mixer2_crosspoint_configuration.output7_configuration.input8_level = extract_mix_value_from_config_dump(14, 7)

    config.mixer2_crosspoint_configuration.output8_configuration.input1_level = extract_mix_value_from_config_dump(15, 0)
    config.mixer2_crosspoint_configuration.output8_configuration.input2_level = extract_mix_value_from_config_dump(15, 1)
    config.mixer2_crosspoint_configuration.output8_configuration.input3_level = extract_mix_value_from_config_dump(15, 2)
    config.mixer2_crosspoint_configuration.output8_configuration.input4_level = extract_mix_value_from_config_dump(15, 3)
    config.mixer2_crosspoint_configuration.output8_configuration.input5_level = extract_mix_value_from_config_dump(15, 4)
    config.mixer2_crosspoint_configuration.output8_configuration.input6_level = extract_mix_value_from_config_dump(15, 5)
    config.mixer2_crosspoint_configuration.output8_configuration.input7_level = extract_mix_value_from_config_dump(15, 6)
    config.mixer2_crosspoint_configuration.output8_configuration.input8_level = extract_mix_value_from_config_dump(15, 7)

    # Options
    opt = data[450]
    config.options_configuration.use_spdif = not bool(opt & 0x01)
    config.options_configuration.use_midi_through = bool(opt & 0x02)

    # Links
    links = (data[452] << 16) | data[451]
    config.mixer_links_configuration.link_channel_input_1_2 = bool(links >> 0 & 0x01)
    config.mixer_links_configuration.link_channel_input_3_4 = bool(links >> 1 & 0x01)
    config.mixer_links_configuration.link_channel_input_5_6 = bool(links >> 2 & 0x01)
    config.mixer_links_configuration.link_channel_input_7_8 = bool(links >> 3 & 0x01)
    config.mixer_links_configuration.link_channel_input_9_10 = bool(links >> 4 & 0x01)
    config.mixer_links_configuration.link_channel_input_11_12 = bool(links >> 5 & 0x01)
    config.mixer_links_configuration.link_channel_input_13_14 = bool(links >> 6 & 0x01)
    config.mixer_links_configuration.link_channel_bus_1_2 = bool(links >> 8 & 0x01)
    config.mixer_links_configuration.link_channel_bus_3_4 = bool(links >> 9 & 0x01)
    config.mixer_links_configuration.link_channel_bus_5_6 = bool(links >> 10 & 0x01)
    config.mixer_links_configuration.link_channel_bus_7_8 = bool(links >> 11 & 0x01)
    config.mixer_links_configuration.link_channel_bus_9_10 = bool(links >> 12 & 0x01)
    config.mixer_links_configuration.link_channel_bus_11_12 = bool(links >> 13 & 0x01)
    config.mixer_links_configuration.link_channel_bus_13_14 = bool(links >> 14 & 0x01)
    config.mixer_links_configuration.link_channel_bus_15_16 = bool(links >> 15 & 0x01)
    config.mixer_links_configuration.link_channel_usb_1_2 = bool(links >> 16 & 0x01)
    config.mixer_links_configuration.link_channel_usb_3_4 = bool(links >> 17 & 0x01)
    config.mixer_links_configuration.link_channel_usb_5_6 = bool(links >> 18 & 0x01)
    config.mixer_links_configuration.link_channel_usb_7_8 = bool(links >> 19 & 0x01)
    config.mixer_links_configuration.link_channel_usb_9_10 = bool(links >> 20 & 0x01)
    config.mixer_links_configuration.link_channel_usb_11_12 = bool(links >> 21 & 0x01)
    config.mixer_links_configuration.link_channel_usb_13_14 = bool(links >> 22 & 0x01)
    config.mixer_links_configuration.link_channel_usb_15_16 = bool(links >> 23 & 0x01)
    config.mixer_links_configuration.link_channel_mix_1_2 = bool(links >> 24 & 0x01)
    config.mixer_links_configuration.link_channel_mix_3_4 = bool(links >> 25 & 0x01)
    config.mixer_links_configuration.link_channel_mix_5_6 = bool(links >> 26 & 0x01)
    config.mixer_links_configuration.link_channel_mix_7_8 = bool(links >> 27 & 0x01)
    config.mixer_links_configuration.link_channel_mix_9_10 = bool(links >> 28 & 0x01)
    config.mixer_links_configuration.link_channel_mix_11_12 = bool(links >> 29 & 0x01)
    config.mixer_links_configuration.link_channel_mix_13_14 = bool(links >> 30 & 0x01)
    config.mixer_links_configuration.link_channel_mix_15_16 = bool(links >> 31 & 0x01)

    # MIDI Channels
    channels = data[453]
    config.midi_channels_configuration.usb_midi_channel = (channels >> 8) & 0xFF
    config.midi_channels_configuration.din_midi_channel = channels & 0xFF

    # DC Offsets
    def to_int16(v):
        v &= 0xFFFF          # keep only the lower 16 bits
        if v & 0x8000:       # if sign bit is set
            v -= 0x10000     # subtract 2^16 to sign-extend
        return v

    config.output_dc_offset_configuration.output1_offset = to_int16(data[454])
    config.output_dc_offset_configuration.output2_offset = to_int16(data[455])
    config.output_dc_offset_configuration.output3_offset = to_int16(data[456])
    config.output_dc_offset_configuration.output4_offset = to_int16(data[457])
    config.output_dc_offset_configuration.output5_offset = to_int16(data[458])
    config.output_dc_offset_configuration.output6_offset = to_int16(data[459])
    config.output_dc_offset_configuration.output7_offset = to_int16(data[460])
    config.output_dc_offset_configuration.output8_offset = to_int16(data[461])

    # Filters
    def get_filter_config(mix_idx: int, filter_idx: int, cursor: int) -> es9_py_pb2.Configuration.MixInputFilterConfiguration.FilterConfiguration:
        def to_int16(v):
            v &= 0xFFFF          # keep only the lower 16 bits
            if v & 0x8000:       # if sign bit is set
                v -= 0x10000     # subtract 2^16 to sign-extend
            return v
        
        filter_config = es9_py_pb2.Configuration.MixInputFilterConfiguration.FilterConfiguration()
        offset = cursor + (mix_idx * 4 + filter_idx) * 4
        type_byte = data[offset + 0]

        filter_config.enabled = es9_filter_enabled_from_storage_value(type_byte)
        filter_config.filter_type = es9_filter_type_from_storage_value(type_byte)
        filter_config.frequency_hz = data[offset + 1]
        filter_config.q_factor = data[offset + 2]
        filter_config.gain = to_int16(data[offset + 3])

        return filter_config

    filter_cursor_base = 462

    config.mix_input_filter_configuration.mix1_filter1.CopyFrom(get_filter_config(0, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix1_filter2.CopyFrom(get_filter_config(0, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix1_filter3.CopyFrom(get_filter_config(0, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix1_filter4.CopyFrom(get_filter_config(0, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix2_filter1.CopyFrom(get_filter_config(1, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix2_filter2.CopyFrom(get_filter_config(1, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix2_filter3.CopyFrom(get_filter_config(1, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix2_filter4.CopyFrom(get_filter_config(1, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix3_filter1.CopyFrom(get_filter_config(2, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix3_filter2.CopyFrom(get_filter_config(2, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix3_filter3.CopyFrom(get_filter_config(2, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix3_filter4.CopyFrom(get_filter_config(2, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix4_filter1.CopyFrom(get_filter_config(3, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix4_filter2.CopyFrom(get_filter_config(3, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix4_filter3.CopyFrom(get_filter_config(3, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix4_filter4.CopyFrom(get_filter_config(3, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix5_filter1.CopyFrom(get_filter_config(4, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix5_filter2.CopyFrom(get_filter_config(4, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix5_filter3.CopyFrom(get_filter_config(4, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix5_filter4.CopyFrom(get_filter_config(4, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix6_filter1.CopyFrom(get_filter_config(5, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix6_filter2.CopyFrom(get_filter_config(5, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix6_filter3.CopyFrom(get_filter_config(5, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix6_filter4.CopyFrom(get_filter_config(5, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix7_filter1.CopyFrom(get_filter_config(6, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix7_filter2.CopyFrom(get_filter_config(6, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix7_filter3.CopyFrom(get_filter_config(6, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix7_filter4.CopyFrom(get_filter_config(6, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix8_filter1.CopyFrom(get_filter_config(7, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix8_filter2.CopyFrom(get_filter_config(7, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix8_filter3.CopyFrom(get_filter_config(7, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix8_filter4.CopyFrom(get_filter_config(7, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix9_filter1.CopyFrom(get_filter_config(8, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix9_filter2.CopyFrom(get_filter_config(8, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix9_filter3.CopyFrom(get_filter_config(8, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix9_filter4.CopyFrom(get_filter_config(8, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix10_filter1.CopyFrom(get_filter_config(9, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix10_filter2.CopyFrom(get_filter_config(9, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix10_filter3.CopyFrom(get_filter_config(9, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix10_filter4.CopyFrom(get_filter_config(9, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix11_filter1.CopyFrom(get_filter_config(10, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix11_filter2.CopyFrom(get_filter_config(10, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix11_filter3.CopyFrom(get_filter_config(10, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix11_filter4.CopyFrom(get_filter_config(10, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix12_filter1.CopyFrom(get_filter_config(11, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix12_filter2.CopyFrom(get_filter_config(11, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix12_filter3.CopyFrom(get_filter_config(11, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix12_filter4.CopyFrom(get_filter_config(11, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix13_filter1.CopyFrom(get_filter_config(12, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix13_filter2.CopyFrom(get_filter_config(12, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix13_filter3.CopyFrom(get_filter_config(12, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix13_filter4.CopyFrom(get_filter_config(12, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix14_filter1.CopyFrom(get_filter_config(13, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix14_filter2.CopyFrom(get_filter_config(13, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix14_filter3.CopyFrom(get_filter_config(13, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix14_filter4.CopyFrom(get_filter_config(13, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix15_filter1.CopyFrom(get_filter_config(14, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix15_filter2.CopyFrom(get_filter_config(14, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix15_filter3.CopyFrom(get_filter_config(14, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix15_filter4.CopyFrom(get_filter_config(14, 3, filter_cursor_base))

    config.mix_input_filter_configuration.mix16_filter1.CopyFrom(get_filter_config(15, 0, filter_cursor_base))
    config.mix_input_filter_configuration.mix16_filter2.CopyFrom(get_filter_config(15, 1, filter_cursor_base))
    config.mix_input_filter_configuration.mix16_filter3.CopyFrom(get_filter_config(15, 2, filter_cursor_base))
    config.mix_input_filter_configuration.mix16_filter4.CopyFrom(get_filter_config(15, 3, filter_cursor_base))

    # Smoothing
    smoothing = data[718]
    config.mix_smoothing_configuration.mix1_enabled = bool(smoothing & 0x01)
    config.mix_smoothing_configuration.mix2_enabled = bool(smoothing & 0x02)
    config.mix_smoothing_configuration.mix3_enabled = bool(smoothing & 0x04)
    config.mix_smoothing_configuration.mix4_enabled = bool(smoothing & 0x08)
    config.mix_smoothing_configuration.mix5_enabled = bool(smoothing & 0x10)
    config.mix_smoothing_configuration.mix6_enabled = bool(smoothing & 0x20)
    config.mix_smoothing_configuration.mix7_enabled = bool(smoothing & 0x40)
    config.mix_smoothing_configuration.mix8_enabled = bool(smoothing & 0x80)
    config.mix_smoothing_configuration.mix9_enabled = bool(smoothing & 0x100)
    config.mix_smoothing_configuration.mix10_enabled = bool(smoothing & 0x200)
    config.mix_smoothing_configuration.mix11_enabled = bool(smoothing & 0x400)
    config.mix_smoothing_configuration.mix12_enabled = bool(smoothing & 0x800)
    config.mix_smoothing_configuration.mix13_enabled = bool(smoothing & 0x1000)
    config.mix_smoothing_configuration.mix14_enabled = bool(smoothing & 0x2000)
    config.mix_smoothing_configuration.mix15_enabled = bool(smoothing & 0x4000)
    config.mix_smoothing_configuration.mix16_enabled = bool(smoothing & 0x8000)

    return config

def es9_parse_mix_dump(data: bytes) -> es9_py_pb2.MixConfiguration:
    raw_mix = [
        (seg[0] << 14) | (seg[1] << 7) | seg[2]
        for seg in zip(data[0::3], data[1::3], data[2::3])
    ]

    config = es9_py_pb2.MixConfiguration()

    config.mixer1_crosspoint_configuration.output1_configuration.input1_level = raw_mix[0]
    config.mixer1_crosspoint_configuration.output1_configuration.input2_level = raw_mix[1]
    config.mixer1_crosspoint_configuration.output1_configuration.input3_level = raw_mix[2]
    config.mixer1_crosspoint_configuration.output1_configuration.input4_level = raw_mix[3]
    config.mixer1_crosspoint_configuration.output1_configuration.input5_level = raw_mix[4]
    config.mixer1_crosspoint_configuration.output1_configuration.input6_level = raw_mix[5]
    config.mixer1_crosspoint_configuration.output1_configuration.input7_level = raw_mix[6]
    config.mixer1_crosspoint_configuration.output1_configuration.input8_level = raw_mix[7]

    config.mixer1_crosspoint_configuration.output2_configuration.input1_level = raw_mix[8]
    config.mixer1_crosspoint_configuration.output2_configuration.input2_level = raw_mix[9]
    config.mixer1_crosspoint_configuration.output2_configuration.input3_level = raw_mix[10]
    config.mixer1_crosspoint_configuration.output2_configuration.input4_level = raw_mix[11]
    config.mixer1_crosspoint_configuration.output2_configuration.input5_level = raw_mix[12]
    config.mixer1_crosspoint_configuration.output2_configuration.input6_level = raw_mix[13]
    config.mixer1_crosspoint_configuration.output2_configuration.input7_level = raw_mix[14]
    config.mixer1_crosspoint_configuration.output2_configuration.input8_level = raw_mix[15]

    config.mixer1_crosspoint_configuration.output3_configuration.input1_level = raw_mix[16]
    config.mixer1_crosspoint_configuration.output3_configuration.input2_level = raw_mix[17]
    config.mixer1_crosspoint_configuration.output3_configuration.input3_level = raw_mix[18]
    config.mixer1_crosspoint_configuration.output3_configuration.input4_level = raw_mix[19]
    config.mixer1_crosspoint_configuration.output3_configuration.input5_level = raw_mix[20]
    config.mixer1_crosspoint_configuration.output3_configuration.input6_level = raw_mix[21]
    config.mixer1_crosspoint_configuration.output3_configuration.input7_level = raw_mix[22]
    config.mixer1_crosspoint_configuration.output3_configuration.input8_level = raw_mix[23]

    config.mixer1_crosspoint_configuration.output4_configuration.input1_level = raw_mix[24]
    config.mixer1_crosspoint_configuration.output4_configuration.input2_level = raw_mix[25]
    config.mixer1_crosspoint_configuration.output4_configuration.input3_level = raw_mix[26]
    config.mixer1_crosspoint_configuration.output4_configuration.input4_level = raw_mix[27]
    config.mixer1_crosspoint_configuration.output4_configuration.input5_level = raw_mix[28]
    config.mixer1_crosspoint_configuration.output4_configuration.input6_level = raw_mix[29]
    config.mixer1_crosspoint_configuration.output4_configuration.input7_level = raw_mix[30]
    config.mixer1_crosspoint_configuration.output4_configuration.input8_level = raw_mix[31]

    config.mixer1_crosspoint_configuration.output5_configuration.input1_level = raw_mix[32]
    config.mixer1_crosspoint_configuration.output5_configuration.input2_level = raw_mix[33]
    config.mixer1_crosspoint_configuration.output5_configuration.input3_level = raw_mix[34]
    config.mixer1_crosspoint_configuration.output5_configuration.input4_level = raw_mix[35]
    config.mixer1_crosspoint_configuration.output5_configuration.input5_level = raw_mix[36]
    config.mixer1_crosspoint_configuration.output5_configuration.input6_level = raw_mix[37]
    config.mixer1_crosspoint_configuration.output5_configuration.input7_level = raw_mix[38]
    config.mixer1_crosspoint_configuration.output5_configuration.input8_level = raw_mix[39]

    config.mixer1_crosspoint_configuration.output6_configuration.input1_level = raw_mix[40]
    config.mixer1_crosspoint_configuration.output6_configuration.input2_level = raw_mix[41]
    config.mixer1_crosspoint_configuration.output6_configuration.input3_level = raw_mix[42]
    config.mixer1_crosspoint_configuration.output6_configuration.input4_level = raw_mix[43]
    config.mixer1_crosspoint_configuration.output6_configuration.input5_level = raw_mix[44]
    config.mixer1_crosspoint_configuration.output6_configuration.input6_level = raw_mix[45]
    config.mixer1_crosspoint_configuration.output6_configuration.input7_level = raw_mix[46]
    config.mixer1_crosspoint_configuration.output6_configuration.input8_level = raw_mix[47]

    config.mixer1_crosspoint_configuration.output7_configuration.input1_level = raw_mix[48]
    config.mixer1_crosspoint_configuration.output7_configuration.input2_level = raw_mix[49]
    config.mixer1_crosspoint_configuration.output7_configuration.input3_level = raw_mix[50]
    config.mixer1_crosspoint_configuration.output7_configuration.input4_level = raw_mix[51]
    config.mixer1_crosspoint_configuration.output7_configuration.input5_level = raw_mix[52]
    config.mixer1_crosspoint_configuration.output7_configuration.input6_level = raw_mix[53]
    config.mixer1_crosspoint_configuration.output7_configuration.input7_level = raw_mix[54]
    config.mixer1_crosspoint_configuration.output7_configuration.input8_level = raw_mix[55]

    config.mixer1_crosspoint_configuration.output8_configuration.input1_level = raw_mix[56]
    config.mixer1_crosspoint_configuration.output8_configuration.input2_level = raw_mix[57]
    config.mixer1_crosspoint_configuration.output8_configuration.input3_level = raw_mix[58]
    config.mixer1_crosspoint_configuration.output8_configuration.input4_level = raw_mix[59]
    config.mixer1_crosspoint_configuration.output8_configuration.input5_level = raw_mix[60]
    config.mixer1_crosspoint_configuration.output8_configuration.input6_level = raw_mix[61]
    config.mixer1_crosspoint_configuration.output8_configuration.input7_level = raw_mix[62]
    config.mixer1_crosspoint_configuration.output8_configuration.input8_level = raw_mix[63]

    config.mixer2_crosspoint_configuration.output1_configuration.input1_level = raw_mix[64]
    config.mixer2_crosspoint_configuration.output1_configuration.input2_level = raw_mix[65]
    config.mixer2_crosspoint_configuration.output1_configuration.input3_level = raw_mix[66]
    config.mixer2_crosspoint_configuration.output1_configuration.input4_level = raw_mix[67]
    config.mixer2_crosspoint_configuration.output1_configuration.input5_level = raw_mix[68]
    config.mixer2_crosspoint_configuration.output1_configuration.input6_level = raw_mix[69]
    config.mixer2_crosspoint_configuration.output1_configuration.input7_level = raw_mix[70]
    config.mixer2_crosspoint_configuration.output1_configuration.input8_level = raw_mix[71]

    config.mixer2_crosspoint_configuration.output2_configuration.input1_level = raw_mix[72]
    config.mixer2_crosspoint_configuration.output2_configuration.input2_level = raw_mix[73]
    config.mixer2_crosspoint_configuration.output2_configuration.input3_level = raw_mix[74]
    config.mixer2_crosspoint_configuration.output2_configuration.input4_level = raw_mix[75]
    config.mixer2_crosspoint_configuration.output2_configuration.input5_level = raw_mix[76]
    config.mixer2_crosspoint_configuration.output2_configuration.input6_level = raw_mix[77]
    config.mixer2_crosspoint_configuration.output2_configuration.input7_level = raw_mix[78]
    config.mixer2_crosspoint_configuration.output2_configuration.input8_level = raw_mix[79]

    config.mixer2_crosspoint_configuration.output3_configuration.input1_level = raw_mix[80]
    config.mixer2_crosspoint_configuration.output3_configuration.input2_level = raw_mix[81]
    config.mixer2_crosspoint_configuration.output3_configuration.input3_level = raw_mix[82]
    config.mixer2_crosspoint_configuration.output3_configuration.input4_level = raw_mix[83]
    config.mixer2_crosspoint_configuration.output3_configuration.input5_level = raw_mix[84]
    config.mixer2_crosspoint_configuration.output3_configuration.input6_level = raw_mix[85]
    config.mixer2_crosspoint_configuration.output3_configuration.input7_level = raw_mix[86]
    config.mixer2_crosspoint_configuration.output3_configuration.input8_level = raw_mix[87]

    config.mixer2_crosspoint_configuration.output4_configuration.input1_level = raw_mix[88]
    config.mixer2_crosspoint_configuration.output4_configuration.input2_level = raw_mix[89]
    config.mixer2_crosspoint_configuration.output4_configuration.input3_level = raw_mix[90]
    config.mixer2_crosspoint_configuration.output4_configuration.input4_level = raw_mix[91]
    config.mixer2_crosspoint_configuration.output4_configuration.input5_level = raw_mix[92]
    config.mixer2_crosspoint_configuration.output4_configuration.input6_level = raw_mix[93]
    config.mixer2_crosspoint_configuration.output4_configuration.input7_level = raw_mix[94]
    config.mixer2_crosspoint_configuration.output4_configuration.input8_level = raw_mix[95]

    config.mixer2_crosspoint_configuration.output5_configuration.input1_level = raw_mix[96]
    config.mixer2_crosspoint_configuration.output5_configuration.input2_level = raw_mix[97]
    config.mixer2_crosspoint_configuration.output5_configuration.input3_level = raw_mix[98]
    config.mixer2_crosspoint_configuration.output5_configuration.input4_level = raw_mix[99]
    config.mixer2_crosspoint_configuration.output5_configuration.input5_level = raw_mix[100]
    config.mixer2_crosspoint_configuration.output5_configuration.input6_level = raw_mix[101]
    config.mixer2_crosspoint_configuration.output5_configuration.input7_level = raw_mix[102]
    config.mixer2_crosspoint_configuration.output5_configuration.input8_level = raw_mix[103]

    config.mixer2_crosspoint_configuration.output6_configuration.input1_level = raw_mix[104]
    config.mixer2_crosspoint_configuration.output6_configuration.input2_level = raw_mix[105]
    config.mixer2_crosspoint_configuration.output6_configuration.input3_level = raw_mix[106]
    config.mixer2_crosspoint_configuration.output6_configuration.input4_level = raw_mix[107]
    config.mixer2_crosspoint_configuration.output6_configuration.input5_level = raw_mix[108]
    config.mixer2_crosspoint_configuration.output6_configuration.input6_level = raw_mix[109]
    config.mixer2_crosspoint_configuration.output6_configuration.input7_level = raw_mix[110]
    config.mixer2_crosspoint_configuration.output6_configuration.input8_level = raw_mix[111]

    config.mixer2_crosspoint_configuration.output7_configuration.input1_level = raw_mix[112]
    config.mixer2_crosspoint_configuration.output7_configuration.input2_level = raw_mix[113]
    config.mixer2_crosspoint_configuration.output7_configuration.input3_level = raw_mix[114]
    config.mixer2_crosspoint_configuration.output7_configuration.input4_level = raw_mix[115]
    config.mixer2_crosspoint_configuration.output7_configuration.input5_level = raw_mix[116]
    config.mixer2_crosspoint_configuration.output7_configuration.input6_level = raw_mix[117]
    config.mixer2_crosspoint_configuration.output7_configuration.input7_level = raw_mix[118]
    config.mixer2_crosspoint_configuration.output7_configuration.input8_level = raw_mix[119]

    config.mixer2_crosspoint_configuration.output8_configuration.input1_level = raw_mix[120]
    config.mixer2_crosspoint_configuration.output8_configuration.input2_level = raw_mix[121]
    config.mixer2_crosspoint_configuration.output8_configuration.input3_level = raw_mix[122]
    config.mixer2_crosspoint_configuration.output8_configuration.input4_level = raw_mix[123]
    config.mixer2_crosspoint_configuration.output8_configuration.input5_level = raw_mix[124]
    config.mixer2_crosspoint_configuration.output8_configuration.input6_level = raw_mix[125]
    config.mixer2_crosspoint_configuration.output8_configuration.input7_level = raw_mix[126]
    config.mixer2_crosspoint_configuration.output8_configuration.input8_level = raw_mix[127]

    # virtual mix starts after raw
    def get_mix_virtual_configuration(mix_id: int) -> es9_py_pb2.MixConfiguration.MixVirtualConfiguration:
        offset = 128 * 3
        mix_config = es9_py_pb2.MixConfiguration.MixVirtualConfiguration()

        mix_config.vpan = data[offset + mix_id * 2 + 1]
        mix_config.vmix = data[offset + mix_id * 2 + 0]

        return mix_config

    config.mix1_vconf.CopyFrom(get_mix_virtual_configuration(0))
    config.mix2_vconf.CopyFrom(get_mix_virtual_configuration(1))
    config.mix3_vconf.CopyFrom(get_mix_virtual_configuration(2))
    config.mix4_vconf.CopyFrom(get_mix_virtual_configuration(3))
    config.mix5_vconf.CopyFrom(get_mix_virtual_configuration(4))
    config.mix6_vconf.CopyFrom(get_mix_virtual_configuration(5))
    config.mix7_vconf.CopyFrom(get_mix_virtual_configuration(6))
    config.mix8_vconf.CopyFrom(get_mix_virtual_configuration(7))
    config.mix9_vconf.CopyFrom(get_mix_virtual_configuration(8))
    config.mix10_vconf.CopyFrom(get_mix_virtual_configuration(9))
    config.mix11_vconf.CopyFrom(get_mix_virtual_configuration(10))
    config.mix12_vconf.CopyFrom(get_mix_virtual_configuration(11))
    config.mix13_vconf.CopyFrom(get_mix_virtual_configuration(12))
    config.mix14_vconf.CopyFrom(get_mix_virtual_configuration(13))
    config.mix15_vconf.CopyFrom(get_mix_virtual_configuration(14))
    config.mix16_vconf.CopyFrom(get_mix_virtual_configuration(15))

    return config

class Message:
    def __init__(self, msg_type: int, payload: bytes):
        self._msg_type = msg_type
        self._data = ES9_SYSEX_HEADER + bytes((msg_type,)) + bytes(payload)

    @property
    def msg_type(self) -> MessageType:
        return self._msg_type

    @property
    def data(self) -> bytes:
        return self._data

class ApplyConfigurationDumpMessage(Message):
    def __init__(self, chunk: int, data: bytes):
        payload = bytes(bytes((chunk,)) + data)
        super().__init__(MessageType.APPLY_CONFIGURATION_DUMP.value, payload)

class RequestVersionStringMessage(Message):
    def __init__(self):
        super().__init__(MessageType.REQUEST_VERSION_STRING.value, bytes())

class RequestConfigurationDumpMessage(Message):
    def __init__(self):
        super().__init__(MessageType.REQUEST_CONFIGURATION_DUMP.value, bytes())

class RequestSaveMessage(Message):
    class Slot(Enum):
        STANDALONE = 0
        HOSTED = 1
    
    def __init__(self, slot: Slot):
        super().__init__(MessageType.REQUEST_SAVE.value, bytes((slot.value,)))

class RequestRestoreMessage(Message):
    class Slot(Enum):
        STANDALONE = 0
        HOSTED = 1
    
    def __init__(self, slot: Slot):
        super().__init__(MessageType.REQUEST_RESTORE.value, bytes((slot.value,)))

class RequestResetMessage(Message):
    def __init__(self):
        super().__init__(MessageType.REQUEST_RESET.value, bytes())

class RequestMixMessage(Message):
    def __init__(self):
        super().__init__(MessageType.REQUEST_MIX.value, bytes())

class RequestUsageMessage(Message):
    def __init__(self):
        super().__init__(MessageType.REQUEST_USAGE.value, bytes())

class RequestSampleRateMessage(Message):
    def __init__(self):
        super().__init__(MessageType.REQUEST_SAMPLE_RATE.value, bytes())

class SetHighPassFiltersMessage(Message):
    def __init__(self, config: es9_py_pb2.Configuration.HighPassFilterConfiguration):
        hpf = 0
        if config.channel_pair_1_2_enabled:
            hpf |= 0x01
        if config.channel_pair_3_4_enabled:
            hpf |= 0x02
        if config.channel_pair_5_6_enabled:
            hpf |= 0x04
        if config.channel_pair_7_8_enabled:
            hpf |= 0x08
        if config.channel_pair_9_10_enabled:
            hpf |= 0x10
        if config.channel_pair_11_12_enabled:
            hpf |= 0x20
        if config.channel_pair_13_14_enabled:
            hpf |= 0x40

        super().__init__(MessageType.SET_HPF.value, bytes((hpf,)))

class SetOptionsMessage(Message):
    def __init__(self, config: es9_py_pb2.Configuration.OptionsConfiguration):
        options = 0
        if not config.use_spdif:
            options |= 0x01
        if config.use_midi_through:
            options |= 0x02
        
        super().__init__(MessageType.SET_OPTIONS.value, bytes((options,)))

class SetLinksMessage(Message):
    MAP_LINK_ID = {
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_1_2: 0x00,
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_3_4: 0x01,
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_5_6: 0x02,
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_7_8: 0x03,
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_9_10: 0x04,
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_11_12: 0x05,
        es9_py_pb2.MixerLink.MIXER_LINK_INPUT_13_14: 0x06,

        es9_py_pb2.MixerLink.MIXER_LINK_BUS_1_2: 0x08,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_3_4: 0x09,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_5_6: 0x0A,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_7_8: 0x0B,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_9_10: 0x0C,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_11_12: 0x0D,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_13_14: 0x0E,
        es9_py_pb2.MixerLink.MIXER_LINK_BUS_15_16: 0x0F,

        es9_py_pb2.MixerLink.MIXER_LINK_USB_1_2: 0x10,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_3_4: 0x11,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_5_6: 0x12,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_7_8: 0x13,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_9_10: 0x14,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_11_12: 0x15,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_13_14: 0x16,
        es9_py_pb2.MixerLink.MIXER_LINK_USB_15_16: 0x17,

        es9_py_pb2.MixerLink.MIXER_LINK_MIX_1_2: 0x18,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_3_4: 0x19,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_5_6: 0x1A,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_7_8: 0x1B,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_9_10: 0x1C,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_11_12: 0x1D,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_13_14: 0x1E,
        es9_py_pb2.MixerLink.MIXER_LINK_MIX_15_16: 0x1F,
    }

    def __init__(self, link: es9_py_pb2.MixerLink, enabled: bool):
        link_id = self.MAP_LINK_ID[link]
        state = 0x01 if enabled else 0x00
        super().__init__(MessageType.SET_LINKS.value, bytes((link_id, state))) 

class SetVirtualMixMessage(Message):
    def __init__(self, mix_id: int, level: int):
        """
        Set the virtual mix level for a given mix ID.
        Note: this feature is not well understood yet,
        and is relatively superfluous given the ability to
        directly set mix levels via SetMixMessage.
        """
        raise NotImplementedError("SetVirtualMixMessage not implemented yet")

class SetMidiChannelsMessage(Message):
    def __init__(self, usb_midi_channel: int, din_midi_channel: int):
        """
        Set the MIDI channels for USB and DIN MIDI inputs.
        0 = Off, 1-16 = MIDI channel number
        """
        assert 0 <= usb_midi_channel <= 16, "USB MIDI channel must be in range 0-16"
        assert 0 <= din_midi_channel <= 16, "DIN MIDI channel must be in range 0-16"
        super().__init__(MessageType.SET_MIDI_CHANNELS.value, bytes((usb_midi_channel, din_midi_channel)))

class SetDCOffsetMessage(Message):
    def __init__(self, channel: es9_py_pb2.Channel, offset: int):
        """
        Set the DC offset for a given channel.
        Offset is a signed 16-bit integer in the range -3176 to +3176.
        """
        assert isinstance(channel, es9_py_pb2.Channel), "channel must be an instance of Channel Enum"
        assert es9_channel_is_output(channel), "DC offset can only be set for output channels"
        assert -3176 <= offset <= 3176, "Offset must be in range -3176 to +3176"
        
        # weird encoding of offset into 3 bytes
        # (defined by ES9 firmware)
        offset_bytes = bytes((
            (offset >> 14) & 0x03,
            (offset >> 7) & 0x7F,
            offset & 0x7F,
        ))

        super().__init__(MessageType.SET_DC_OFFSET.value, bytes((channel.value,)) + offset_bytes)

class SetFilterMessage(Message):
    def __init__(self, mix_id: int, filter_instance: int, enable: bool, filter_type: es9_py_pb2.FilterType, frequency: int, q_factor: int, gain: int):
        """
        Configure a filter for a given mixer input.
        The Mix ID maps to the input channels of mixer 1 and mixer 2.
        Mixer 1: inputs 1-8 (Mix ID 0-7)
        Mixer 2: inputs 9-14 (Mix ID 8-15)
        """
        assert 0 <= mix_id <= 15, "Mix ID must be in range 0-15"
        assert 0 <= filter_instance <= 3, "Only 4 filter instances (0-3) per mix are supported"
        assert filter_type in es9_py_pb2.FilterType.values(), "Invalid filter type"

        # ES-9 firmware expects frequency, Q factor, and gain
        # to be encoded as 3 bytes each using this strange format
        # (defined by ES9 firmware)
        freq_bytes = bytes((
            (frequency >> 14) & 0x03,
            (frequency >> 7) & 0x7F,
            frequency & 0x7F,
        ))
        q_bytes = bytes((
            (q_factor >> 14) & 0x03,
            (q_factor >> 7) & 0x7F,
            q_factor & 0x7F,
        ))
        gain_bytes = bytes((
            (gain >> 14) & 0x03,
            (gain >> 7) & 0x7F,
            gain & 0x7F,
        ))

        payload = bytes((
            mix_id,
            filter_instance,
            filter_type << 1 | (0x01 if enable else 0x00),
        )) + freq_bytes + q_bytes + gain_bytes

        super().__init__(MessageType.SET_FILTER.value, payload)

class SetSmoothingMessage(Message):
    def __init__(self, mix_id: int, enabled: bool):
        """
        Enable or disable smoothing for a given mix ID.
        Mix ID 0-7 correspond to mixer 1 outputs 1-8,
        Mix ID 8-15 correspond to mixer 2 outputs 9-14.
        """
        assert 0 <= mix_id <= 15, "Mix ID must be in range 0-15"
        state = 0x01 if enabled else 0x00
        super().__init__(MessageType.SET_SMOOTHING.value, bytes((mix_id, state)))

class SetInputsMessage(Message):
    def __init__(self, dsp_block: int, routing: bytes):
        """
        Set the input routing for a given DSP block (0-3).
        Routing is a bytes object of length 8, each byte
        representing the source for each of the 8 inputs.
        
        The USB audio block represents dsp blocks 0 and 1,
        consuming 16 input channels in total.

        USB channels 1-8: dsp0 inputs 1-8
        USB channels 9-16: dsp1 inputs 1-8
        Mixer 1 inputs 1-8: dsp2 inputs 1-8
        Mixer 2 inputs 1-6: dsp3 inputs 1-6
        """
        assert 0 <= dsp_block <= 3, "DSP block must be in range 0-3"
        assert len(routing) == 8, "Routing must be 8 bytes long"
        super().__init__(MessageType.SET_INPUTS.value + dsp_block, routing)

class SetOutputsMessage(Message):
    def __init__(self, dsp_block: int, routing: bytes):
        """
        Set the output routing for a given DSP block (0-3).
        Routing is a bytes object of length 8, each byte
        representing the destination for each of the 8 outputs.
        
        The USB audio block represents dsp blocks 0 and 1,
        consuming 16 output channels in total.

        USB channels 1-8: dsp0 outputs 1-8
        USB channels 9-16: dsp1 outputs 1-8
        Mixer 1 outputs 1-8: dsp2 outputs 1-8
        Mixer 2 outputs 9-16: dsp3 outputs 1-8
        """
        assert 0 <= dsp_block <= 3, "DSP block must be in range 0-3"
        assert len(routing) == 8, "Routing must be 8 bytes long"
        super().__init__(MessageType.SET_OUTPUTS.value + dsp_block, routing)

class SetMixMessage(Message):
    def __init__(self, mix_id: int, input_id: int, level: int):
        """
        Set the mix level for a given mix ID and input ID.
        Mix ID 0-7 correspond to mixer 1 outputs 1-8,
        Mix ID 8-15 correspond to mixer 2 outputs 1-8.
        Input ID corresponds to the input channel number (0-7).
        Level is in the range [0, 32768].
        """
        assert 0 <= mix_id <= 15, "Mix ID must be in range 0-15"
        assert 0 <= input_id <= 7, "Input ID must be in range 0-7"
        assert 0 <= level <= 32768, "Level must be in range 0-32768"

        level_bytes = bytes((
            (level >> 14),
            (level >> 7) & 0x7F,
            level & 0x7F,
        ))

        payload = bytes((input_id,)) + level_bytes

        super().__init__(MessageType.SET_MIX.value + mix_id, payload)

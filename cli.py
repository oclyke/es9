import asyncio
import mido
import click

from datetime import datetime

from interface import (
    ES9_SYSEX_HEADER,
    MessageType,

    SetHighPassFiltersMessage,
    SetLinksMessage,

    es9_parse_configuration_dump,
    es9_parse_mix_dump,
    es9_parse_message_report,

    es9_py_pb2,
)

def sniff_sysex(port_name: str):
    print(f"Opening MIDI input: {port_name}")
    print("Waiting for SysEx messages... (Ctrl+C to quit)\n")

    with mido.open_input(port_name) as inport:
        for msg in inport:
            if msg.type == 'sysex':
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                data_hex = " ".join(f"{b:02X}" for b in msg.data)
                data_dec = " ".join(str(b) for b in msg.data)

                print(f"[{timestamp}] SysEx received")
                print(f"  Length : {len(msg.data)} bytes")
                print(f"  Hex    : {data_hex}")
                print(f"  Dec    : {data_dec}")
                print()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--port', type=str, required=True, help='MIDI input port name to listen on')
def serve(
    port: str
):
    def blocking_poll_configuration():
        with mido.open_input(port) as rx:
            for msg in rx:
                if msg.type == 'sysex':

                    data = bytes(msg.data)
                    if not data.startswith(ES9_SYSEX_HEADER):
                        continue

                    message_type = data[4]
                    payload = data[5:-1]  # Exclude header and F7

                    match message_type:
                        case MessageType.REPORT_MESSAGE.value:
                            message = es9_parse_message_report(payload)
                            print(f"Received message: {message}")

                        case MessageType.REPORT_CONFIGURATION_DUMP.value:
                            config = es9_parse_configuration_dump(payload)
                            print("Received Configuration Dump:")
                            print(config)

                        case MessageType.REPORT_MIX.value:
                            mix_config = es9_parse_mix_dump(payload)
                            print("Received Mix Configuration Dump:")
                            print(mix_config)


    async def coro_poll_configuration():
        # Offload blocking MIDI receive loop
        await asyncio.to_thread(blocking_poll_configuration)

    async def coro_toggle_mix_level():
        pass

        while True:
            await asyncio.sleep(1)

        # with mido.open_output(port) as tx:
        #     mix_id = 0  # Mixer 1 Output 1
        #     input_id = 0  # Input 1
        #     level_on = 16384  # Mid-level
        #     level_off = 0     # Muted

        #     while True:
        #         # Set mix level to mid-level
        #         msg_on = SetMixMessage(mix_id, input_id, level_on)
        #         tx.send(mido.Message('sysex', data=msg_on.data[1:-1]))
        #         print(f"Sent SetMixMessage to set mix {mix_id} input {input_id} to level {level_on}")
        #         await asyncio.sleep(2)

        #         # Set mix level to muted
        #         msg_off = SetMixMessage(mix_id, input_id, level_off)
        #         tx.send(mido.Message('sysex', data=msg_off.data[1:-1]))
        #         print(f"Sent SetMixMessage to set mix {mix_id} input {input_id} to level {level_off}")
        #         await asyncio.sleep(2)

    async def main():
        poll_task = asyncio.create_task(coro_poll_configuration())
        toggle_task = asyncio.create_task(coro_toggle_mix_level())
        await asyncio.gather(poll_task, toggle_task)
    
    asyncio.run(main())


@cli.command()
@click.argument('mask', type=str)
def hpf(
    mask: str
):
    """Set high-pass filter configuration based on a bitmask."""
    mask = int(mask, 0) # Convert string to integer (supports hex with 0x prefix)

    config = es9_py_pb2.Configuration.HighPassFilterConfiguration(
        channel_pair_1_2_enabled=bool(mask & 0x01),
        channel_pair_3_4_enabled=bool(mask & 0x02),
        channel_pair_5_6_enabled=bool(mask & 0x04),
        channel_pair_7_8_enabled=bool(mask & 0x08),
        channel_pair_9_10_enabled=bool(mask & 0x10),
        channel_pair_11_12_enabled=bool(mask & 0x20),
        channel_pair_13_14_enabled=bool(mask & 0x40),
    )
    msg = SetHighPassFiltersMessage(config)
    print("Constructed SetHighPassFiltersMessage:")
    print("  Data (hex):", " ".join(f"{b:02X}" for b in msg.data))

@cli.command()
@click.option('--enable', multiple=True, type=click.Choice([
    'input_1_2', 'input_3_4', 'input_5_6', 'input_7_8',
    'input_9_10', 'input_11_12', 'input_13_14',
    'bus_1_2', 'bus_3_4', 'bus_5_6', 'bus_7_8',
    'bus_9_10', 'bus_11_12', 'bus_13_14', 'bus_15_16',
    'usb_1_2', 'usb_3_4', 'usb_5_6', 'usb_7_8',
    'usb_9_10', 'usb_11_12', 'usb_13_14', 'usb_15_16',
    'mix_1_2', 'mix_3_4', 'mix_5_6', 'mix_7_8',
    'mix_9_10', 'mix_11_12',  'mix_13_14', 'mix_15_16',
]))
def links(
    enable
):
    """Set mixer link configuration."""
    link_map = {
        'input_1_2': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_1_2,
        'input_3_4': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_3_4,
        'input_5_6': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_5_6,
        'input_7_8': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_7_8,
        'input_9_10': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_9_10,
        'input_11_12': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_11_12,
        'input_13_14': es9_py_pb2.MixerLink.MIXER_LINK_INPUT_13_14,
        'bus_1_2': es9_py_pb2.MixerLink.MIXER_LINK_BUS_1_2,
        'bus_3_4': es9_py_pb2.MixerLink.MIXER_LINK_BUS_3_4,
        'bus_5_6': es9_py_pb2.MixerLink.MIXER_LINK_BUS_5_6,
        'bus_7_8': es9_py_pb2.MixerLink.MIXER_LINK_BUS_7_8,
        'bus_9_10': es9_py_pb2.MixerLink.MIXER_LINK_BUS_9_10,
        'bus_11_12': es9_py_pb2.MixerLink.MIXER_LINK_BUS_11_12,
        'bus_13_14': es9_py_pb2.MixerLink.MIXER_LINK_BUS_13_14,
        'bus_15_16': es9_py_pb2.MixerLink.MIXER_LINK_BUS_15_16,
        'usb_1_2': es9_py_pb2.MixerLink.MIXER_LINK_USB_1_2,
        'usb_3_4': es9_py_pb2.MixerLink.MIXER_LINK_USB_3_4,
        'usb_5_6': es9_py_pb2.MixerLink.MIXER_LINK_USB_5_6,
        'usb_7_8': es9_py_pb2.MixerLink.MIXER_LINK_USB_7_8,
        'usb_9_10': es9_py_pb2.MixerLink.MIXER_LINK_USB_9_10,
        'usb_11_12': es9_py_pb2.MixerLink.MIXER_LINK_USB_11_12,
        'usb_13_14': es9_py_pb2.MixerLink.MIXER_LINK_USB_13_14,
        'usb_15_16': es9_py_pb2.MixerLink.MIXER_LINK_USB_15_16,
        'mix_1_2': es9_py_pb2.MixerLink.MIXER_LINK_MIX_1_2,
        'mix_3_4': es9_py_pb2.MixerLink.MIXER_LINK_MIX_3_4,
        'mix_5_6': es9_py_pb2.MixerLink.MIXER_LINK_MIX_5_6,
        'mix_7_8': es9_py_pb2.MixerLink.MIXER_LINK_MIX_7_8,
        'mix_9_10': es9_py_pb2.MixerLink.MIXER_LINK_MIX_9_10,
        'mix_11_12': es9_py_pb2.MixerLink.MIXER_LINK_MIX_11_12,
        'mix_13_14': es9_py_pb2.MixerLink.MIXER_LINK_MIX_13_14,
        'mix_15_16': es9_py_pb2.MixerLink.MIXER_LINK_MIX_15_16,
    }
    for link_name, link_enum in link_map.items():
        enabled = link_name in enable
        msg = SetLinksMessage(link_enum, enabled)
        print(f"Constructed SetLinksMessage for {link_name} (enabled={enabled}):")
        print("  Data (hex):", " ".join(f"{b:02X}" for b in msg.data)
)
        


if __name__ == "__main__":
    cli()

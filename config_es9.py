import asyncio
import mido
import click

from loguru import logger

from datetime import datetime

from interface import (
    ES9_SYSEX_HEADER,
    MessageType,

    SetHighPassFiltersMessage,
    SetLinksMessage,
    RequestConfigurationDumpMessage,
    SetMixMessage,
    SetInputsMessage,
    SetFilterMessage,
    SetOptionsMessage,
    SetMidiChannelsMessage,
    SetLinksMessage,

    es9_parse_configuration_dump,
    es9_parse_mix_dump,
    es9_parse_message_report,
    es9_channel_to_input_route_id,

    es9_py_pb2,
)

def send_msg(
    output: mido.ports.BaseOutput,
    msg,
):
    logger.trace(f"Sending SysEx message: {' '.join(f'{b:02X}' for b in msg.data)}")
    output.send(mido.Message('sysex', data=msg.data))

@click.command()
@click.option('--outport', type=str, required=True, help='MIDI output port name to send to', default='ES-9 MIDI Out')
@click.option('--inport', type=str, required=True, help='MIDI input port name to listen on', default='ES-9 MIDI In')
@click.option('--timeout', type=float, default=1.0, help='Timeout in seconds to wait for responses')
def configure(
  outport: str,
  inport: str,
  timeout: float,
):
    async def run():
        print(f"Opening MIDI output: {outport}")
        with mido.open_output(outport) as portout, mido.open_input(inport) as portin:

            msg = SetMixMessage(mix_id=2, input_id=0, level=0)
            send_msg(portout, msg)

            msg = SetMixMessage(mix_id=3, input_id=0, level=0)
            send_msg(portout, msg)
            msg =  SetMixMessage(mix_id=3, input_id=0, level=0)
            send_msg(portout, msg)

            msg = SetLinksMessage(link=es9_py_pb2.MixerLink.MIXER_LINK_INPUT_1_2, enabled=True)
            send_msg(portout, msg)

            # request configuration dump to get current state (for modification)
            msg = RequestConfigurationDumpMessage()
            send_msg(portout, msg)
            print("Requested configuration dump")
            # wait for and process incoming messages
            config = None
            while True:
                msg = portin.receive()
                if msg.type == 'sysex':
                    data = bytes(msg.data)
                    if not data.startswith(ES9_SYSEX_HEADER):
                        continue

                    message_type = data[4]
                    payload = data[5:-1]  # Exclude header and F7

                    if message_type == MessageType.REPORT_CONFIGURATION_DUMP.value:
                        config = es9_parse_configuration_dump(payload)
                        print("Received configuration dump")

                        break

            # Now, with the updated input routing, we can make a granular adjustment
            # Let's change mixer1 input1 to use Input 1
            # and mixer1 input5 to use Bus 4
            print(f"mnixer1 input1 channel:", es9_py_pb2.Channel.Name(config.mixer1_routing_configuration.input1_channel))
            msg = SetInputsMessage(
                dsp_block=2,
                routing=bytes([
                    es9_channel_to_input_route_id(es9_py_pb2.Channel.CHANNEL_INPUT_1), # Specify Input 1
                    es9_channel_to_input_route_id(config.mixer1_routing_configuration.input2_channel),
                    es9_channel_to_input_route_id(config.mixer1_routing_configuration.input3_channel),
                    es9_channel_to_input_route_id(config.mixer1_routing_configuration.input4_channel),
                    es9_channel_to_input_route_id(es9_py_pb2.Channel.CHANNEL_BUS_4), # Specify Bus 4
                    es9_channel_to_input_route_id(config.mixer1_routing_configuration.input6_channel),
                    es9_channel_to_input_route_id(config.mixer1_routing_configuration.input7_channel),
                    es9_channel_to_input_route_id(config.mixer1_routing_configuration.input8_channel),
                ])
            )
            send_msg(portout, msg)
            print("Updated input routing to use Input 1 and Bus 4")


            # Now let's modify the USB block inputs and outputs
            msg = SetInputsMessage(
                dsp_block=0,
                routing=bytes([
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input1_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input2_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input3_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input4_channel),
                    es9_channel_to_input_route_id(es9_py_pb2.Channel.CHANNEL_INPUT_1), # Specify Input 1
                    es9_channel_to_input_route_id(es9_py_pb2.Channel.CHANNEL_INPUT_2), # Specify Input 2
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input7_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input8_channel),
                ])
            )
            send_msg(portout, msg)
            print("Updated USB input routing to use Input 5 and Input 6")

            msg = SetInputsMessage(
                dsp_block=1,
                routing=bytes([
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input1_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input2_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input3_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input4_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input5_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input6_channel),
                    es9_channel_to_input_route_id(config.usb_routing_configuration.input7_channel),
                    es9_channel_to_input_route_id(es9_py_pb2.Channel.CHANNEL_BUS_15), # Specify Bus 15
                ])
            )
            send_msg(portout, msg)
            print("Updated USB output routing to use Bus 15")

            ## Now let's configure a filter
            msg = SetFilterMessage(
                mix_id=3,
                enable=True,
                filter_instance=1,
                filter_type=es9_py_pb2.FilterType.LOW_PASS_1ST_ORDER,
                frequency=1000,
                q_factor=100,
                gain=0,
            )
            send_msg(portout, msg)
            print("Configured filter on mixer 2 input 1")

            ## Configure some DC blocking filters
            msg = SetHighPassFiltersMessage(config=es9_py_pb2.Configuration.HighPassFilterConfiguration(
                channel_pair_1_2_enabled=True,
                channel_pair_3_4_enabled=False,
                channel_pair_5_6_enabled=True,
                channel_pair_7_8_enabled=True,
                channel_pair_9_10_enabled=True,
                channel_pair_11_12_enabled=False,
                channel_pair_13_14_enabled=False,
            ))
            send_msg(portout, msg)
            print("Configured DC blocking filters")

            # Configure the options
            msg = SetOptionsMessage(
                config=es9_py_pb2.Configuration.OptionsConfiguration(
                    use_spdif=False,
                    use_midi_through=True,
                )
            )
            send_msg(portout, msg)
            print("Configured options")

            # Configure MIDI channels
            msg = SetMidiChannelsMessage(
                usb_midi_channel=12,
                din_midi_channel=0,
            )
            send_msg(portout, msg)
            print("Configured MIDI channels")

            # Set up a link 
            msg = SetLinksMessage(
                link=es9_py_pb2.MixerLink.MIXER_LINK_INPUT_5_6,
                enabled=True,
            )
            send_msg(portout, msg)
            print("Configured mixer link for inputs 5 and 6")

            # Request configuration dump to show final state
            msg = RequestConfigurationDumpMessage()
            send_msg(portout, msg)

    asyncio.run(run())

if __name__ == '__main__':
    configure()

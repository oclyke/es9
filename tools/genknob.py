#! /usr/bin/env python3

"""
file: genknob.py
description: generate an svg representing a synthesizer knob.
"""

import click
import os
import math

from enum import Enum
from loguru import logger

class KnownException(Exception):
  class Severity(Enum):
    CRITICAL = 1
    ERROR = 2
    WARNING = 3

  def __init__(self, message: str, help: str):
    super().__init__(message)
    self.help = help
    self.message = message

@click.command()
@click.option('--output', '-o', type=click.Path(exists=False), required=True, help='Output SVG file path')
@click.option('--knurls', '-k', type=int, default=5, help='Number of knurls on the knob')
@click.option('--knurl-depth', '-d', type=float, default=0.1, help='Depth of the knurls as a fraction of the knob radius')
@click.option('--knob-duty-cycle', '-D', type=float, default=0.7, help='Duty cycle of the knob knurls (fraction of knurl occupied by raised area)')
@click.option('--center-radius', '-c', type=float, default=0.8, help='Radius of the center circle as a fraction of the knob radius')
def cli(
  output: str,
  knurls: int,
  knurl_depth: float,
  knob_duty_cycle: float,
  center_radius: float,
):
  if not os.path.exists(os.path.dirname(output)):
    raise KnownException(
        message=f"Output directory does not exist: {os.path.dirname(output)}",
        help=f"""
    cwd: {os.getcwd()}
    output: {output}
    {'The output path is not absolute. Please consider using an absolute path to avoid unexpected behavior.' if not os.path.isabs(output) else ''}
    """,
    )

  with open(output, 'w') as f:
    f.write("""<svg width="200" height="200" viewBox="-100 -100 200 200" xmlns="http://www.w3.org/2000/svg">""")

    # Center circle
    # ID: knob-center
    f.write(f"""<circle id="knob-center" cx="0" cy="0" r="{100 * center_radius}" fill="#CCCCCC"/>""")

    # Knurls
    # Knurls go from the outside of the knob to a fraction of the radius inward
    # Generated in 2x the number of knurls so that odd ones are centered at "top dead center"
    # Using path: "A rx ry x-axis-rotation large-arc-flag sweep-flag x y"
    for i in range(2*knurls):
      arc = math.pi / knurls
      angle = i * arc

      def arc(center, radius: float, arc: float, offset: float):
        """
        center: (x, y)
        radius: radius of the arc
        arc: angle of the arc in radians
        offset: angle offset in radians
        """
        f.write(f"""<path d="M {(center[0] + radius * math.sin(offset)):.2f} """)
        f.write(f"""{(center[1] - radius * math.cos(offset)):.2f} """)
        f.write(f"""A {radius:.2f} {radius:.2f} 0 0 1 """)
        f.write(f"""{(center[0] + radius * math.sin(offset + arc)):.2f} """)
        f.write(f"""{(center[1] - radius * math.cos(offset + arc)):.2f} """)
        f.write(f"""" fill="none" stroke="black" stroke-width="2"/>""")
        

      # outside segments (left and right)
      span = (math.pi / (2 * knurls))
      span_outside = span * knob_duty_cycle
      span_inside = span - span_outside
      arc(
        center=(0,0),
        radius=100,
        arc=span_outside,
        offset=angle,
      )
      arc(
        center=(0,0),
        radius=100,
        arc=span_outside,
        offset=angle - span_outside,
      )
      # inside segment)
      arc(
        center=(0,0),
        radius=100 * (1 - knurl_depth),
        arc=2 * span_inside,
        offset=angle + span - span_inside,
      )
      # connecting lines from outside to inside
      x1_out = 100 * math.sin(angle)
      y1_out = -100 * math.cos(angle)
      x1_in = 100 * (1 - knurl_depth) * math.sin(angle)
      y1_in = -100 * (1 - knurl_depth) * math.cos(angle)
      f.write(f"""<line x1="{x1_out:.2f}" y1="{y1_out:.2f}" x2="{x1_in:.2f}" y2="{y1_in:.2f}" stroke="#000000" stroke-width="2"/>""")

    # Indicator line
    # ID: knob-indicator
    f.write("""<line id="knob-indicator" x1="50" y1="50" x2="50" y2="10" stroke="#000000" stroke-width="5" stroke-linecap="round"/>""")
    f.write("</svg>\n")

if __name__ == "__main__":
  try:
    cli()
  except KnownException as e:
    logger.error(f"{e.message}")
    logger.info(f"{e.help}")
    exit(1)

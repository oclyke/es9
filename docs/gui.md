# es-9 configurator gui

Tool for configuring the es-9 mixer via WebMIDI.

# development

For the sake of speed this project relies on CDN-hosted tooling.

* React: event based state management and rendering engine
* Babel: JSX transpilation in the browser
* Protobuf.js: binary serialization for ES-9 state (to help make code more readable, mostly)

Future work could include setting up a proper build system with bundling and transpilation,
but for now this is sufficient.

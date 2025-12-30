const {
  useState,
  useEffect,
  useRef,
} = React;

const COLORS = {
  violet: "#9900ff",
  lavender: "#aa33ff",
  purple: "#cc00ff",
  amethyst: "#dd33ff",
  orchid: "#bb66ff",

  shocking_pink: "#ff00cc",
  vivid_pink: "#ff00aa",
  hot_pink: "#ff33ff",
  fuchsia: "#ff66ff",
  rose: "#ff0099",
  carnation: "#ff3399",
  bubblegum: "#ff66cc",
  electric_pink: "#ff1aff",
  neon_pink: "#ff4dff",
  flamingo: "#ff33cc",
  orchid_pink: "#ff66ff",

  red: "#ff4d4d",
  pink: "#ff3399",
  deep_pink: "#ff0066",
  coral: "#ff3366",
  magenta: "#ff1aff",

  light_orange: "#ff9933",
  amber: "#ff8800",
  orange: "#ff6600",
  pumpkin: "#ff5500",
  dark_orange: "#ff7700",

  yellow: "#ffff00",
  sunflower: "#fff700",
  bright_yellow: "#fffa00",
  golden_yellow: "#ffee00",
  daffodil: "#ffef33",

  turquoise: "#33ffff",
  aqua: "#00ffff",
  cyan: "#00f0ff",
  electric_blue: "#00d4ff",
  light_blue: "#66ccff",
  sky_blue: "#00ccff",
  deep_sky_blue: "#00bfff",
  dodger_blue: "#00aaff",
  cornflower_blue: "#3399ff",
  azure: "#3399ff",
  royal_blue: "#3366ff",

  mint: "#00ffee",
  teal: "#00ddcc",
  sea_green: "#00ccaa",
  aquamarine: "#00ffaa",
  medium_turquoise: "#33ffcc",
  turquoise: "#33ffee",
  light_sea_green: "#66ffdd",
};

/**
 * Blend two hex colors.
 * @param {string} color1 - First hex color, e.g. "#ff0000"
 * @param {string} color2 - Second hex color, e.g. "#0000ff"
 * @param {number} ratio - Blend ratio between 0 and 1 (0 = all color1, 1 = all color2)
 * @returns {string} Blended hex color
 */
function blendHexColors(color1, color2, ratio = 0.5) {
  // Remove the '#' if present
  color1 = color1.replace('#', '');
  color2 = color2.replace('#', '');
  
  // Parse the colors to integers
  const r1 = parseInt(color1.substring(0, 2), 16);
  const g1 = parseInt(color1.substring(2, 4), 16);
  const b1 = parseInt(color1.substring(4, 6), 16);
  
  const r2 = parseInt(color2.substring(0, 2), 16);
  const g2 = parseInt(color2.substring(2, 4), 16);
  const b2 = parseInt(color2.substring(4, 6), 16);
  
  // Blend each channel
  const r = Math.round(r1 + (r2 - r1) * ratio);
  const g = Math.round(g1 + (g2 - g1) * ratio);
  const b = Math.round(b1 + (b2 - b1) * ratio);
  
  // Convert back to hex and return
  const toHex = (c) => c.toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

/**
 * Generate a stacked neon text-shadow string from a base color
 * @param {string} color - The base color (hex, rgb, etc.)
 * @param {number} layers - How many shadow layers
 * @param {number} blurStep - How much to increase the blur per layer
 * @returns {string} - CSS text-shadow value
 */
function neonTextShadow(color, layers = 4, blurStep = 5) {
  const shadows = [];

  for (let i = 1; i <= layers; i++) {
    const blur = i * blurStep;
    shadows.push(`0 0 ${blur}px ${color}`);
  }

  return shadows.join(", ");
}


function Knob({
  value,
  onChange,
  min = 0,
  max = 1,
  step = null,
  left = -150,
  right = 150,
  size = 40,
  highlight = false,
  light = 'fade', // 'fade' | 'on' | 'off'
  lightColor = "#00f0ff",
  style = {},
}) {
  const defaultTransitionIn = "stroke-opacity 0.1s ease"; // fade-in default
  const defaultTransitionOut = "stroke-opacity 5s ease"; // fade-out default

  const knobRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [glowOpacity, setGlowOpacity] = useState(light === 'on' ? 1 : 0);
  const [transition, setTransition] = useState(defaultTransitionIn); // fade-in default

  const valueToAngle = (val) => left + ((right - left) * (val - min)) / (max - min);

  // --- Mouse dragging logic ---
  const handleMouseMove = (e) => {
    if (!isDragging) return;
    const sensitivity = { x: 1 / 200, y: 1 / 500 };
    const rect = knobRef.current.getBoundingClientRect();
    const centerY = rect.top + rect.height / 2;
    const centerX = rect.left + rect.width / 2;
    const deltaY = centerY - e.clientY;
    const deltaX = e.clientX - centerX;
    let newValue = value + deltaY * sensitivity.y * Math.exp(deltaX * sensitivity.x);
    newValue = Math.min(Math.max(newValue, min), max);
    if (step !== null) newValue = Math.round(newValue / step) * step;
    onChange(newValue);
  };

  const handleMouseUp = () => setIsDragging(false);

  useEffect(() => {
    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
      if (light === 'fade') {
        setTransition(defaultTransitionIn);
        setGlowOpacity(1);
      }
    } else {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      if (light === 'fade') {
        setTransition(defaultTransitionOut);
        setGlowOpacity(0.5);
      }
    }
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging]);

  const angle = valueToAngle(value);

  // --- SVG arc calculation ---
  const radius = size / 2 - 4;
  const startAngle = (left - 90) * (Math.PI / 180);
  const endAngle = (angle - 90) * (Math.PI / 180);
  const startX = size / 2 + radius * Math.cos(startAngle);
  const startY = size / 2 + radius * Math.sin(startAngle);
  const endX = size / 2 + radius * Math.cos(endAngle);
  const endY = size / 2 + radius * Math.sin(endAngle);
  const largeArcFlag = endAngle - startAngle <= Math.PI ? "0" : "1";
  const pathData = `M ${startX} ${startY} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endX} ${endY}`;

  // --- Mouse enter/leave for hover fade ---
  const handleMouseEnter = () => {
    if (light === 'fade') {
      setTransition(defaultTransitionIn); // quick fade-in
      setGlowOpacity(1);
    }
  };
  const handleMouseLeave = () => {
    if (light === 'fade' && !isDragging) {
      setTransition(defaultTransitionOut); // slow fade-out
      setGlowOpacity(0.5);
    }
  };

  let finalGlowOpacity = 0;
  let finalTransition = defaultTransitionOut;
  if (light === 'on') {
    finalGlowOpacity = 1;
    finalTransition = defaultTransitionIn;
  } else if (light === 'off') {
    finalGlowOpacity = 0.5;
    finalTransition = defaultTransitionIn;
  } else if (light === 'fade') {
    finalGlowOpacity = glowOpacity;
    finalTransition = transition;

    if (highlight) {
      finalGlowOpacity = 1;
      finalTransition = defaultTransitionIn;
    }
  }

  return (
    <div
      ref={knobRef}
      onMouseDown={() => setIsDragging(true)}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{
        width: size,
        height: size,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        cursor: "pointer",
        userSelect: "none",
        position: "relative",
        ...style,
      }}
    >
      {/* Neon Glow Value Indicator */}
      <svg
        width="100%"
        height="100%"
        viewBox={`0 0 ${size} ${size}`}
        style={{ position: "absolute", top: 0, left: 0, overflow: "visible" }}
      >
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        <path
          d={pathData}
          stroke={lightColor}
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          filter="url(#glow)"
          style={{
            transition: finalTransition,
            strokeOpacity: finalGlowOpacity,
          }}
        />
      </svg>

      <img
        src="./assets/knob.svg"
        alt="Knob"
        draggable={false}
        style={{
          width: "60%",
          height: "60%",
          transform: `rotate(${angle}deg)`,
          transformOrigin: "50% 50%",
          position: "absolute",
        }}
      />
    </div>
  );
}



function Mixer(props) {
  const dimInput = 8;
  const dimOutput = 8;
  const knobSize = 40;

  const [matrix, setMatrix] = useState(
    Array.from({ length: dimInput }, () =>
      Array.from({ length: dimOutput }, () => 0.0)
    )
  );
  const [highlightRow, setHighlightRow] = useState(null);
  const [highlightCol, setHighlightCol] = useState(null);

  const palettes = {
    mixer1: {
      inputs: [
        COLORS.violet,
        COLORS.lavender,
        COLORS.amethyst,
        COLORS.purple,
        COLORS.orchid,
        COLORS.hot_pink,
        COLORS.shocking_pink,
        COLORS.vivid_pink,
      ],
      outputs: [
        COLORS.red,
        COLORS.pumpkin,
        COLORS.orange,
        COLORS.dark_orange,
        COLORS.amber,
        COLORS.light_orange,
        COLORS.yellow,
        COLORS.sunflower,
      ],
    },
    mixer2: {
      inputs: [
        COLORS.sea_green,
        COLORS.teal,
        COLORS.mint,
        COLORS.medium_turquoise,
        COLORS.turquoise,
        COLORS.light_sea_green,
        COLORS.aqua,
        COLORS.turquoise,
      ],
      outputs: [
        COLORS.light_blue,
        COLORS.electric_blue,
        COLORS.sky_blue,
        COLORS.deep_sky_blue,
        COLORS.dodger_blue,
        COLORS.cornflower_blue,
        COLORS.azure,
        COLORS.royal_blue,
      ],
    },
  };

  const range = (size) => Array.from({ length: size }, (_, i) => i);
  const cartesianProduct = (arrays) => arrays.reduce((a, b) => a.flatMap(d => b.map(e => [...d, e])), [[]]);

  return <div>
    <div
      id="panel"
      style={{
        backgroundColor: "#2a2a2aff",
        padding: "20px",
        fontWeight: "bold",
      }}
      >

      {/* Mixer Title */}
      <h2
        className="monoton-regular"
        style={{
          textTransform: "uppercase",
          color: "#e8e8e8ff",
        }}
      >
        Mixer {props.id}
      </h2>

      {/* Lighting control area */}
      <div id="lighting-control-area">
        
      </div>

      <div style={{ display: "flex", flexDirection: "row"}}>
        <div style={{ display: "flex", flexDirection: "column"}}>

          {/* Input Labels */}
          <div
            id="inputs"
            style={{ display: "grid", gridTemplateColumns: `repeat(${dimInput}, ${knobSize}px)`, gap: "5px", padding: "5px" }}
          >
            {range(dimInput).map((input) => {
              
              const color = palettes["mixer" + props.id].inputs[input];
              const shadow = neonTextShadow(color, 1, 5);
              
              return (
              
              <div key={"input-label-" + input}
                onMouseEnter={() => {
                  setHighlightRow(input);
                }}
                onMouseLeave={() => {
                  setHighlightRow(null);
                }}
                >

                <div
                  className="orbitron-heavy"
                  style={{
                    gridColumn: input + 1,
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    color: color,
                    textShadow: shadow,
                    fontWeight: "bold",
                    rotate: "-60deg",
                  }}
                >
                  in:{input + 1}
                </div>
              </div>
            )})}
          </div>

          {/* Crosspoint Matrix Knobs */}
          <div
            id="crosspoint-matrix"
            style={{
              display: "grid",
              gridTemplateColumns: `repeat(${dimOutput}, ${knobSize}px)`,
              gridTemplateRows: `repeat(${dimInput}, ${knobSize}px)`,
              gap: "5px",
              padding: "5px",
              backgroundColor: "#2a2a2aff",
            }}
          >
            {cartesianProduct([range(dimInput), range(dimOutput)]).map(([input, output]) => (
              <div key={"knob-" + input + "-" + output}
                style={{
                  gridColumn: input + 1,
                  gridRow: output + 1,
                  display: "grid",
                }}
              >
                <Knob
                  value={matrix[input][output]}
                  size={knobSize}
                  highlight={highlightRow === input || highlightCol === output}
                  light="fade"
                  lightColor={blendHexColors(
                    palettes["mixer" + props.id].inputs[input],
                    palettes["mixer" + props.id].outputs[output],
                    0.5
                  )}
                  onChange={(val) => {
                    console.log(`Mixer ${props.id} - Input ${input} to Output ${output} set to ${val.toFixed(2)}`);
                    setMatrix((prev) => {
                      const newMatrix = prev.map(row => row.slice());
                      newMatrix[input][output] = val;
                      return newMatrix;
                    });
                  }}
                />
              </div>
            ))
            }
          </div>

        </div>

        {/* Output Labels */}
        <div style={{ display: "flex", flexDirection: "column",  justifyContent: "end" }}>
          <div
            id="outputs"
            style={{
              display: "grid",
              gridTemplateRows: `repeat(${dimOutput}, ${knobSize}px)`,
              gap: "5px",
              padding: "5px",
              marginTop: "5px",
            }}
          >
            {range(dimOutput).map((output, index) => {

              const color = palettes["mixer" + props.id].outputs[output];
              const shadow = neonTextShadow(color, 1, 5);
              return (
              <div
                key={"output-label-" + output}
                onMouseEnter={() => {
                  setHighlightCol(output);
                }}
                onMouseLeave={() => {
                  setHighlightCol(null);
                }}
                >

                <div
                    className="orbitron-heavy"
                    style={{
                      gridRow: index + 1, // note: use the index here
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      color: color,
                      textShadow: shadow,
                      fontWeight: "bold",
                      rotate: "30deg",
                    }}
                >
                  out:{output + 1}
                </div>
              </div>
            )})}
          </div>
        </div>
      </div>
    </div>
  </div>;
}

function App() {
  const [state, setState] = useState({});
  const [message, setMessage] = useState(null);

  useEffect(() => {
    protobuf.load("./proto/es9.proto").then(root => {

      console.log("Proto loaded");

      const Usage = root.lookupType("dev.oclyke.external.expert_sleepers.es9.v1.Usage");
      console.log("Usage expected fields:", Usage.fields);

      const payload = {
        usageDsp0: 0.5,
        usageDsp1: 0.75,
        usage_dsp2: 0.25,
        usage_dsp3: 0.9,
      };
      const err = Usage.verify(payload);
      if (err) throw Error(err);

      const msg = Usage.create(payload);
      const buffer = Usage.encode(msg).finish();
      const decoded = Usage.decode(buffer);

      console.log("Decoded message:", decoded);

      setMessage(decoded);
    })
    .catch(err => {
      console.error("Error loading proto:", err);
    });
  }, []);

  return <>
    <div>
      <h1>ES-9 Configuration Tool</h1>
    </div>

    <div id="mixer1">
      <Mixer id={1} />
    </div>
    <div id="mixer2">
      <Mixer id={2} />
    </div>
  </>
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

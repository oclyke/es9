const {
  useState,
  useEffect,
  useRef,
} = React;

function Knob({
  value,
  onChange,
  min = 0,
  max = 1,
  step = null,
  left = -150,
  right = 150,
  size = 30,
  style = {},
}) {
  const knobRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const valueToAngle = (val) => left + ((right - left) * (val - min)) / (max - min);

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    const sensitivity = {
      x: 1 / 200,
      y: 1 / 500,
    }

    const rect = knobRef.current.getBoundingClientRect();
    const centerY = rect.top + rect.height / 2;
    const centerX = rect.left + rect.width / 2;
    const deltaY = centerY - e.clientY;
    const deltaX = e.clientX - centerX;

    let newValue = value + deltaY * sensitivity.y * Math.exp(deltaX * sensitivity.x);
    newValue = Math.min(Math.max(newValue, min), max);

    // Snap to step
    if (step !== null) {
      newValue = Math.round(newValue / step) * step;
    }
    onChange(newValue);
  };

  const handleMouseUp = () => setIsDragging(false);

  useEffect(() => {
    if (isDragging) {
      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    } else {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    }
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isDragging]);

  const angle = valueToAngle(value);

  // SVG arc calculation
  const radius = size / 2 - 4; // leave padding
  const startAngle = (left - 90) * (Math.PI / 180); // rotate to top-left
  const endAngle = (angle - 90) * (Math.PI / 180);

  const startX = size / 2 + radius * Math.cos(startAngle);
  const startY = size / 2 + radius * Math.sin(startAngle);
  const endX = size / 2 + radius * Math.cos(endAngle);
  const endY = size / 2 + radius * Math.sin(endAngle);

  const largeArcFlag = endAngle - startAngle <= Math.PI ? "0" : "1";

  const pathData = `M ${startX} ${startY} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${endX} ${endY}`;

  return (
    <div
      ref={knobRef}
      onMouseDown={() => setIsDragging(true)}
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
      {/* Background SVG path */}
      <svg
        width="100%"
        height="100%"
        viewBox={`0 0 ${size} ${size}`}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          overflow: "visible",
        }}
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
          stroke="#00f0ff"
          strokeWidth="4"
          fill="none"
          strokeLinecap="round"
          filter="url(#glow)"
        />
      </svg>

      {/* Rotating knob image */}
      <img
        src="./assets/knob.svg"
        alt="Knob"
        draggable={false}
        style={{
          width: "80%",
          height: "80%",
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
      Array.from({ length: dimOutput }, () => 0.5)
    )
  );

  const range = (size) => Array.from({ length: size }, (_, i) => i);
  const cartesianProduct = (arrays) => arrays.reduce((a, b) => a.flatMap(d => b.map(e => [...d, e])), [[]]);

  return <div>
    <h2>Mixer {props.id}</h2>

    <div
      id="panel"
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
            gridColumn: output + 1,
            gridRow: input + 1,
            display: "grid",
          }}
        >
          <Knob
            value={matrix[input][output]}
            size={knobSize}
            onChange={(val) => {
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

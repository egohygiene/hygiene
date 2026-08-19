import { writeFileSync } from "node:fs";

const updated = 1786944000000;
let sequence = 0;

function base(id, type, x, y, width, height, color) {
  sequence += 1;
  return {
    id,
    type,
    x,
    y,
    width,
    height,
    angle: 0,
    strokeColor: color,
    backgroundColor: "transparent",
    fillStyle: "solid",
    strokeWidth: 2,
    strokeStyle: "solid",
    roughness: 1,
    opacity: 100,
    groupIds: [],
    frameId: null,
    index: `a${sequence.toString(36).padStart(3, "0")}`,
    roundness: { type: 3 },
    seed: 1000 + sequence * 7919,
    version: 1,
    versionNonce: 2000 + sequence * 3571,
    isDeleted: false,
    boundElements: [],
    updated,
    link: null,
    locked: false,
  };
}

function rectangle(id, x, y, width, height, stroke, fill, opacity = 100, dashed = false) {
  return {
    ...base(id, "rectangle", x, y, width, height, stroke),
    backgroundColor: fill,
    opacity,
    strokeStyle: dashed ? "dashed" : "solid",
  };
}

function textElement(id, text, x, y, width, height, color, fontSize = 18, align = "center") {
  const element = base(id, "text", x, y, width, height, color);
  delete element.roundness;
  return {
    ...element,
    strokeWidth: 1,
    roughness: 0,
    fontSize,
    fontFamily: 1,
    text,
    textAlign: align,
    verticalAlign: "middle",
    containerId: null,
    originalText: text,
    autoResize: false,
    lineHeight: 1.25,
  };
}

function arrow(id, start, end, color = "#94a3b8", dashed = false) {
  const x = start.x;
  const y = start.y;
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  const element = base(id, "arrow", x, y, dx, dy, color);
  delete element.roundness;
  return {
    ...element,
    points: [[0, 0], [dx, dy]],
    lastCommittedPoint: null,
    startBinding: null,
    endBinding: null,
    startArrowhead: null,
    endArrowhead: "arrow",
    elbowed: false,
    strokeStyle: dashed ? "dashed" : "solid",
  };
}

const planes = [
  {
    id: "control",
    title: "ARCHITECTURE & CONTROL PLANE",
    subtitle: "Define · create · converge · observe",
    y: 170,
    color: "#c084fc",
    fill: "#261447",
    nodes: [
      ["hygiene", "architecture · registry · policy"],
      [".github", "organization-facing defaults"],
      ["aether", "AI specs · skills · agents"],
      ["holon", "create repositories"],
      ["pace", "converge the fleet"],
      ["observatory", "maturity · evidence · telemetry"],
    ],
  },
  {
    id: "platform",
    title: "DEVELOPER & RUNTIME PLATFORM",
    subtitle: "Reproducible from laptop to CI",
    y: 440,
    color: "#22d3ee",
    fill: "#083344",
    nodes: [
      ["realm", "OCI · Dev Containers · Nix · hosts"],
      ["mantle", "portable shell runtime"],
      ["relay", "reusable CI · release workflows"],
      ["egolint", "quality policy · reports"],
      ["empathy", "golden consumer · integration"],
    ],
  },
  {
    id: "content",
    title: "CONTENT TRANSFORMATION & PUBLISHING",
    subtitle: "Specialized engines, one orchestration facade",
    y: 710,
    color: "#fb923c",
    fill: "#3f1d0b",
    nodes: [
      ["flow", "cross-holon orchestration"],
      ["aniflow", "temporal video engine"],
      ["optiflow", "safe collection optimization"],
      ["renderflow", "spec-driven derivatives"],
      ["beacon", "package · publish · distribute"],
    ],
  },
  {
    id: "knowledge",
    title: "KNOWLEDGE & RESEARCH",
    subtitle: "Capture · structure · curate · preserve · learn",
    y: 980,
    color: "#4ade80",
    fill: "#102a1d",
    nodes: [
      ["mindcap", "capture · verify · archive"],
      ["mindgarden", "semantic knowledge system"],
      ["akashic", "curated public knowledge"],
      ["athena", "raw references · archives"],
      ["reflector", "recursive-engineering research"],
    ],
  },
  {
    id: "experience",
    title: "IDENTITY, PRODUCT & EXPERIENCE",
    subtitle: "A coherent public and personal surface",
    y: 1250,
    color: "#fb7185",
    fill: "#3b1024",
    nodes: [
      ["identity", "tokens · voice · brand assets"],
      ["egohygiene", "private Flutter product"],
      ["egohygiene.io", "site · docs · playground"],
      ["store", "provider-neutral commerce"],
    ],
  },
];

const elements = [];
const centers = new Map();

elements.push(textElement("title", "EGO HYGIENE ECOSYSTEM ARCHITECTURE", 80, 35, 2040, 55, "#f8fafc", 34));
elements.push(textElement("subtitle", "25 independently useful repositories · one owner per capability · versioned artifacts and contracts", 80, 95, 2040, 34, "#cbd5e1", 18));

for (const plane of planes) {
  elements.push(rectangle(`group-${plane.id}`, 55, plane.y, 2090, 230, plane.color, plane.fill, 42));
  elements.push(textElement(`group-${plane.id}-title`, plane.title, 85, plane.y + 25, 300, 45, plane.color, 22));
  elements.push(textElement(`group-${plane.id}-sub`, plane.subtitle, 85, plane.y + 72, 300, 58, "#cbd5e1", 15));

  plane.nodes.forEach(([name, role], index) => {
    const x = 420 + index * 285;
    const y = plane.y + 68;
    const width = 255;
    const height = 115;
    const id = `node-${name.replaceAll(".", "-")}`;
    elements.push(rectangle(id, x, y, width, height, plane.color, "#111827", 100));
    elements.push(textElement(`${id}-text`, `${name}\n${role}`, x + 12, y + 12, width - 24, height - 24, "#f8fafc", 17));
    centers.set(name, { x: x + width / 2, y: y + height / 2 });
  });
}

elements.push(rectangle("group-future", 55, 1530, 2090, 175, "#94a3b8", "#1f2937", 45, true));
elements.push(textElement("future-title", "PROPOSED FUTURE BOUNDARY", 85, 1560, 300, 42, "#cbd5e1", 21));
elements.push(textElement("future-sub", "Create only after Realm's artifact contract is stable", 85, 1605, 300, 55, "#94a3b8", 15));
elements.push(rectangle("node-firmament", 420, 1560, 540, 95, "#94a3b8", "#111827", 100, true));
elements.push(textElement("node-firmament-text", "firmament (proposed)\nOpenTofu/Pulumi · local and multi-cloud infrastructure", 440, 1570, 500, 75, "#f8fafc", 17));
centers.set("firmament", { x: 690, y: 1607 });

const relationships = [
  ["hygiene", "holon"], ["hygiene", "pace"], ["hygiene", "observatory"], ["hygiene", ".github"],
  ["aether", "holon"], ["aether", "pace"], ["holon", "empathy"], ["pace", "empathy"],
  ["mantle", "realm"], ["realm", "empathy"], ["egolint", "relay"], ["relay", "empathy"],
  ["relay", "observatory"], ["egolint", "observatory"],
  ["flow", "aniflow"], ["flow", "optiflow"], ["flow", "renderflow"], ["flow", "beacon"], ["renderflow", "beacon"],
  ["athena", "mindcap"], ["mindcap", "mindgarden"], ["mindgarden", "akashic"], ["reflector", "observatory"],
  ["identity", "egohygiene"], ["identity", "egohygiene.io"], ["identity", "store"], ["identity", "beacon"],
  ["mindgarden", "egohygiene"], ["beacon", "egohygiene.io"], ["store", "egohygiene.io"],
  ["realm", "firmament"], ["beacon", "firmament"],
];

relationships.forEach(([from, to], index) => {
  const start = centers.get(from);
  const end = centers.get(to);
  if (start && end) elements.push(arrow(`edge-${index}`, start, end, "#64748b", to === "firmament"));
});

elements.push(textElement(
  "legend",
  "Arrows show versioned artifacts, contracts, or control flow—not copied source. Canonical semantics live in ARCHITECTURE.md and catalog/repositories.yaml.",
  1010,
  1570,
  1060,
  70,
  "#cbd5e1",
  16,
));

const document = {
  type: "excalidraw",
  version: 2,
  source: "https://github.com/egohygiene/hygiene",
  elements,
  appState: {
    viewBackgroundColor: "#070b14",
    gridSize: 20,
    gridStep: 5,
    gridModeEnabled: false,
    currentItemStrokeColor: "#94a3b8",
    currentItemBackgroundColor: "transparent",
  },
  files: {},
};

writeFileSync("ecosystem.excalidraw", `${JSON.stringify(document, null, 2)}\n`, "utf8");

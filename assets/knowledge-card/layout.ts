export const KNOWLEDGE_CARD_LAYOUT = {
  id: "zdk-knowledge-card-v1",
  width: 1080,
  height: 1920,
  fps: 30,
  transitionFrames: 12,
  captionTransitionDelayFrames: 8,
  portrait: {
    left: 244,
    bottom: 54,
    width: 592,
    height: 780,
    borderRadius: 64,
  },
  safeArea: {
    top: 90,
    right: 72,
    bottom: 150,
    left: 72,
  },
  sceneTypes: [
    "light-information-board",
    "portrait-picture-in-picture",
    "dark-emphasis",
    "summary-checklist",
  ],
} as const;

